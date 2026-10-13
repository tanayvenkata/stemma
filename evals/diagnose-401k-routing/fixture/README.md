# 401(k) RAG Advisor

Ask questions about your 401(k) plan in plain English.

This is a weekend project I built to get hands-on experience with RAG (Retrieval-Augmented Generation). It combines document search with structured data queries to answer questions about retirement plans—everything from "When do I become vested?" to "What fund has the lowest fees?"

## What It Does

The system handles three types of questions:

| Type | What it answers | How it works |
|------|-----------------|--------------|
| **Plan Rules** | Vesting, contributions, withdrawals, eligibility | Searches your plan documents (PDFs) |
| **Fund Data** | Fees, returns, fund comparisons | Queries structured fund data (SQL) |
| **Combined** | "I'm 30, which target-date fund should I pick?" | Uses both, merges the answer |

### Example Session

```
You: How much can I contribute to my 401k?

Bot: For 2024, you can contribute up to $23,000 in pre-tax or Roth
deferrals. If you're 50 or older, you can add a $7,500 catch-up
contribution for a total of $30,500. Your plan also allows after-tax
contributions up to the IRS limit of $69,000 total.

You: What's the cheapest index fund?

Bot: The Government Money Market fund has the lowest expense ratio at
0.002%. For equity exposure, the Large Cap Stock Index fund is 0.01%.

You: sources

[Showing sources for future answers]

You: I'm 35 and moderately aggressive. What fund should I pick?

Bot: Based on your age, target retirement around 2054, the LifePath 2055
fund would be appropriate. It's currently 94% stocks / 6% bonds and has
an expense ratio of 0.11%.

Sources:
- funds.csv: LifePath 2055 fund data
- SPD.pdf (page 42): Target-date fund descriptions
```

## Quick Start

### Option 1: Local LLM (Free, Private)

Requires [LM Studio](https://lmstudio.ai/) running locally.

```bash
# Clone and setup
git clone https://github.com/tanayvenkata/401k-rag.git
cd 401k-rag
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Configure for local LLM
cp .env.example .env
# (default settings use local LM Studio)

# Start LM Studio, load a model (I used qwen3-4b), start the server

# Index the sample documents
python src/indexer.py

# Start asking questions
python src/interactive_rag.py
```

### Option 2: Cloud LLM (OpenRouter)

```bash
# Same setup steps, then edit .env:
LLM_BACKEND=openrouter
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

## Using Your Own 401(k) Plan

The real value is using this with your actual plan documents.

### Step 1: Add Your Documents

Put your 401(k) PDFs in the `docs/` folder:

```
docs/
├── SPD.pdf              # Summary Plan Description
├── fee_disclosure.pdf   # Fee disclosure notice
├── fund_prospectus.pdf  # Fund details
└── enrollment.pdf       # Enrollment forms
```

### Step 2: Update Fund Data

Edit `data/funds.csv` with your plan's investment options:

```csv
name,category,type,fee,ytd,1yr,3yr,5yr,10yr,target_year,stocks,bonds
Large Cap Index,equity,index,0.01,12.5,15.2,8.1,10.3,11.2,,,
LifePath 2055,target_date,target_date,0.11,18.2,22.1,9.8,12.1,,2055,94,6
Stable Value,fixed_income,stable_value,0.25,4.2,4.5,3.8,3.2,2.8,,0,100
```

### Step 3: Reindex

```bash
# Clear old index and rebuild
rm -rf data/chroma
python src/indexer.py
```

### Step 4: Test It

```bash
python src/interactive_rag.py
```

## Architecture

```
Question → Classifier → Dispatcher
                          ├── RAG Pipeline (document search)
                          ├── Fund Pipeline (text-to-SQL)
                          └── Hybrid (both merged)
```

### Core Components

| File | Purpose |
|------|---------|
| `classifier.py` | Routes questions to the right pipeline |
| `dispatcher.py` | Orchestrates pipelines, handles fallbacks |
| `retriever.py` | ChromaDB vector search + query enhancement |
| `fund_sql.py` | Converts natural language to SQL |
| `indexer.py` | Chunks PDFs and creates embeddings |
| `evaluate.py` | LLM-as-judge evaluation framework |
| `interactive_rag.py` | Terminal interface |

### Interesting Design Decisions

**Two-tier classification**: Instead of calling the LLM for every query, the classifier first checks against 70+ keyword patterns. This handles ~80% of questions instantly. The LLM only kicks in for ambiguous cases.

```python
# Fast path: keyword matching
fund_patterns = ["expense ratio", "fee", "return", "lifepath", "target date"]
rag_patterns = ["contribution", "vesting", "withdrawal", "eligible"]

# Slow path: LLM classification (only if confidence < 70%)
```

**Domain term injection**: Before searching the vector database, the system asks the LLM to add relevant 401(k) vocabulary to the query. This bridges the gap between how users ask questions and how plan documents are written.

```
User query: "Can I buy stocks directly?"
Enhanced:   "Can I buy stocks directly? company stock SDA self-directed brokerage window"
```

**Graceful fallbacks**: If SQL generation fails (malformed query, no results), the system falls back to RAG search. If classification is uncertain, it defaults to RAG. The user always gets an answer.

**Error-as-data**: Database queries return `(result, error)` tuples instead of throwing exceptions. This makes error handling explicit and composable.

## Evaluation

I built a golden set of 8 intentionally challenging test cases to stress-test the system:

| Metric | Score |
|--------|-------|
| Pass Rate | 62% (5/8) |
| Avg LLM-Judge Score | 3.6/5 |
| Avg Fact Coverage | ~70% |

**Context**: The system works well for typical interactive use. The golden set specifically tests edge cases—hybrid questions requiring multiple sources, nuanced policy interpretations, and complex fund comparisons. There's room to improve, and I'm incorporating what I learned into future projects.

Run the evaluation yourself:

```bash
python src/evaluate.py
```

### Creating Your Own Test Cases

Edit `data/golden_set_v4.json`:

```json
{
  "tests": [
    {
      "id": 1,
      "question": "When do I become vested?",
      "pipeline": "rag",
      "key_facts": [
        "Your contributions are always 100% vested",
        "Company match requires 3 years of service"
      ],
      "expected_answer_summary": "Employee contributions vest immediately, company match vests after 3 years."
    }
  ]
}
```

## Project Structure

```
401k/
├── src/
│   ├── classifier.py       # Query routing (keyword + LLM)
│   ├── dispatcher.py       # Pipeline orchestration
│   ├── retriever.py        # ChromaDB search
│   ├── fund_sql.py         # Text-to-SQL
│   ├── indexer.py          # PDF processing
│   ├── evaluate.py         # Evaluation framework
│   └── interactive_rag.py  # CLI interface
│
├── data/
│   ├── funds.csv           # Fund data (28 funds in sample)
│   ├── golden_set_v4.json  # Test cases
│   └── chroma/             # Vector store (auto-generated)
│
├── docs/                   # Your PDFs go here (gitignored)
├── .env.example            # Environment template
└── requirements.txt        # Dependencies
```

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
# LLM Backend: "local" (LM Studio) or "openrouter"
LLM_BACKEND=local

# For OpenRouter
OPENROUTER_API_KEY=sk-or-v1-your-key

# Model selection (optional)
LLM_MODEL=qwen/qwen3-4b-2507
```

## Commands Reference

```bash
# Interactive Q&A
python src/interactive_rag.py

# Index/reindex documents
python src/indexer.py

# Run evaluation
python src/evaluate.py

# Test individual components
python src/classifier.py    # Test query classification
python src/retriever.py     # Test document retrieval
python src/fund_sql.py      # Test SQL generation
```

---

*December 2025*
