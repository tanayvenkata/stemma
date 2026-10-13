import sys
import os
from pathlib import Path
import time
import json
import hashlib
from typing import List, Dict, Optional
from contextlib import asynccontextmanager
from datetime import date
from collections import defaultdict

# Demo cache: simple dicts populated from JSON on startup (no TTLCache needed)

# Add project root to sys.path to allow imports from scripts/
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Production config: disable reranker to stay under 512MB memory limit
USE_RERANKER = os.getenv("USE_RERANKER", "false").lower() == "true"

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from scripts.retrieve import (
    FocusGroupRetrieverV2, LLMRouter, RetrievalResult,
    StrategyMemoRetriever, StrategyRetrievalResult, RouterResult
)
from scripts.synthesize import FocusGroupSynthesizer, get_friendly_error
from eval.config import STRATEGY_TOP_K_PER_RACE, DATA_DIR, PROJECT_ROOT, USE_HYBRID_RETRIEVAL

# Lazy import for hybrid retrieval (requires rank_bm25, not in prod requirements)
HybridFocusGroupRetriever = None
if USE_HYBRID_RETRIEVAL:
    try:
        from scripts.retrieval.hybrid import HybridFocusGroupRetriever
    except ImportError:
        print("Warning: HybridFocusGroupRetriever not available, falling back to dense retrieval")
from api.schemas import (
    SearchRequest, SearchResponse, SynthesisRequest, MacroSynthesisRequest,
    GroupedResult, RetrievalChunk,
    LightMacroSynthesisRequest, DeepMacroSynthesisRequest, DeepMacroResponse,
    StrategyChunk, StrategyGroupedResult, UnifiedSearchResponse,
    StrategySynthesisRequest, StrategyMacroSynthesisRequest,
    UnifiedMacroSynthesisRequest, CorpusItem, DocumentContent
)
from api.observability import (
    QueryTracer, log_retrieval_decision, log_score_distribution,
    log_router_decision, log_result_summary
)

# Global instances
retriever: Optional[FocusGroupRetrieverV2] = None
strategy_retriever: Optional[StrategyMemoRetriever] = None
router: Optional[LLMRouter] = None
synthesizer: Optional[FocusGroupSynthesizer] = None

# === Demo Cache (populated from JSON on startup, never modified at runtime) ===
# Only the 4 suggested queries are cached - all other queries make fresh LLM calls
search_cache: Dict[str, dict] = {}
light_summary_cache: Dict[str, str] = {}
macro_synthesis_cache: Dict[str, str] = {}
deep_summary_cache: Dict[str, str] = {}
unified_macro_cache: Dict[str, str] = {}
strategy_light_cache: Dict[str, str] = {}
strategy_deep_cache: Dict[str, str] = {}
strategy_macro_cache: Dict[str, str] = {}

# Rate limiting: IP -> {"count": int, "date": date}
rate_limits: Dict[str, Dict] = defaultdict(lambda: {"count": 0, "date": date.today()})
DAILY_RATE_LIMIT = int(os.getenv("DAILY_RATE_LIMIT", "100"))


def _get_cache_key(query: str, top_k: int, score_threshold: float, use_hybrid: bool = False) -> str:
    """Generate cache key from query parameters."""
    raw = f"{query.lower().strip()}:{top_k}:{score_threshold}:{use_hybrid}"
    return hashlib.md5(raw.encode()).hexdigest()


def _check_rate_limit(client_ip: str) -> bool:
    """Check if client is within rate limit. Returns True if allowed."""
    today = date.today()
    entry = rate_limits[client_ip]

    # Reset count if new day
    if entry["date"] != today:
        entry["count"] = 0
        entry["date"] = today

    if entry["count"] >= DAILY_RATE_LIMIT:
        return False

    entry["count"] += 1
    return True

# Example queries to pre-warm (from frontend landing page)
# Selected for variety: quotes-only, lessons-only, and mixed routing
EXAMPLE_QUERIES = [
    "Ohio voters on economy",                                  # quotes (0.62)
    "What messaging mistakes did campaigns make?",             # lessons (0.64)
    "Where did Democratic messaging fail with union voters?",  # both (0.62)
    "What do swing voters want to hear about inflation?",      # both (0.62)
]

# Default search params for pre-warming
DEFAULT_TOP_K = 5
DEFAULT_SCORE_THRESHOLD = 0.50

# Persistent demo cache file (committed to repo for zero-cost demo queries)
DEMO_CACHE_FILE = PROJECT_ROOT / "data" / "demo_cache.json"


def _load_demo_cache() -> bool:
    """Load pre-generated demo cache from JSON file. Returns True if loaded."""
    if not DEMO_CACHE_FILE.exists():
        return False

    try:
        with open(DEMO_CACHE_FILE) as f:
            demo_cache = json.load(f)

        queries_loaded = 0
        for query, cache_data in demo_cache.get("queries", {}).items():
            cache_key = cache_data["cache_key"]

            # Load search results
            search_cache[cache_key] = cache_data["search_results"]

            # Load light summaries
            for fg_id, summary in cache_data.get("light_summaries", {}).items():
                light_summary_cache[f"{cache_key}:{fg_id}"] = summary

            # Load deep summaries
            for fg_id, synthesis in cache_data.get("deep_summaries", {}).items():
                deep_summary_cache[f"deep:{cache_key}:{fg_id}"] = synthesis

            # Load macro synthesis
            if cache_data.get("macro_synthesis"):
                macro_synthesis_cache[f"macro:{cache_key}"] = cache_data["macro_synthesis"]

            # Load strategy light summaries
            for race_id, summary in cache_data.get("strategy_light", {}).items():
                strategy_light_cache[f"strategy:{cache_key}:{race_id}"] = summary

            # Load strategy deep summaries
            for race_id, synthesis in cache_data.get("strategy_deep", {}).items():
                strategy_deep_cache[f"strategy_deep:{cache_key}:{race_id}"] = synthesis

            # Load strategy macro (if exists)
            if cache_data.get("strategy_macro"):
                # Compute race_ids_hash for the key
                race_ids = list(cache_data.get("strategy_light", {}).keys())
                race_ids_hash = hashlib.md5(",".join(sorted(race_ids)).encode()).hexdigest()[:8]
                strategy_macro_cache[f"strategy_macro:{cache_key}:{race_ids_hash}"] = cache_data["strategy_macro"]

            queries_loaded += 1
            print(f"  Loaded cache: {query}")

        print(f"Loaded {queries_loaded} queries from demo cache ({DEMO_CACHE_FILE})")
        return True
    except Exception as e:
        print(f"Failed to load demo cache: {e}")
        return False


def _prewarm_query(query: str) -> None:
    """Execute a search query and cache the result. Used for pre-warming."""
    from api.schemas import GroupedResult, StrategyGroupedResult, RetrievalChunk, StrategyChunk

    cache_key = _get_cache_key(query, DEFAULT_TOP_K, DEFAULT_SCORE_THRESHOLD, USE_HYBRID_RETRIEVAL)

    # Skip if already cached
    if cache_key in search_cache:
        return

    # Route the query
    route_result = router.route_unified(query)
    content_type = route_result.content_type

    quotes_results = []
    lessons_results = []

    # Fetch focus group quotes if needed
    if content_type in ("quotes", "both"):
        fg_ids = route_result.focus_group_ids
        results_by_fg = retriever.retrieve_per_focus_group(
            query=query,
            top_k_per_fg=DEFAULT_TOP_K,
            score_threshold=DEFAULT_SCORE_THRESHOLD,
            filter_focus_groups=fg_ids
        )

        for fg_id, chunks in results_by_fg.items():
            if not chunks:
                continue
            top_score = max(c.score for c in chunks)
            if top_score < DEFAULT_SCORE_THRESHOLD:
                continue

            fg_meta = retriever._load_focus_group_metadata(fg_id)
            api_chunks = [
                RetrievalChunk(
                    chunk_id=c.chunk_id, score=c.score, content=c.content,
                    content_original=c.content_original, focus_group_id=c.focus_group_id,
                    participant=c.participant, participant_profile=c.participant_profile,
                    section=c.section, source_file=c.source_file, line_number=c.line_number,
                    preceding_moderator_q=c.preceding_moderator_q
                ) for c in chunks
            ]
            quotes_results.append(GroupedResult(
                focus_group_id=fg_id, focus_group_metadata=fg_meta, chunks=api_chunks
            ))

    # Fetch strategy lessons if needed
    if content_type in ("lessons", "both"):
        strategy_grouped = strategy_retriever.retrieve_grouped(
            query=query, top_k=STRATEGY_TOP_K_PER_RACE * 5,
            outcome_filter=route_result.outcome_filter, score_threshold=0.0
        )

        for group in strategy_grouped:
            top_chunks = sorted(group.chunks, key=lambda c: c.score, reverse=True)[:STRATEGY_TOP_K_PER_RACE]
            if not top_chunks or top_chunks[0].score < DEFAULT_SCORE_THRESHOLD:
                continue

            race_meta = strategy_retriever._get_race_metadata(group.race_id)
            api_chunks = [
                StrategyChunk(
                    chunk_id=c.chunk_id, score=c.score, content=c.content,
                    race_id=c.race_id, section=c.section, subsection=c.subsection,
                    outcome=c.outcome, state=c.state, year=c.year, margin=c.margin,
                    source_file=c.source_file, line_number=c.line_number
                ) for c in top_chunks
            ]
            lessons_results.append(StrategyGroupedResult(
                race_id=group.race_id, race_metadata=race_meta, chunks=api_chunks
            ))

    # Store search results in cache
    cache_data = {
        "content_type": content_type,
        "quotes": [q.model_dump() for q in quotes_results],
        "lessons": [l.model_dump() for l in lessons_results],
        "stats": {
            "retrieval_time_ms": 0,  # Pre-warmed
            "total_quotes": sum(len(g.chunks) for g in quotes_results),
            "total_lessons": sum(len(g.chunks) for g in lessons_results),
            "focus_groups_count": len(quotes_results),
            "races_count": len(lessons_results),
            "routed_to": content_type,
            "outcome_filter": route_result.outcome_filter,
            "cached": True,
            "prewarmed": True
        }
    }
    search_cache[cache_key] = cache_data

    # Pre-warm light summaries and macro synthesis for focus group results
    if quotes_results and synthesizer:
        fg_summaries = {}
        fg_metadata = {}
        top_quotes_dict = {}

        for fg in quotes_results:
            fg_id = fg.focus_group_id
            fg_metadata[fg_id] = fg.focus_group_metadata

            # Convert chunks for synthesizer
            from scripts.retrieve import RetrievalResult as ScriptRetrievalResult
            script_chunks = [
                ScriptRetrievalResult(
                    chunk_id=c.chunk_id, score=c.score, content=c.content,
                    content_original=c.content_original, focus_group_id=c.focus_group_id,
                    participant=c.participant, participant_profile=c.participant_profile,
                    section=c.section, source_file=c.source_file, line_number=c.line_number,
                    preceding_moderator_q=c.preceding_moderator_q or ""
                ) for c in fg.chunks
            ]
            top_quotes_dict[fg_id] = script_chunks

            # Generate and cache light summary
            summary_cache_key = f"{cache_key}:{fg_id}"
            if summary_cache_key not in light_summary_cache:
                fg_name = fg.focus_group_metadata.get("location", fg_id)
                summary = synthesizer.light_summary(script_chunks, query, fg_name)
                light_summary_cache[summary_cache_key] = summary
                fg_summaries[fg_id] = summary
            else:
                fg_summaries[fg_id] = light_summary_cache[summary_cache_key]

            # Generate and cache deep summary (for suggested queries, pre-warm everything)
            deep_cache_key = f"deep:{cache_key}:{fg_id}"
            if deep_cache_key not in deep_summary_cache:
                fg_name = fg.focus_group_metadata.get("location", fg_id)
                # Fetch expanded context for deep synthesis
                context = retriever.fetch_expanded_context(script_chunks, max_chunks=5) if retriever else []
                # deep_synthesis(quotes, source_context, query, focus_group_name)
                deep_result = synthesizer.deep_synthesis(script_chunks, context, query, fg_name)
                deep_summary_cache[deep_cache_key] = deep_result
                print(f"    Pre-warmed deep summary for {fg_id}")

        # Generate and cache macro synthesis if we have multiple FGs
        if len(fg_summaries) >= 2:
            macro_cache_key = f"macro:{cache_key}"
            if macro_cache_key not in macro_synthesis_cache:
                macro_result = synthesizer.light_macro_synthesis(
                    fg_summaries=fg_summaries,
                    top_quotes=top_quotes_dict,
                    fg_metadata=fg_metadata,
                    query=query
                )
                macro_synthesis_cache[macro_cache_key] = macro_result

    # Pre-warm strategy light summaries
    if lessons_results and synthesizer:
        for race in lessons_results:
            race_id = race.race_id
            strategy_cache_key = f"strategy:{cache_key}:{race_id}"

            if strategy_cache_key not in strategy_light_cache:
                race_meta = race.race_metadata
                race_name = f"{race_meta.get('state', 'Unknown')} {race_meta.get('year', '?')}"

                # Build context from chunks for synthesis
                chunks_text = []
                for c in race.chunks:
                    chunks_text.append(f"[{c.section}] {c.content}")
                context = "\n\n".join(chunks_text)

                prompt = f"""You are a senior political strategist summarizing campaign lessons.

Query: "{query}"
Race: {race_name}

Strategy memo excerpts:
{context}

Write a 1-2 sentence summary of the key lesson(s) from this race relevant to the query.
Be specific - include what worked/failed and why. No fluff."""

                try:
                    response = synthesizer.client.chat.completions.create(
                        model=synthesizer.model,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=150,
                        temperature=0.3
                    )
                    summary = response.choices[0].message.content.strip()
                    strategy_light_cache[strategy_cache_key] = summary
                    print(f"    Pre-warmed strategy summary for {race_id}")
                except Exception as e:
                    print(f"    Failed to pre-warm strategy summary for {race_id}: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize expensive resources on startup."""
    global retriever, strategy_retriever, router, synthesizer
    print(f"Initializing resources (reranker={'enabled' if USE_RERANKER else 'disabled'}, hybrid={'enabled' if USE_HYBRID_RETRIEVAL else 'disabled'})...")
    # Initialize with same settings as app.py
    # Note: app.py uses st.cache_resource, here we use global singletons
    # USE_RERANKER=false for production (512MB limit), true for local dev
    # USE_HYBRID_RETRIEVAL=false by default, enables BM25+dense fusion
    if USE_HYBRID_RETRIEVAL and HybridFocusGroupRetriever is not None:
        retriever = HybridFocusGroupRetriever(use_router=True, use_reranker=USE_RERANKER, verbose=False)
    else:
        retriever = FocusGroupRetrieverV2(use_router=True, use_reranker=USE_RERANKER, verbose=False)
    strategy_retriever = StrategyMemoRetriever(use_reranker=USE_RERANKER, verbose=False)
    router = LLMRouter()
    synthesizer = FocusGroupSynthesizer(verbose=False)
    print("Resources initialized.")

    # Load demo cache from JSON (zero LLM cost) or fall back to live pre-warming
    if os.getenv("PREWARM_CACHE", "true").lower() == "true":
        # Try loading from persistent JSON cache first
        if _load_demo_cache():
            print("Demo cache loaded from file (no LLM calls needed).")
        else:
            # Fall back to live pre-warming (makes LLM calls)
            print(f"Pre-warming cache with {len(EXAMPLE_QUERIES)} example queries...")
            for query in EXAMPLE_QUERIES:
                try:
                    _prewarm_query(query)
                    print(f"  Cached: {query}")
                except Exception as e:
                    print(f"  Failed to cache '{query}': {e}")
            print("Cache pre-warming complete.")

    yield
    # Cleanup if needed
    print("Shutting down...")

app = FastAPI(title="Focus Group Search API", lifespan=lifespan)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local dev
        "https://campaign-intel.vercel.app",  # Production frontend
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",  # Preview deployments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "resources_loaded": retriever is not None}

@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    if not retriever or not router:
        raise HTTPException(status_code=503, detail="Service not ready")

    start_time = time.time()
    
    # 1. Route (retriever handles routing internally if filter_focus_groups is None)
    # The retriever.retrieve_per_focus_group handles routing internally if filter_focus_groups is None
    # but app.py does it explicitly to show the decision. Let's rely on retriever's internal logic 
    # OR replicate app.py if we want to return the routing decision in stats.
    
    # Let's replicate app.py logic to capture routing time stats if possible, 
    # but retrieve_per_focus_group is convenient.
    # For now, we'll let retrieve_per_focus_group handle it, or we can add a router endpoint later if needed.
    
    # Actually, app.py calls router.route() explicitly. 
    # To keep it simple and robust, let's just call retrieve_per_focus_group.
    # It returns a dict of results.

    results_by_fg = retriever.retrieve_per_focus_group(
        query=request.query,
        top_k_per_fg=request.top_k,
        score_threshold=request.score_threshold
    )
    
    retrieval_time = (time.time() - start_time) * 1000

    # Convert to response model
    grouped_results = []
    total_quotes = 0
    
    for fg_id, chunks in results_by_fg.items():
        if not chunks:
            continue
            
        fg_meta = retriever._load_focus_group_metadata(fg_id)
        
        # Convert dataclass chunks to Pydantic chunks
        api_chunks = []
        for c in chunks:
            api_chunks.append(RetrievalChunk(
                chunk_id=c.chunk_id,
                score=c.score,
                content=c.content,
                content_original=c.content_original,
                focus_group_id=c.focus_group_id,
                participant=c.participant,
                participant_profile=c.participant_profile,
                section=c.section,
                source_file=c.source_file,
                line_number=c.line_number,
                preceding_moderator_q=c.preceding_moderator_q
            ))
            
        grouped_results.append(GroupedResult(
            focus_group_id=fg_id,
            focus_group_metadata=fg_meta,
            chunks=api_chunks
        ))
        total_quotes += len(api_chunks)

    return SearchResponse(
        results=grouped_results,
        stats={
            "retrieval_time_ms": round(retrieval_time),
            "total_quotes": total_quotes,
            "focus_groups_count": len(grouped_results)
        }
    )


@app.post("/search/stream")
async def search_stream(request: SearchRequest):
    """Streaming search endpoint that yields status events during processing."""
    if not retriever or not router:
        raise HTTPException(status_code=503, detail="Service not ready")

    def build_response(results_by_fg: Dict, retrieval_time: float) -> dict:
        """Build the final response dict."""
        grouped_results = []
        total_quotes = 0

        for fg_id, chunks in results_by_fg.items():
            if not chunks:
                continue

            fg_meta = retriever._load_focus_group_metadata(fg_id)

            api_chunks = []
            for c in chunks:
                api_chunks.append({
                    "chunk_id": c.chunk_id,
                    "score": c.score,
                    "content": c.content,
                    "content_original": c.content_original,
                    "focus_group_id": c.focus_group_id,
                    "participant": c.participant,
                    "participant_profile": c.participant_profile,
                    "section": c.section,
                    "source_file": c.source_file,
                    "line_number": c.line_number,
                    "preceding_moderator_q": c.preceding_moderator_q
                })

            grouped_results.append({
                "focus_group_id": fg_id,
                "focus_group_metadata": fg_meta,
                "chunks": api_chunks
            })
            total_quotes += len(api_chunks)

        return {
            "results": grouped_results,
            "stats": {
                "retrieval_time_ms": round(retrieval_time),
                "total_quotes": total_quotes,
                "focus_groups_count": len(grouped_results)
            }
        }

    def event_generator():
        start_time = time.time()

        # Step 1: Routing
        yield json.dumps({"type": "status", "step": "routing", "message": "Analyzing query intent..."}) + "\n"

        fg_ids = router.route(request.query)
        if fg_ids is None:
            fg_ids = router._get_all_ids()
            yield json.dumps({"type": "status", "step": "filtering", "message": f"Searching all {len(fg_ids)} focus groups..."}) + "\n"
        else:
            yield json.dumps({"type": "status", "step": "filtering", "message": f"Routing to {len(fg_ids)} relevant focus groups..."}) + "\n"

        # Step 2: Searching
        yield json.dumps({"type": "status", "step": "searching", "message": "Scanning transcripts..."}) + "\n"

        results_by_fg = retriever.retrieve_per_focus_group(
            query=request.query,
            top_k_per_fg=request.top_k,
            score_threshold=request.score_threshold,
            filter_focus_groups=fg_ids  # Skip internal routing since we already routed
        )

        # Step 3: Ranking
        yield json.dumps({"type": "status", "step": "ranking", "message": "Ranking relevance..."}) + "\n"

        retrieval_time = (time.time() - start_time) * 1000

        # Step 4: Complete
        yield json.dumps({"type": "status", "step": "complete", "message": "Done"}) + "\n"

        # Final results
        response_data = build_response(results_by_fg, retrieval_time)
        yield json.dumps({"type": "results", "data": response_data}) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")


@app.post("/search/unified", response_model=UnifiedSearchResponse)
async def search_unified(search_request: SearchRequest, request: Request):
    """
    Unified search that routes to quotes (focus groups) and/or lessons (strategy memos).
    Uses LLM router to determine content type based on query intent.
    """
    if not retriever or not strategy_retriever or not router:
        raise HTTPException(status_code=503, detail="Service not ready")

    # Rate limiting
    client_ip = request.client.host if request.client else "unknown"
    if not _check_rate_limit(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Daily request limit reached. Please try again tomorrow."
        )

    # Check cache first
    cache_key = _get_cache_key(
        search_request.query,
        search_request.top_k,
        search_request.score_threshold,
        USE_HYBRID_RETRIEVAL
    )
    if cache_key in search_cache:
        cached = search_cache[cache_key]
        # Add cache hit indicator to stats
        cached_response = cached.copy()
        cached_response["stats"] = {**cached["stats"], "cached": True}
        return UnifiedSearchResponse(**cached_response)

    # Initialize tracer for observability
    tracer = QueryTracer(query=search_request.query)

    quotes_results = []
    lessons_results = []

    # Route to determine content type
    try:
        with tracer.step("routing"):
            route_result = router.route_unified(search_request.query)
            content_type = route_result.content_type
            log_router_decision(
                tracer, content_type, route_result.outcome_filter,
                f"FG IDs: {route_result.focus_group_ids[:3] if route_result.focus_group_ids else 'all'}"
            )
    except Exception as e:
        tracer.log("error", {"type": "routing_failure", "message": str(e)})
        # Fallback to searching both when router fails
        content_type = "both"
        route_result = RouterResult(
            content_type="both",
            focus_group_ids=None,
            outcome_filter=None,
            reasoning="Router failed, falling back to comprehensive search"
        )

    # Fetch focus group quotes if needed
    if content_type in ("quotes", "both"):
        try:
            with tracer.step("fg_retrieval"):
                fg_ids = route_result.focus_group_ids
                results_by_fg = retriever.retrieve_per_focus_group(
                    query=search_request.query,
                    top_k_per_fg=search_request.top_k,
                    score_threshold=search_request.score_threshold,
                    filter_focus_groups=fg_ids
                )

                # Log score distribution for debugging
                all_fg_scores = []
                for fg_id, chunks in results_by_fg.items():
                    all_fg_scores.extend([c.score for c in chunks])
                    if not chunks:
                        continue

                    # Filter out FGs where top chunk is below threshold
                    top_score = max(c.score for c in chunks)
                    if top_score < search_request.score_threshold:
                        continue

                    fg_meta = retriever._load_focus_group_metadata(fg_id)
                    api_chunks = [
                        RetrievalChunk(
                            chunk_id=c.chunk_id,
                            score=c.score,
                            content=c.content,
                            content_original=c.content_original,
                            focus_group_id=c.focus_group_id,
                            participant=c.participant,
                            participant_profile=c.participant_profile,
                            section=c.section,
                            source_file=c.source_file,
                            line_number=c.line_number,
                            preceding_moderator_q=c.preceding_moderator_q
                        )
                        for c in chunks
                    ]
                    quotes_results.append(GroupedResult(
                        focus_group_id=fg_id,
                        focus_group_metadata=fg_meta,
                        chunks=api_chunks
                    ))

                log_score_distribution(tracer, "fg", all_fg_scores)
                tracer.log("fg_results", {
                    "focus_groups": len(quotes_results),
                    "total_quotes": sum(len(g.chunks) for g in quotes_results)
                })
        except Exception as e:
            tracer.log("error", {"type": "fg_retrieval_failure", "message": str(e)})
            # Continue without FG results rather than failing completely

    # Fetch strategy lessons if needed
    if content_type in ("lessons", "both"):
        try:
            with tracer.step("strategy_retrieval"):
                strategy_grouped = strategy_retriever.retrieve_grouped(
                    query=search_request.query,
                    top_k=STRATEGY_TOP_K_PER_RACE * 5,
                    outcome_filter=route_result.outcome_filter,
                    score_threshold=0.0  # Rely on threshold filter below
                )

                # Track filtering for observability
                races_before_filter = len(strategy_grouped)
                filtered_races = []

                for group in strategy_grouped:
                    top_chunks = sorted(group.chunks, key=lambda c: c.score, reverse=True)[:STRATEGY_TOP_K_PER_RACE]
                    if not top_chunks:
                        continue

                    top_score = top_chunks[0].score
                    if top_score < search_request.score_threshold:
                        filtered_races.append({
                            "race_id": group.race_id,
                            "top_score": round(top_score, 3),
                            "threshold": search_request.score_threshold
                        })
                        continue

                    race_meta = strategy_retriever._get_race_metadata(group.race_id)
                    api_chunks = [
                        StrategyChunk(
                            chunk_id=c.chunk_id,
                            score=c.score,
                            content=c.content,
                            race_id=c.race_id,
                            section=c.section,
                            subsection=c.subsection,
                            outcome=c.outcome,
                            state=c.state,
                            year=c.year,
                            margin=c.margin,
                            source_file=c.source_file,
                            line_number=c.line_number
                        )
                        for c in top_chunks
                    ]
                    lessons_results.append(StrategyGroupedResult(
                        race_id=group.race_id,
                        race_metadata=race_meta,
                        chunks=api_chunks
                    ))

                # Log filtering decision
                log_retrieval_decision(
                    tracer, "strategy",
                    races_before_filter, len(lessons_results),
                    search_request.score_threshold,
                    f"Filtered out: {[r['race_id'] for r in filtered_races]}" if filtered_races else "No races filtered"
                )

                tracer.log("strategy_results", {
                    "races": len(lessons_results),
                    "total_lessons": sum(len(g.chunks) for g in lessons_results),
                    "filtered_out": filtered_races
                })
        except Exception as e:
            tracer.log("error", {"type": "strategy_retrieval_failure", "message": str(e)})
            # Continue without strategy results rather than failing completely

    # Complete trace with final summary
    log_result_summary(
        tracer,
        len(quotes_results),
        sum(len(g.chunks) for g in quotes_results),
        len(lessons_results),
        sum(len(g.chunks) for g in lessons_results)
    )
    trace = tracer.complete({
        "content_type": content_type,
        "fg_count": len(quotes_results),
        "races_count": len(lessons_results)
    })

    # Build response
    response_data = {
        "content_type": content_type,
        "quotes": quotes_results,
        "lessons": lessons_results,
        "stats": {
            "retrieval_time_ms": round(trace["total_duration_ms"]),
            "total_quotes": sum(len(g.chunks) for g in quotes_results),
            "total_lessons": sum(len(g.chunks) for g in lessons_results),
            "focus_groups_count": len(quotes_results),
            "races_count": len(lessons_results),
            "routed_to": content_type,
            "outcome_filter": route_result.outcome_filter,
            "cached": False
        }
    }

    return UnifiedSearchResponse(**response_data)



# ============ Corpus Explorer Endpoints ============

