"""
Fund SQL Pipeline - Text-to-SQL for structured fund data.

Two-step approach:
1. LLM generates SQL from natural language question
2. Execute SQL, LLM generates answer from results
"""

import sqlite3
import csv
import json
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = Path(__file__).parent.parent / "data" / "funds.csv"
GOLDEN_PATH = Path(__file__).parent.parent / "data" / "fund_golden_set.json"
MODEL = "qwen/qwen3-4b-2507"

# =============================================================================
# PROMPT 1: SQL Generation
# =============================================================================
SQL_PROMPT = """You are a SQL expert. Write a SQLite query to answer the user's question about 401(k) funds.

TABLE SCHEMA:
Table: funds
Columns:
  - name (text): Fund name (e.g., "Large Cap Growth", "LifePath 2055")
  - category (text): money_market, bond, equity, international, target_date, stable_value, real_estate
  - type (text): index, active, target_date, money_market, stable_value
  - fee (real): Expense ratio as percentage (0.01 means 0.01%, 0.35 means 0.35%)
  - ytd, "1yr", "3yr", "5yr", "10yr" (real): Return percentages, can be NULL
  - target_year (integer): For LifePath funds (2025, 2030, ... 2070), NULL for others
  - stocks, bonds (real): Allocation percentages for LifePath funds

RULES:
1. Return ONLY the SQL query - no explanation, no markdown code blocks
2. ALWAYS include the "name" column in SELECT so we know which fund the data is for
3. Keep queries simple - one SELECT statement, avoid complex subqueries
4. Column names with numbers need double quotes: "1yr", "10yr"
5. For comparing funds, use: WHERE name IN ('Fund A', 'Fund B')
6. For advisory questions, fetch ALL relevant rows so the answer step can reason
7. For age-based target date questions: retirement age is 65, calculate target_year = 2024 + (65 - age).
   Get the nearest fund by ordering by ABS(target_year - calculated_year) LIMIT 1, or better: fetch ALL LifePath funds so the answer step can recommend the closest one.
   Example: 22 year old → 2024 + 43 = 2067 → fetch all LifePath funds, answer step recommends LifePath 2065 or 2070

EXAMPLES:

Q: What's the fee for Large Cap Growth?
SELECT name, fee FROM funds WHERE name = 'Large Cap Growth';

Q: Compare Large Cap Growth vs Large Cap Stock Index
SELECT name, type, fee, "5yr", "10yr" FROM funds WHERE name IN ('Large Cap Growth', 'Large Cap Stock Index');

Q: Which funds are index funds?
SELECT name, category, fee, "10yr" FROM funds WHERE type = 'index';

Q: What's the average fee for index vs active funds?
SELECT type, AVG(fee) as avg_fee, COUNT(*) as count FROM funds WHERE type IN ('index', 'active') GROUP BY type;

Q: Show me all LifePath funds
SELECT name, target_year, stocks, bonds, fee FROM funds WHERE category = 'target_date' ORDER BY target_year;

Q: I'm 22 years old, what LifePath fund should I pick?
SELECT name, target_year, stocks, bonds, fee FROM funds WHERE category = 'target_date' ORDER BY target_year;

Now write SQL for this question:
Q: {question}
"""

# =============================================================================
# PROMPT 2: Answer Generation
# =============================================================================
ANSWER_PROMPT = """You are a helpful 401(k) advisor. Answer the user's question using ONLY the data provided below.

RULES:
1. Be specific - cite actual numbers from the data (fees, returns, fund names)
2. If asked for a recommendation, give a clear answer with reasoning
3. Keep your answer concise (2-3 sentences for simple questions, 1 paragraph for complex)
4. If the data doesn't contain what's needed to answer, say so clearly
5. For target-date fund recommendations based on age: assume retirement at 65. Calculate target_year = 2024 + (65 - age). Round to nearest available fund (2030, 2035...2065, 2070). Example: age 22 → 2024 + 43 = 2067 → recommend LifePath 2065 or 2070
6. LifePath funds with higher target years have MORE stocks (higher risk). If user has low risk tolerance but young age, suggest a blended approach: mostly age-appropriate LifePath for growth plus Stable Value or Government Money Market for stability.

DATA:
{data}

QUESTION: {question}

ANSWER:"""


def create_db() -> sqlite3.Connection:
    """Load fund CSV into in-memory SQLite database."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE funds (
            name TEXT, category TEXT, type TEXT, fee REAL,
            ytd REAL, "1yr" REAL, "3yr" REAL, "5yr" REAL, "10yr" REAL,
            target_year INTEGER, stocks REAL, bonds REAL
        )
    """)
    with open(CSV_PATH) as f:
        for row in csv.DictReader(f):
            cursor.execute(
                "INSERT INTO funds VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    row["name"], row["category"], row["type"],
                    float(row["fee"]) if row["fee"] else None,
                    float(row["ytd"]) if row["ytd"] else None,
                    float(row["1yr"]) if row["1yr"] else None,
                    float(row["3yr"]) if row["3yr"] else None,
                    float(row["5yr"]) if row["5yr"] else None,
                    float(row["10yr"]) if row["10yr"] else None,
                    int(row["target_year"]) if row["target_year"] else None,
                    float(row["stocks"]) if row["stocks"] else None,
                    float(row["bonds"]) if row["bonds"] else None,
                )
            )
    conn.commit()
    return conn


def call_llm(prompt: str, max_tokens: int = 400) -> str:
    """Call local LLM via LM Studio."""
    response = requests.post(
        "http://127.0.0.1:1234/v1/chat/completions",
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": max_tokens
        },
        timeout=60
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def generate_sql(question: str) -> str:
    """Generate SQL from natural language question."""
    prompt = SQL_PROMPT.format(question=question)
    sql = call_llm(prompt, max_tokens=250)

    # Light cleanup
    sql = sql.strip()
    sql = sql.replace('"', '"').replace('"', '"')  # Fix smart quotes
    sql = sql.replace(''', "'").replace(''', "'")

    # Remove markdown code blocks if model added them despite instructions
    if sql.startswith("```"):
        lines = sql.split("\n")
        sql = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
    if sql.endswith("```"):
        sql = sql[:-3].strip()
    if sql.lower().startswith("sql"):
        sql = sql[3:].strip()

    return sql


def execute_sql(conn: sqlite3.Connection, sql: str) -> tuple[str, list[dict], str | None]:
    """Execute SQL and return (formatted_table, rows_as_dicts, error_or_none)."""
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        # Format as table
        lines = [" | ".join(columns)]
        for row in rows:
            lines.append(" | ".join(str(v) if v is not None else "N/A" for v in row))

        # Also return as dicts for checking
        rows_dicts = [dict(zip(columns, row)) for row in rows]

        return "\n".join(lines), rows_dicts, None
    except Exception as e:
        return "", [], str(e)


def generate_answer(question: str, data: str) -> str:
    """Generate natural language answer from SQL results."""
    prompt = ANSWER_PROMPT.format(data=data, question=question)
    return call_llm(prompt, max_tokens=350)


def ask(question: str, conn: sqlite3.Connection, verbose: bool = True) -> dict:
    """Full pipeline: question -> SQL -> execute -> answer."""
    result = {"question": question}

    # Step 1: Generate SQL
    sql = generate_sql(question)
    result["sql"] = sql
    if verbose:
        print(f"SQL: {sql}")

    # Step 2: Execute SQL
    data, rows, error = execute_sql(conn, sql)
    result["sql_error"] = error
    result["row_count"] = len(rows)

    if error:
        result["answer"] = f"SQL Error: {error}"
        if verbose:
            print(f"Error: {error}")
        return result

    if verbose:
        preview = data[:300] + "..." if len(data) > 300 else data
        print(f"Data ({len(rows)} rows):\n{preview}")

    # Step 3: Generate answer
    answer = generate_answer(question, data)
    result["answer"] = answer
    if verbose:
        print(f"Answer: {answer}")

    return result


def run_golden_set(conn: sqlite3.Connection) -> dict:
    """Run all golden set tests and return results."""
    with open(GOLDEN_PATH) as f:
        golden = json.load(f)

    results = {
        "timestamp": datetime.now().isoformat(),
        "model": MODEL,
        "prompts": {
            "sql_prompt_preview": SQL_PROMPT[:500] + "...",
            "answer_prompt_preview": ANSWER_PROMPT[:300] + "..."
        },
        "total": len(golden["tests"]),
        "passed": 0,
        "failed": 0,
        "tests": []
    }

    for test in golden["tests"]:
        print(f"\n{'='*70}")
        print(f"#{test['id']} [{test['pattern']}]: {test['question']}")
        print("="*70)

        result = ask(test["question"], conn, verbose=True)
        result["id"] = test["id"]
        result["pattern"] = test["pattern"]
        result["expected"] = test["expected_result_contains"]

        # Check if expected values are in the answer
        answer_lower = result["answer"].lower()
        found = [exp for exp in test["expected_result_contains"] if exp.lower() in answer_lower]
        missing = [exp for exp in test["expected_result_contains"] if exp.lower() not in answer_lower]

        result["found"] = found
        result["missing"] = missing
        result["passed"] = len(missing) == 0

        if result["passed"]:
            results["passed"] += 1
            print(f"\n✅ PASSED - Found: {found}")
        else:
            results["failed"] += 1
            print(f"\n❌ FAILED - Missing: {missing}")

        results["tests"].append(result)

    return results


def main():
    """Run golden set evaluation and save results."""
    print("="*70)
    print("FUND SQL PIPELINE - Golden Set Evaluation")
    print("="*70)
    print(f"Model: {MODEL}")
    print(f"Golden set: {GOLDEN_PATH}")

    print("\nLoading database...")
    conn = create_db()

    results = run_golden_set(conn)

    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print("="*70)
    print(f"Passed: {results['passed']}/{results['total']}")
    print(f"Failed: {results['failed']}/{results['total']}")

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(__file__).parent.parent / "data" / f"fund_eval_{timestamp}.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {output_path}")

    return results


if __name__ == "__main__":
    main()
