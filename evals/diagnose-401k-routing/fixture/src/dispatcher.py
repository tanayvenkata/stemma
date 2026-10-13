"""
Unified Dispatcher - Routes queries to RAG, Fund SQL, or both pipelines.

Entry point for all 401(k) queries with automatic pipeline selection.
"""

import requests
from dataclasses import dataclass, field
from typing import Optional

from classifier import QueryClassifier, ClassificationResult
from retriever import Retriever, RetrievalResult


@dataclass
class DispatchResult:
    """Result from the unified dispatcher."""
    question: str
    classification: ClassificationResult
    answer: str

    # Pipeline-specific results
    rag_context: Optional[str] = None
    rag_sources: list = field(default_factory=list)
    fund_data: Optional[str] = None
    fund_sql: Optional[str] = None

    # Metadata
    pipelines_used: list = field(default_factory=list)


# =============================================================================
# PROMPTS
# =============================================================================

RAG_PROMPT = """You are a helpful 401(k) plan advisor. Answer the user's question using ONLY the context provided below.

RULES:
1. Base your answer ONLY on the provided context
2. If the context doesn't contain enough information, say so clearly
3. Be specific - cite numbers, percentages, and references when available
4. Keep your answer concise but complete

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""


FUND_PROMPT = """You are a helpful 401(k) advisor. Answer the user's question using ONLY the fund data provided below.

RULES:
1. Be specific - cite actual numbers from the data (fees, returns, fund names)
2. If asked for a recommendation, give a clear answer with reasoning
3. Keep your answer concise
4. If the data doesn't contain what's needed, say so clearly
5. For target-date fund recommendations based on age: assume retirement at 65. Calculate target_year = 2024 + (65 - age). Round to nearest available fund (2030...2070). Example: age 22 → 2024 + 43 = 2067 → recommend LifePath 2065 or 2070
6. LifePath funds with higher target years have MORE stocks (higher risk). If user has low risk tolerance but young age, suggest a blended approach: mostly age-appropriate LifePath for growth plus Stable Value or Government Money Market for stability.

DATA:
{data}

QUESTION: {question}

ANSWER:"""


HYBRID_PROMPT = """You are a helpful 401(k) plan advisor. Answer the user's question using the information from both sources below.

PLAN DOCUMENTS (rules, procedures, eligibility):
{rag_context}

FUND DATA (fees, returns, fund details):
{fund_data}

GUIDANCE:
- For target-date funds: age 22 → retirement ~2067 → recommend LifePath 2065 or 2070
- LifePath funds with higher years have MORE stocks (higher risk)
- For low risk tolerance with young age: suggest blended approach with mostly age-appropriate LifePath plus Stable Value for stability

Use both sources to give a comprehensive answer. Be specific and cite numbers when available.

QUESTION: {question}

ANSWER:"""


# =============================================================================
# DISPATCHER
# =============================================================================

class UnifiedDispatcher:
    """Routes queries to appropriate pipeline(s) and returns unified results."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.classifier = QueryClassifier(llm_fallback=True)
        self.retriever = Retriever()
        self._fund_db = None  # Lazy-loaded

    @property
    def fund_db(self):
        """Lazy-load fund database."""
        if self._fund_db is None:
            from fund_sql import create_db
            self._fund_db = create_db()
        return self._fund_db

    def ask(self, question: str) -> DispatchResult:
        """Route and answer a question using the appropriate pipeline(s)."""
        # Step 1: Classify the query
        try:
            classification = self.classifier.classify(question)
        except Exception as e:
            # Fall back to RAG on classification error
            if self.verbose:
                print(f"Classification error: {e}, defaulting to RAG")
            classification = ClassificationResult(
                query_type="rag",
                confidence=0.5,
                method="fallback",
                reasoning=f"Classification failed: {e}"
            )

        if self.verbose:
            print(f"[{classification.query_type.upper()}] "
                  f"confidence={classification.confidence:.0%} "
                  f"({classification.method})")

        # Step 2: Route to appropriate pipeline(s)
        result = DispatchResult(
            question=question,
            classification=classification,
            answer="",
            pipelines_used=[]
        )

        try:
            if classification.query_type == "rag":
                result = self._run_rag(question, result)
            elif classification.query_type == "fund":
                result = self._run_fund(question, result)
            elif classification.query_type == "hybrid":
                result = self._run_hybrid(question, result)
        except Exception as e:
            result.answer = f"Error processing query: {e}"
            if self.verbose:
                print(f"Pipeline error: {e}")

        return result

    def _run_rag(self, question: str, result: DispatchResult) -> DispatchResult:
        """Execute RAG pipeline."""
        result.pipelines_used = ["rag"]

        # Retrieve context
        retrieved = self.retriever.retrieve(question, top_k=5)
        result.rag_sources = [
            {"source": r.source, "page": r.page, "score": r.score}
            for r in retrieved
        ]
        result.rag_context = self.retriever.retrieve_with_context(question, top_k=5)

        if self.verbose:
            print(f"Retrieved {len(retrieved)} chunks")
            for r in retrieved[:3]:  # Show top 3
                print(f"  - {r.source} p.{r.page} (score: {r.score:.3f})")

        # Generate answer
        prompt = RAG_PROMPT.format(context=result.rag_context, question=question)
        result.answer = self._call_llm(prompt)

        return result

    def _run_fund(self, question: str, result: DispatchResult) -> DispatchResult:
        """Execute Fund SQL pipeline."""
        result.pipelines_used = ["fund"]

        from fund_sql import generate_sql, execute_sql

        # Generate and execute SQL
        sql = generate_sql(question)
        result.fund_sql = sql

        if self.verbose:
            print(f"SQL: {sql}")

        data, rows, error = execute_sql(self.fund_db, sql)

        if error:
            if self.verbose:
                print(f"SQL Error: {error}")
            # Try falling back to RAG
            if self.verbose:
                print("Falling back to RAG pipeline...")
            return self._run_rag(question, result)

        result.fund_data = data

        if self.verbose:
            print(f"Retrieved {len(rows)} rows")

        # Generate answer
        prompt = FUND_PROMPT.format(data=data, question=question)
        result.answer = self._call_llm(prompt)

        return result

    def _run_hybrid(self, question: str, result: DispatchResult) -> DispatchResult:
        """Execute both pipelines and merge results."""
        result.pipelines_used = ["rag", "fund"]

        # Step 1: Run RAG
        retrieved = self.retriever.retrieve(question, top_k=5)
        result.rag_sources = [
            {"source": r.source, "page": r.page, "score": r.score}
            for r in retrieved
        ]
        result.rag_context = self.retriever.retrieve_with_context(question, top_k=5)

        if self.verbose:
            print(f"RAG: Retrieved {len(retrieved)} chunks")

        # Step 2: Run Fund SQL
        from fund_sql import generate_sql, execute_sql

        sql = generate_sql(question)
        result.fund_sql = sql
        data, rows, error = execute_sql(self.fund_db, sql)

        if error:
            data = "[Fund data unavailable due to SQL error]"
            if self.verbose:
                print(f"Fund SQL error: {error}")
        else:
            if self.verbose:
                print(f"Fund: Retrieved {len(rows)} rows")

        result.fund_data = data

        # Step 3: Merge and generate unified answer
        prompt = HYBRID_PROMPT.format(
            rag_context=result.rag_context,
            fund_data=result.fund_data,
            question=question
        )
        result.answer = self._call_llm(prompt)

        return result

    def _call_llm(self, prompt: str) -> str:
        """Call LLM for answer generation."""
        try:
            response = requests.post(
                "http://127.0.0.1:1234/v1/chat/completions",
                json={
                    "model": "qwen/qwen3-4b-2507",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                    "max_tokens": 500
                },
                timeout=60
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"[LLM Error: {e}]"


def main():
    """Test the dispatcher with sample queries."""
    print("=" * 70)
    print("Unified Dispatcher Test")
    print("=" * 70)

    dispatcher = UnifiedDispatcher(verbose=True)

    test_queries = [
        "What's the expense ratio for Large Cap Index?",  # Fund
        "How much can I contribute to my 401k?",          # RAG
        "Which LifePath fund is right for someone age 30?", # Hybrid
    ]

    for question in test_queries:
        print(f"\n{'='*70}")
        print(f"Q: {question}")
        print("-" * 70)

        result = dispatcher.ask(question)

        print(f"\nPipelines: {result.pipelines_used}")
        print(f"Answer: {result.answer[:300]}...")


if __name__ == "__main__":
    main()
