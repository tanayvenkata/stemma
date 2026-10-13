# Content Hygiene Ledger

**Date:** 2026-10-11

**Scope:** every note under `plugins/stemma/skills/stemma/`. `check_notes.py` counts 123 notes plus `SKILL.md`.

**Method:**
1. Six read-only folder sweeps: Indexing, Retrieval, Generation, Architectures plus Production, and Evaluation in two parts.
2. One verification and cross-folder pass. In this pass every proposed row was checked against the note text, and consequential sources were opened before being cited. "(verified 2026-10)" appears only where the primary source was actually fetched.
3. A book-reference check. No note attributes its content to a book, author, or chapter (grep for book/chapter: clean).

**Result:**
- 75 proposals verified: 63 applied (62 Improved, several modified from the proposal, and 1 Removed deliberately) and 12 Preserved (5 rejected proposals, plus 7 already fine or merged into another row).
- 5 cross-folder edits: 4 for the migration procedure and 1 defining evidence-token ratio.
- 32 notes changed. Each one has `reviewed: 2026-10-11` in its frontmatter.
- 0 `Missing` rows.

**How to read the Class column:**
- durable: a mechanism that holds regardless of system.
- measured: a result under stated conditions.
- hypothesis: plausible but unverified.
- time-sensitive: a landscape fact that can go out of date.

## Indexing Pipeline

| Note | Claim (short) | Issue | Class | Status | What changed |
|---|---|---|---|---|---|
| Agentic Chunking | "Highest coherence (~87% accuracy on clinical benchmarks)" | unsourced number, superlative | measured | Improved | Now a hypothesis to confirm against a recursive baseline on labeled regions |
| Agentic Chunking | "Slowest and most expensive method" | superlative | hypothesis | Improved | "Among the slowest and most expensive"; one LLM decision per candidate boundary |
| Agentic Chunking | When-to-Use domains asserted as settled | unproven fit | hypothesis | Improved | Lead-in line: candidates to test against a recursive/structure-aware baseline |
| Proposition-based Chunking | Index grows "5x–10x" | unsourced multiplier | measured | Improved | "Often several-fold; measure propositions per source chunk on a sample" |
| Proposition-based Chunking | "Maximum possible search precision" | superlative | measured | Improved | Cites Dense X Retrieval (arXiv 2312.06648, abstract checked): propositions outperform passage units; confirm on your queries |
| Proposition-based Chunking | "Fully standalone (zero dangling pronouns)" | overclaim, conflicts with rewrite-error risk | hypothesis | Improved | Meant to be standalone; audit a sample for ambiguity and unsupported facts |
| Proposition-based Chunking | Apple example "founded … in Cupertino, California" | factually shaky (founding location is usually given as Los Altos) | durable | Improved | Location removed from the source sentence and from proposition 3 (proposal fixed only the proposition); four propositions remain |
| Semantic Chunking | Split when distance "drops below" a percentile | inverted direction (diagram shows a spike) | durable | Improved | "rises above" |
| Semantic Chunking | Diagram distances 0.12/0.78 | read as thresholds | durable | Improved | Labelled "Illustrative distances (not thresholds to copy)" |
| Semantic Chunking | "10–50x more embedding calls" | unsourced multiplier | measured | Improved | Calls scale with sentence count; multiple depends on sentences per chunk |
| Semantic Chunking | "massive 3,000-token chunks" | illustrative number as fact | hypothesis | Improved | "very large chunks" |
| Semantic Chunking | Semantic chunking "is cheaper" than late chunking | contradicts overhead bullet above | hypothesis | Improved | Avoids a long-context model but pays per-sentence embedding cost; compare total indexing cost |
| Late Chunking | "then splits the embedding" | imprecise mechanism | durable | Improved | Mean-pools token embeddings per chunk span; cites arXiv 2409.04701 (abstract checked) |
| Late Chunking | "Long documents (8k+ tokens): Yes" | ignores input-limit constraint | durable | Improved | Long, context-dependent documents within the model's input limit; longer ones need overlapping macro-chunks (paper §3.1 checked) |
| Late Chunking | "Requires long-context model (8k+)" | model-specific figure | time-sensitive | Improved | Document length capped by the model's input limit |
| Late Chunking | "No information loss at chunk boundaries" | overclaim | durable | Improved | "Reduces context loss … pooling still compresses detail" |
| Late Chunking | Yes/No table as verdicts | unbaselined | hypothesis | Improved | Added: starting hypotheses; compare with the same boundaries embedded independently |
| IVF | `nlist` "√N or 4√N" | unsourced, and lower than library guidance | time-sensitive | Improved | Cites FAISS guidelines (verified 2026-10): 4√N–16√N below ~1M vectors, 30–256 training vectors per centroid |
| IVF | `nprobe` "1 to 16", "linearly increases latency" | unsourced range, overstated | measured | Improved | Start small; raise until recall vs exact search meets target; work grows with lists probed |
| IVF | Column "Typical Production Values" | presents heuristics as norms | measured | Improved | "Starting Point (tune on your data)" |
| IVF | "10M+ vectors … 2x RAM overhead of HNSW" | unsourced cutoff and multiplier; contradicts Vector Index | measured | Improved | Measure memory and recall for both; no fixed overhead or size cutoff |
| IVF | IVF-PQ "8-bit integers … billions" | conflates PQ with scalar quantization | durable | Improved | PQ stores sub-vector codes; measure the recall cost against exact search |
| Vector Index | "At 1,000,000 vectors … hundreds of ms" | unsourced; contradicts Flat Index | measured | Improved | The point where exhaustive search fails targets is found by measurement (links Flat Index) |
| Vector Index | Diagram "Best for <10k vectors" | fixed cutoff contradicts Flat Index | measured | Improved | "Small collections" |
| Vector Index | Matrix "Small datasets (<10k vectors)" | same | measured | Improved | Collections where exhaustive search meets latency needs (measure; see Flat Index) |
| Vector Index | HNSW "O(log N) search time" | stated as a bound | durable | Improved — proposal modified | The proposal said "sublinear, no guarantee", but the HNSW paper does report logarithmic scaling (abstract checked). Now "~log N (empirical)" plus a prose sentence citing the paper |
| Vector Index | IVF "O(N/K) search time" | ignores nprobe | durable | Improved | "~nprobe/K of N scanned" plus prose |
| Vector Index | HNSW "Best for production RAG" | superlative; matrix says "when memory permits" | hypothesis | Improved | "Default if RAM permits" |
| Metadata Extraction | "Document Hash (MD5/SHA)" | MD5 weak; payload example uses sha256 | durable | Improved | "Content Hash (SHA-256)" |
| Model Selection Criteria | MTEB/BEIR "can shortlist candidates" | no verification date | time-sensitive | Preserved — proposal rejected: claim is about benchmark design (aggregate rank mixes tasks), not standings | No change; MTEB/BEIR are cited in Embedding & Index Evaluation; MMTEB not added unverified |
| Multimodal Handling | "Current research increasingly uses…" | undated landscape claim | time-sensitive | Improved | Generalized (not verified): research includes these directions; test them; rankings stay workload-specific |
| Late Interaction Models | ColBERT and descendants as examples | named systems | time-sensitive | Preserved | Already framed as examples with arXiv link |
| Contextual Retrieval | Vendor blog as primary reference | no date | time-sensitive | Improved | Title and date checked: "Introducing Contextual Retrieval" (Anthropic post, September 2024), marked as a vendor report |
| BM25 | Personal-page PDF link | link-rot risk, no authors | time-sensitive | Improved | PDF opened; added "(Robertson & Zaragoza, 2009)" |
| Normalization | "equals exactly 1.0" | — | durable | Preserved | Mathematically exact |

## Retrieval Pipeline

| Note | Claim (short) | Issue | Class | Status | What changed |
|---|---|---|---|---|---|
| Sparse Retrieval | "Instant Real-Time Indexing … in microseconds" | unsourced, wrong for most engines | measured | Improved | Label "Cheap Incremental Indexing"; no embedding inference needed; visibility depends on refresh/commit settings (proposal left the bold label) |
| Multi-Query Retrieval | "Short, Vague Queries (1–3 words)" | word-count threshold | hypothesis | Improved | Vague queries where a baseline run shows missed evidence |
| Multi-Query Retrieval | Q3 "Sick leave policy" for a PTO query | example drifts intent | durable | Improved | "Time-off request process" |
| Query Expansion | "Vague / 1-Word Queries: Use Multi-Query" | prescriptive, not baseline-first | hypothesis | Improved | "candidate for … compare against the original query first" |
| Query Expansion | "Overly Specific Niche Queries: Use Step-Back" | conflicts with Step-Back's own gating | hypothesis | Improved | Specific queries also needing general policy; only after a baseline shows the miss |
| Query Expansion | Decomposition listed as an expansion archetype | ownership mismatch | durable | Improved | Decision line links [[Query Decomposition]] as a sibling owned by Query Transformation; diagram kept |
| Query Expansion | Heading "The 3 Expansion Archetypes" | arbitrary count | durable | Preserved — proposal rejected: cosmetic count, not a contradiction; headings kept stable | No change |
| MMR | "often returns 5 nearly identical chunks" | unmeasured frequency | hypothesis | Improved | "can return several nearly identical chunks" |
| MMR | λ=0 "selects completely unrelated chunks" | overstated (pool is still retrieved) | durable | Improved | Ignores relevance; picks the pool candidate least similar to those selected |
| MMR | "ensures diverse grievances are captured" | MMR cannot guarantee coverage | durable | Improved | "reduces the chance that near-duplicates crowd out distinct ones" |
| Self-Query | Query "after January 2025" | — | durable | Preserved | Query text kept; mismatch fixed in the filter (next row) |
| Self-Query | Filter `$gt 2025-01-01` | boundary contradicts "after January 2025" | durable | Improved | `$gte 2025-02-01` |
| Filtered Retrieval | pgvector filtering behavior | library behavior, no source | time-sensitive | Improved | README opened (verified 2026-10): post-scan filtering, iterative scans from 0.8.0, partial indexes, partitioning; link added |
| Query Understanding | BRIGHT warning, link title | undated; title wrong | time-sensitive | Improved | Exact title fixed (arXiv checked), "(2024; standings change …)" |
| Query Rewriting | Warranty "8 years or 100k miles" | real vendor terms, vary by trim | time-sensitive | Improved | "a set number of years or miles, whichever comes first" |

## Generation Pipeline

| Note | Claim (short) | Issue | Class | Status | What changed |
|---|---|---|---|---|---|
| Few-shot & In-Context Learning | "1–2 minimal format pairs" as best practice | count as rule | hypothesis | Improved — proposal modified | Count kept as a starting point; add more only if held-out format errors persist (proposal deleted the number) |
| Few-shot & In-Context Learning | "Show 1 Bad vs 1 Good Output" | count as rule | hypothesis | Improved | Start with one pair; confirm filler drops and bad example is not imitated |
| Few-shot & In-Context Learning | "2–3 boundary edge case examples" | count as rule | hypothesis | Improved — proposal modified | Count kept as starting point tied to observed confusions; add one at a time |
| Few-shot & In-Context Learning | Demonstrations "clutter working memory" | asserted mechanism | hypothesis | Improved | Consume budget and may distract; compare against concise ones |
| Few-shot & In-Context Learning | "When using models with test-time reasoning" | model-dependent | time-sensitive | Preserved — proposal rejected: section already frames anchoring as a hypothesis and makes zero-shot the baseline | No change |
| Few-shot & In-Context Learning | Column "Why Few-Shot Wins" / "Best Practice" | overclaim | durable | Improved | "Why Few-Shot Helps" / "Starting Point (confirm on held-out cases)" |
| Model Selection & Reasoning Tiers | "a few hundred representative labels" | unsourced threshold | hypothesis | Improved — proposal modified | Kept as a cheap starting assumption confirmed by a learning curve |
| Model Selection & Reasoning Tiers | "2026 'decision model' or 'System One' APIs" | unverifiable product names | time-sensitive | Removed deliberately | Names could not be traced to a primary source and would date quickly; replaced with "hosted zero-shot classifier products … category names are marketing labels" |
| Model Selection & Reasoning Tiers | Supervised baseline "often wins" | unsourced comparison | measured | Improved | "often" kept; "confirm with a held-out comparison" added |
| Model Selection & Reasoning Tiers | Classifier "with no output-parsing failures" | absolute | hypothesis | Improved | "typically … without free-text parsing failures" |
| Model Selection & Reasoning Tiers | Extraction "may regress under deliberation" | — | hypothesis | Preserved | Already hedged |
| Model Selection & Reasoning Tiers | Specialized checker "parity does not transfer" | depends on Hallucination note | measured | Preserved | Fixed at origin (next row) |
| Hallucination Detection & Verification | Small checkers approach model judges "at a fraction of the cost" | unsourced result | measured | Improved | Cites MiniCheck (arXiv 2404.10774, abstract checked): GPT-4-level accuracy on its grounding benchmark with a much smaller model; "400x" not imported |
| Context Formatting & Ordering | "Long-context models can still show position effects" | source tested older models | time-sensitive | Improved | "(Lost in the Middle measured them on 2023-era models; re-test on yours)" |

## RAG Architectures and RAG Production

| Note | Claim (short) | Issue | Class | Status | What changed |
|---|---|---|---|---|---|
| RAG Architectures | Self-RAG named without link | missing citation | durable | Improved | Link to arXiv 2310.11511 (opened; title confirmed) |
| Production Security, Privacy & Tenant Isolation | OWASP vector/embedding URL | versioned list entry | time-sensitive | Improved | "(LLM08:2025; the list is revised periodically, verified 2026-10)" — page opened |
| Production Observability & Incident Response | OpenInference adds AI semantic conventions | landscape | time-sensitive | Preserved — proposal rejected: already hedged ("convention maturity … not universal guarantees"); not re-fetched, so a date stamp would be unearned | No change |

## Evaluation

| Note | Claim (short) | Issue | Class | Status | What changed |
|---|---|---|---|---|---|
| Evaluation Frameworks & Tooling | Snapshot "checked in August 2026" | stale stamp | time-sensitive | Preserved — proposal rejected: only the OpenAI dates were rechecked, so restamping the whole snapshot to 2026-10 would be unearned | August 2026 stamp kept |
| Evaluation Frameworks & Tooling | OpenAI Evals read-only Oct 31 / shutdown Nov 30, 2026 | imminent dates | time-sensitive | Improved | Docs opened 2026-10-11; dates confirmed; phrased to read correctly after Oct 31; points to deprecations page |
| Evaluation Frameworks & Tooling | "As of this snapshot:" product list | no per-product date | time-sensitive | Improved | "(August 2026; individual product descriptions not rechecked since)" |
| Evaluation Frameworks & Tooling | OTel GenAI conventions "moved into their own project" | unsourced status | time-sensitive | Improved | Generalized: conventions have been evolving; check current status before relying on attribute names |
| Evaluation Data & Benchmarks | Ragas testset-generation docs URL | drift-prone | time-sensitive | Improved | Page opened ("Testset Generation for RAG"); "(page checked 2026-10)" |
| Judge Calibration & Validation | "Research through August 2026 continues to support…" | undated landscape framing | time-sensitive | Improved | All four ACL Anthology links opened; one-clause topic per paper; "(links verified 2026-10)" |
| Judge Calibration & Validation | SAJA link | — | time-sensitive | Preserved | Title confirmed; covered by row above |
| Statistical Decision-Making for Evaluation | Rule of three 3/n | — | durable | Preserved | Standard approximation, already caveated |

## Cross-folder resolutions

| Topic | Finding | Resolution |
|---|---|---|
| Flat-search cutoff | Vector Index ("<10k", "hundreds of ms at 1M") contradicted Flat Index ("not at a universal vector-count boundary"). Nothing in other folders. | Flat Index is the owner; Vector Index aligned and links it |
| HNSW/IVF complexity and memory | IVF "2x RAM overhead", "10M+" conflicted with Vector Index's "graph overhead depends on parameters". | Vector Index matrix and HNSW note are authoritative; IVF aligned to "measure both" |
| Chunk size/overlap defaults | Only numbers were in Semantic and Late Chunking ("3,000-token", "8k+"). Chunking and Chunking Strategy say size and overlap are experimental variables. No other folder states defaults. | Outliers removed (rows above) |
| Semantic-chunking threshold direction | Only described in Semantic Chunking; internal contradiction. | Fixed to "rises above" |
| RRF k | RRF and Hybrid Fusion both treat k as tunable and cite Cormack; no hardcoded k=60 anywhere. | Consistent; no change |
| MMR λ | MMR and Diversity Selection both say tune on development cases; no default elsewhere. | Consistent; no change |
| Top-k defaults | Only illustrative "Top 5" (Multi-Query diagram) and an explicit K=20 example (Evaluation Metrics). | Consistent; no change |
| Score/abstention thresholds | No numeric thresholds in any folder (broad regex including bare `0.x` values). | Consistent; no change |
| Hybrid as default | BM25, Hybrid Fusion, Retrieval & Metadata Evaluation and SKILL.md all treat hybrid as an empirical option. | Consistent; no change |
| Hash choice | Only Metadata Extraction mentions a hash; diagram (MD5/SHA) contradicted its own sha256 payload. | Aligned to SHA-256 |
| Embedding-migration procedure | Four places. The owner `Indexing Lifecycle & Migrations` was the only one missing dual-processing of live changes during backfill and identity/ACL reconciliation. RAG Production Lifecycle said "dual-write" where the others say "dual-process". | Owner gained both steps. RAG Production Lifecycle, Production Evaluation Gates & Release Engineering, and Production Caching & Vector DB Ops now point to it, and Lifecycle uses "dual-process live changes". Other wording left as is |
| Dated "through <month>" stamps | Two: Judge Calibration ("through August 2026") and Evaluation Frameworks ("checked in August 2026"). | Judge Calibration re-verified and restamped; Frameworks kept with honest scope (rows above) |
| Agreement/kappa cutoffs | Judge Calibration describes kappa variants and limitations; no numeric bands anywhere. | Consistent; no change |
| Pass percentages / zero-failure gates | Only the rule of three (Statistical Decision-Making) and qualitative pass-rate remarks (Agent System Evaluation); Release Engineering gates by slice with uncertainty. | Consistent; no change |
| Cache discounts, TTLs, semantic-cache thresholds | Contextual Retrieval, Prompt Caching & Compression, Production Caching & Vector DB Ops all refuse durable percentages; no TTL or similarity numbers. | Consistent; no change |
| Evidence at both edges of context | Only Context Formatting & Ordering, which rejects a universal rule. | Consistent; no change |
| Few-shot exemplar counts elsewhere | Query Rewriting, Query Routing, Query Transformation & Routing Evaluation and Prompt Construction give no counts; they version exemplar sets. | Consistent; no change |
| Router size ("start with two routes") | Adaptive & Composite Retrieval ties two routes to measured slices; Query Routing and Routing Evaluation are baseline-first. | Compatible (stated starting point plus measurement); no change |
| "Evidence-token ratio" definition | Used in Chunking, Chunking Evaluation, Reranking Evaluation, Retrieval & Metadata Evaluation, Contextual Compression and Context Assembly but defined nowhere. | Defined once in Chunking Evaluation (tokens inside labeled evidence regions ÷ all retrieved tokens), which owns region labels |
| Named benchmarks/frameworks | MTEB/BEIR (Model Selection Criteria, Embedding & Index Evaluation, Retrieval & Metadata Evaluation), BRIGHT, ViDoRe, Ragas et al. | Citations agree; BRIGHT title corrected; no standings claims remain |

## Riskiest changes for review

1. **IVF `nlist` guidance.** Before: "$\sqrt{N}$ or $4\sqrt{N}$" under "Typical Production Values". After: FAISS guidance, $4\sqrt{N}$ to $16\sqrt{N}$ below ~1M vectors, 30–256 training vectors per centroid (verified 2026-10), under "Starting Point (tune on your data)". The number changed, not just the hedge.
2. **Proposition-based Chunking example.** Before: source sentence "…Ronald Wayne in Cupertino, Apple developed…" with five propositions, including "Apple was founded in Cupertino, California." After: location removed from the sentence and the proposition, leaving four propositions.
3. **Vector Index size cutoffs.** Before: "At 1,000,000 vectors, search takes hundreds of milliseconds…" and "Best for <10k vectors" / "Small datasets (<10k vectors)". After: the point where exhaustive search fails latency/throughput targets is found by measurement (see Flat Index); "Small collections".
4. **IVF vs HNSW memory rule.** Before: "When you have 10M+ vectors and cannot afford the 2x RAM overhead of HNSW graphs." After: "When the collection is large enough that HNSW graph memory is unaffordable; measure memory and recall for both … rather than assuming a fixed overhead or size cutoff."
5. **Agentic Chunking benefit.** Before: "Highest semantic coherence on irregular documents (~87% accuracy on clinical benchmarks)". After: "Can place more coherent boundaries on irregular documents (a hypothesis to confirm: compare … against a recursive baseline on your own labeled regions)".
6. **Semantic Chunking threshold direction.** Before: "When the distance drops below a statistical percentile threshold…". After: "When the distance rises above a statistical percentile threshold…". This reverses the stated mechanism.
7. **Late Chunking applicability.** Before: "Long documents (8k+ tokens): Yes" and "Requires long-context embedding model (8k+)". After: long, context-dependent documents within the model's input limit (longer ones need overlapping macro-chunks); "document length is capped by its input limit".
8. **Model Selection & Reasoning Tiers product references (Removed deliberately).** Before: "Products in this class (e.g. 2026 'decision model' or 'System One' APIs) change quickly". After: "Hosted zero-shot classifier products change quickly and their category names are marketing labels". The named product terms are removed.
