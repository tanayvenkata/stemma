"""
RAG Evaluator v4 - LLM-as-Judge evaluation with proper scoring.

Evaluates generated answers against verified expected answers using:
1. LLM-as-Judge for semantic correctness (primary)
2. Key fact coverage (secondary)
3. Overall pipeline diagnosis

Run: python src/eval_v4.py
"""

import json
import requests
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent.parent / "data"
GOLDEN_PATH = DATA_DIR / "golden_set_v4.json"
MODEL = "qwen/qwen3-4b-2507"


@dataclass
class EvalResult:
    """Evaluation result for a single question."""
    id: int
    question: str
    pipeline: str

    # Generated output
    generated_answer: str

    # Scores
    llm_judge_score: int  # 1-5
    llm_judge_reasoning: str
    key_facts_found: list = field(default_factory=list)
    key_facts_missing: list = field(default_factory=list)
    fact_coverage: float = 0.0

    # Final
    passed: bool = False


def call_llm(prompt: str, max_tokens: int = 500) -> str:
    """Call local LLM."""
    try:
        response = requests.post(
            "http://127.0.0.1:1234/v1/chat/completions",
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": max_tokens
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[LLM Error: {e}]"


def generate_answer(question: str, pipeline: str) -> str:
    """Generate answer using the full pipeline."""
    from dispatcher import UnifiedDispatcher

    dispatcher = UnifiedDispatcher(verbose=False)
    result = dispatcher.ask(question)
    return result.answer


def llm_judge(question: str, expected_summary: str, generated_answer: str, key_facts: list) -> tuple[int, str]:
    """Use LLM to judge answer quality."""

    facts_list = "\n".join(f"  - {f}" for f in key_facts)

    prompt = f"""You are evaluating a 401(k) advisor chatbot's answer.

QUESTION: {question}

EXPECTED ANSWER (verified from documents):
{expected_summary}

KEY FACTS THAT SHOULD BE MENTIONED:
{facts_list}

GENERATED ANSWER:
{generated_answer}

---
Rate the generated answer on a scale of 1-5:

5 = EXCELLENT: Covers all key facts, accurate, well-explained
4 = GOOD: Covers most key facts, minor omissions or imprecision
3 = PARTIAL: Gets the main point but misses important details
2 = POOR: Some relevant info but significant errors or omissions
1 = FAIL: Wrong, irrelevant, or completely misses the point

Consider:
- Does it answer the actual question asked?
- Are the key facts present (even if worded differently)?
- Is it accurate (no hallucinations or wrong info)?
- Would this be helpful to an employee?

Respond in this exact format:
SCORE: [1-5]
REASONING: [2-3 sentences explaining your rating]"""

    response = call_llm(prompt, max_tokens=200)

    # Parse response
    score = 3  # default
    reasoning = response

    for line in response.split("\n"):
        if line.strip().startswith("SCORE:"):
            try:
                score = int(line.split(":")[1].strip()[0])
                score = max(1, min(5, score))  # clamp 1-5
            except:
                pass
        elif line.strip().startswith("REASONING:"):
            reasoning = line.split(":", 1)[1].strip()

    return score, reasoning


def check_key_facts(answer: str, key_facts: list) -> tuple[list, list]:
    """Check which key facts appear in the answer (fuzzy matching via LLM)."""

    found = []
    missing = []

    for fact in key_facts:
        # Use LLM to check if the fact is present (handles paraphrasing)
        prompt = f"""Does this answer mention or convey this fact? Answer only YES or NO.

FACT: {fact}

ANSWER: {answer[:1000]}

The fact can be paraphrased or stated differently.
Answer YES if the meaning is conveyed, NO if it's missing."""

        response = call_llm(prompt, max_tokens=10)

        if "YES" in response.upper():
            found.append(fact)
        else:
            missing.append(fact)

    return found, missing


def run_evaluation():
    """Run full evaluation on golden set v4."""

    with open(GOLDEN_PATH) as f:
        golden = json.load(f)

    print("=" * 80)
    print("RAG EVALUATION v4 - LLM-as-Judge")
    print("=" * 80)
    print(f"Model: {MODEL}")
    print(f"Golden set: {GOLDEN_PATH.name}")
    print(f"Tests: {len(golden['tests'])}")
    print("=" * 80)

    results = []

    for test in golden["tests"]:
        print(f"\n{'─' * 80}")
        print(f"#{test['id']}: {test['question']}")
        print(f"Pipeline: {test['pipeline']}")
        print("─" * 80)

        # Generate answer
        print("Generating answer...")
        answer = generate_answer(test["question"], test["pipeline"])
        print(f"Answer: {answer[:200]}...")

        # LLM Judge scoring
        print("\nLLM Judge evaluating...")
        score, reasoning = llm_judge(
            test["question"],
            test["expected_answer_summary"],
            answer,
            test["key_facts"]
        )
        print(f"Score: {score}/5")
        print(f"Reasoning: {reasoning}")

        # Key fact coverage
        print("\nChecking key facts...")
        found, missing = check_key_facts(answer, test["key_facts"])
        coverage = len(found) / len(test["key_facts"]) if test["key_facts"] else 1.0
        print(f"Facts found: {len(found)}/{len(test['key_facts'])} ({coverage:.0%})")
        if missing:
            print(f"Missing: {missing[:3]}...")

        # Determine pass/fail
        passed = score >= 4  # 4 or 5 = pass

        result = EvalResult(
            id=test["id"],
            question=test["question"],
            pipeline=test["pipeline"],
            generated_answer=answer,
            llm_judge_score=score,
            llm_judge_reasoning=reasoning,
            key_facts_found=found,
            key_facts_missing=missing,
            fact_coverage=coverage,
            passed=passed
        )
        results.append(result)

        print(f"\n{'✓ PASS' if passed else '✗ FAIL'}")

    # Summary
    print("\n" + "=" * 80)
    print("EVALUATION SUMMARY")
    print("=" * 80)

    passed = sum(1 for r in results if r.passed)
    total = len(results)
    avg_score = sum(r.llm_judge_score for r in results) / total
    avg_coverage = sum(r.fact_coverage for r in results) / total

    print(f"""
┌────────────────────────────────────────────────────────────────────────────┐
│  METRIC                    │  SCORE                                        │
├────────────────────────────┼───────────────────────────────────────────────┤
│  Pass Rate (score >= 4)    │  {passed}/{total} ({100*passed//total}%)                                    │
│  Average LLM Judge Score   │  {avg_score:.1f}/5                                         │
│  Average Fact Coverage     │  {avg_coverage:.0%}                                           │
└────────────────────────────┴───────────────────────────────────────────────┘
""")

    # Per-question breakdown
    print("\nPER-QUESTION BREAKDOWN:")
    print("─" * 80)

    for r in results:
        status = "✓" if r.passed else "✗"
        bar = "█" * r.llm_judge_score + "░" * (5 - r.llm_judge_score)
        print(f"{status} #{r.id} [{r.pipeline:6}] {bar} {r.llm_judge_score}/5  {r.question[:40]}...")

    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "model": MODEL,
        "summary": {
            "pass_rate": passed / total,
            "avg_score": avg_score,
            "avg_fact_coverage": avg_coverage
        },
        "results": [
            {
                "id": r.id,
                "question": r.question,
                "score": r.llm_judge_score,
                "reasoning": r.llm_judge_reasoning,
                "fact_coverage": r.fact_coverage,
                "passed": r.passed
            }
            for r in results
        ]
    }

    output_path = DATA_DIR / f"eval_v4_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: {output_path}")

    return results


if __name__ == "__main__":
    run_evaluation()
