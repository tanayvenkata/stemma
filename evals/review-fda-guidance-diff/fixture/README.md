# FDA Guidance Diff

Semantic comparison tool for FDA regulatory guidance documents. Unlike raw text diffs, this classifies *how* requirements changed—stricter, clarified, expanded—so regulatory teams know what matters.

![Demo Screenshot](docs/demo-screenshot.png)

## What It Does

- **Input:** Two PDF versions of an FDA guidance document
- **Output:** Classified diff with change types (NEW, REMOVED, STRICTER, EXPANDED, CLARIFICATION, etc.)
- **Validated:** 90-100% accuracy on modern docs against law firm analyses

## Pre-computed Comparisons

| Document | Years | Changes | High Impact |
|----------|-------|---------|-------------|
| Cybersecurity in Medical Devices | 2014 → 2023 | 45 | 43 |
| AI/ML: Predetermined Change Control Plans | 2023 → 2024 | 28 | 8 |
| Software: Content of Premarket Submissions | 2005 → 2023 | 49 | 47 |

## How It Works

1. **Chunk & Parse** - PDFs parsed with pymupdf, split into semantic chunks using FDA section patterns
2. **Align with BM25** - Sparse retrieval matches chunks across versions (0.915 MRR)
3. **Classify with LLM** - Matched pairs classified by Gemini 2.5 Flash into change types

## Quick Start

```bash
# Backend (Python)
python -m venv venv && source venv/bin/activate
pip install pymupdf rank-bm25 openai python-dotenv numpy
cp .env.example .env  # Add your OpenRouter API key
python src/diff_pipeline.py

# Demo site (Astro)
cd demo && npm install && npm run dev
```

## Change Taxonomy

| Type | Meaning |
|------|---------|
| NEW | Content only in newer document |
| REMOVED | Content only in older document |
| STRICTER | Requirements more stringent |
| MORE_LENIENT | Requirements less stringent |
| EXPANDED | Same topic, more detail added |
| CLARIFICATION | Same meaning, clearer language |
| RESTRUCTURED | Content moved/reorganized |
| EDITORIAL | Cosmetic changes only |

## Architecture

```
PDF → FDAChunker → Chunks
                      ↓
Old + New chunks → BM25 alignment → Matches
                                       ↓
Matches → LLM classification → JSON report
```

## License

MIT
