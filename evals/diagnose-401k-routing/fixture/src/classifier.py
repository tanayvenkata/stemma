"""
Query Classifier - Route queries to RAG, Fund SQL, or Hybrid pipeline.

Uses keyword-based classification with LLM fallback for uncertain cases.
"""

import re
from dataclasses import dataclass
from typing import Literal

QueryType = Literal["rag", "fund", "hybrid"]


@dataclass
class ClassificationResult:
    """Result of query classification."""
    query_type: QueryType
    confidence: float  # 0.0 to 1.0
    method: str        # "keyword" or "llm"
    reasoning: str     # Why this classification


# =============================================================================
# KEYWORD PATTERNS
# =============================================================================

# Fund-related patterns (structured data queries)
FUND_SIGNALS = [
    # Fund names
    r"large cap", r"small cap", r"mid cap", r"lifepath", r"stable value",
    r"bond fund", r"money market", r"target date", r"index fund",
    r"growth fund", r"international", r"real estate",
    # Fund metrics
    r"expense ratio", r"fee", r"fees", r"cost",
    r"return", r"returns", r"performance",
    r"ytd", r"year return", r"10.year", r"5.year", r"3.year", r"1.year",
    # Comparisons and recommendations
    r"compare", r"vs\.?", r"versus", r"better", r"best",
    r"cheapest", r"lowest fee", r"highest return",
    r"which fund", r"what fund", r"recommend",
    # Target date / age-based
    r"i.m \d+ years? old", r"i am \d+", r"age \d+", r"retire",
    r"target year", r"2025|2030|2035|2040|2045|2050|2055|2060|2065|2070",
]

# RAG-related patterns (plan document queries)
RAG_SIGNALS = [
    # Plan rules
    r"contribution", r"contribute", r"limit", r"maximum", r"can i contribute",
    r"match", r"employer match", r"matching", r"vesting", r"vested",
    # Procedures
    r"how do i", r"how to", r"steps to", r"process for",
    r"withdraw", r"withdrawal", r"distribution", r"rollover", r"loan",
    r"hardship", r"penalty", r"early withdrawal",
    # Eligibility
    r"eligible", r"eligibility", r"qualify", r"requirement", r"enroll",
    # Documents/forms
    r"form", r"document", r"paperwork", r"application", r"beneficiary",
    # Plan info
    r"plan rules", r"what happens if", r"termination", r"leave",
    r"fired", r"quit", r"change job",
]

# Patterns that suggest hybrid (both fund data AND plan rules needed)
HYBRID_SIGNALS = [
    # Questions combining fund + plan concepts
    r"(fund|invest).*(contribution|match|limit|plan)",
    r"(contribution|match).*(fund|invest|put)",
    r"put.*(money|contribution).*(fund|stable|bond|stock)",
    r"options?.*(low.risk|conservative|safe|aggressive)",
    r"allocat.*(retirement|age|years)",
]


class QueryClassifier:
    """Classify 401(k) queries into RAG, Fund, or Hybrid pipelines."""

    def __init__(self, llm_fallback: bool = True):
        self.llm_fallback = llm_fallback
        self.confidence_threshold = 0.7

    def classify(self, question: str) -> ClassificationResult:
        """Classify a question, using keyword matching with optional LLM fallback."""
        # Try keyword classification first (fast)
        result = self._keyword_classify(question)

        if result.confidence >= self.confidence_threshold:
            return result

        # Fall back to LLM if uncertain and enabled
        if self.llm_fallback:
            return self._llm_classify(question)

        return result

    def _keyword_classify(self, question: str) -> ClassificationResult:
        """Fast keyword-based classification."""
        q_lower = question.lower()

        # Check for hybrid patterns first (they're more specific)
        for pattern in HYBRID_SIGNALS:
            if re.search(pattern, q_lower):
                return ClassificationResult(
                    query_type="hybrid",
                    confidence=0.8,
                    method="keyword",
                    reasoning=f"Matched hybrid pattern: {pattern}"
                )

        # Count signals for each type
        fund_matches = [p for p in FUND_SIGNALS if re.search(p, q_lower)]
        rag_matches = [p for p in RAG_SIGNALS if re.search(p, q_lower)]

        fund_score = len(fund_matches)
        rag_score = len(rag_matches)
        total = fund_score + rag_score

        if total == 0:
            return ClassificationResult(
                query_type="rag",  # Default to RAG
                confidence=0.4,
                method="keyword",
                reasoning="No clear signals found, defaulting to RAG"
            )

        # Determine type based on scores
        if fund_score > rag_score:
            confidence = min(fund_score / (total + 1), 0.9)
            return ClassificationResult(
                query_type="fund",
                confidence=confidence,
                method="keyword",
                reasoning=f"Fund signals ({fund_score}): {fund_matches[:3]}"
            )
        elif rag_score > fund_score:
            confidence = min(rag_score / (total + 1), 0.9)
            return ClassificationResult(
                query_type="rag",
                confidence=confidence,
                method="keyword",
                reasoning=f"RAG signals ({rag_score}): {rag_matches[:3]}"
            )
        else:
            # Equal scores - likely hybrid or ambiguous
            return ClassificationResult(
                query_type="hybrid",
                confidence=0.6,
                method="keyword",
                reasoning=f"Equal signals (fund={fund_score}, rag={rag_score}) - likely hybrid"
            )

    def _llm_classify(self, question: str) -> ClassificationResult:
        """LLM-based classification for uncertain cases."""
        # Import here to avoid circular dependency
        from unified_evaluator import classify_query

        query_type = classify_query(question)
        return ClassificationResult(
            query_type=query_type,
            confidence=0.85,
            method="llm",
            reasoning="Classified by LLM"
        )


def main():
    """Test the classifier with sample queries."""
    classifier = QueryClassifier(llm_fallback=False)  # Keyword only for testing

    test_queries = [
        # Fund queries
        ("What's the expense ratio for Large Cap Growth?", "fund"),
        ("Which fund has the best 10-year return?", "fund"),
        ("Compare the index funds", "fund"),
        ("I'm 30 years old, which LifePath fund?", "fund"),
        # RAG queries
        ("How much can I contribute to my 401k?", "rag"),
        ("What is the employer match formula?", "rag"),
        ("How do I take a hardship withdrawal?", "rag"),
        ("When am I fully vested?", "rag"),
        # Hybrid queries
        ("Should I put my contribution in the stable value fund?", "hybrid"),
        ("What fund options are good for a conservative investor?", "hybrid"),
    ]

    print("=" * 70)
    print("Query Classifier Test")
    print("=" * 70)

    for question, expected in test_queries:
        result = classifier.classify(question)
        status = "PASS" if result.query_type == expected else "FAIL"
        print(f"\n[{status}] {question}")
        print(f"       Expected: {expected}, Got: {result.query_type}")
        print(f"       Confidence: {result.confidence:.0%}, Method: {result.method}")
        print(f"       Reasoning: {result.reasoning[:60]}...")


if __name__ == "__main__":
    main()
