"""
Retriever - Query ChromaDB and return relevant chunks.

Features:
- Semantic search with ChromaDB
- Smart domain injection: LLM picks relevant 401k terms to enhance queries
"""

import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
from dataclasses import dataclass
import requests

CHROMA_DIR = Path(__file__).parent.parent / "data" / "chroma"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Domain terms the LLM can choose from to enhance queries
DOMAIN_TERM_PROMPT = """Given this 401k question, pick 3-5 relevant search terms from this list that would help find the answer in plan documents.

IMPORTANT: If the question mentions a specific term from this list (like "intern", "SDA", "Roth"), always include it.

TERM LIST:
- company stock, employer stock, BNY stock
- self-directed account, SDA, brokerage window, minimum transfer, initial investment
- contribution, contribution limit, deferral, after-tax, pre-tax, Roth
- employer match, matching, company matching contributions
- vesting, vested, vesting service, years of service
- withdrawal, distribution, hardship
- loan, plan loan
- beneficiary, beneficiary designation
- rollover, transfer, in-plan conversion
- QDIA, default investment, LifePath, target-date
- eligibility, enrollment, eligible employees
- student intern, co-op employee, intern employee
- mega backdoor Roth, after-tax contributions, Roth conversion

Question: "{question}"

Return ONLY the relevant terms, comma-separated. No explanation:"""


@dataclass
class RetrievalResult:
    """A single retrieved chunk with metadata."""
    text: str
    source: str
    page: int
    score: float  # Distance (lower = more similar)


class Retriever:
    """Semantic search retriever with smart domain injection."""

    def __init__(self, collection_name: str = "401k_docs", enhance_queries: bool = True):
        self.client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL
        )
        self.collection = self.client.get_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )
        self.enhance_queries = enhance_queries

    def _enhance_query(self, query: str) -> str:
        """Use LLM to add relevant domain terms to the query."""
        try:
            response = requests.post(
                "http://127.0.0.1:1234/v1/chat/completions",
                json={
                    "model": "qwen/qwen3-4b-2507",
                    "messages": [{"role": "user", "content": DOMAIN_TERM_PROMPT.format(question=query)}],
                    "temperature": 0.2,
                    "max_tokens": 50
                },
                timeout=10
            )
            response.raise_for_status()
            terms = response.json()["choices"][0]["message"]["content"].strip()
            return f"{query} {terms}"
        except Exception:
            # If LLM fails, return original query
            return query

    def retrieve(self, query: str, top_k: int = 5, enhance: bool = None) -> list[RetrievalResult]:
        """Retrieve top_k most relevant chunks for query.

        Args:
            query: The search query
            top_k: Number of results to return
            enhance: Override instance-level enhance_queries setting
        """
        # Determine whether to enhance
        should_enhance = enhance if enhance is not None else self.enhance_queries

        # Enhance query with domain terms if enabled
        search_query = self._enhance_query(query) if should_enhance else query

        results = self.collection.query(
            query_texts=[search_query],
            n_results=top_k
        )

        # Parse results
        retrieved = []
        for i in range(len(results["documents"][0])):
            retrieved.append(RetrievalResult(
                text=results["documents"][0][i],
                source=results["metadatas"][0][i]["source"],
                page=results["metadatas"][0][i]["page"],
                score=results["distances"][0][i] if results["distances"] else 0.0
            ))

        return retrieved

    def retrieve_with_context(self, query: str, top_k: int = 5) -> str:
        """Retrieve and format as context string for LLM."""
        results = self.retrieve(query, top_k)

        context_parts = []
        for i, r in enumerate(results, 1):
            context_parts.append(
                f"[Source: {r.source}, Page {r.page}]\n{r.text}"
            )

        return "\n\n---\n\n".join(context_parts)


def main():
    """Test retrieval with and without enhancement."""
    print("="*70)
    print("Retriever Test - Smart Domain Injection")
    print("="*70)

    retriever = Retriever(enhance_queries=True)

    test_queries = [
        "Can I buy individual stocks in my 401k?",
        "How much can I contribute to my 401k?",
        "How do I change my beneficiary?",
    ]

    for query in test_queries:
        print(f"\n{'='*70}")
        print(f"Query: {query}")
        print("-"*50)

        # Show enhanced query
        enhanced = retriever._enhance_query(query)
        print(f"Enhanced: {enhanced}")
        print("-"*50)

        results = retriever.retrieve(query, top_k=3)
        for i, r in enumerate(results, 1):
            print(f"{i}. [{r.source}, p.{r.page}] (score: {r.score:.3f})")


if __name__ == "__main__":
    main()
