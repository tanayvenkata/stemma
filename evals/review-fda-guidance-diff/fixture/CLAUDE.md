# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

FDA Guidance Diff - semantic document comparison for FDA regulatory guidance PDFs. Takes two PDF versions, outputs classified diffs (what changed, what type, what's new, what's gone).

**Key differentiator:** Classifies change types (STRICTER, MORE_LENIENT, CLARIFICATION, etc.) rather than just showing text diffs.

## Commands

```bash
# Setup
python -m venv venv && source venv/bin/activate
pip install pymupdf rank-bm25 openai python-dotenv numpy

# Run diff pipeline
python src/diff_pipeline.py

# Run chunking strategies comparison
python src/chunking_strategies.py

# Run retrieval evaluation
python src/retrieval_eval_chunklevel.py
```

## Architecture

```
PDF → FDAChunker (parent_child strategy) → Chunks
                                              ↓
Old chunks + New chunks → BM25Index.align_chunks() → ChunkMatches
                                                          ↓
ChunkMatches → LLM classification → ClassifiedChanges → JSON report
```

**Core pipeline:** `src/diff_pipeline.py`
- `DiffPipeline.run()` - entry point, orchestrates full flow
- `BM25Index` - sparse retrieval for chunk alignment
- `classify_change()` - LLM classification (Gemini 2.5 Flash via OpenRouter)

**Chunking:** `src/chunking_strategies.py`
- `FDAChunker` - PDF parsing + section detection with regex patterns
- `chunk_parent_child()` - production strategy (level 1 = parent, level 2 = child)
- Fallback patterns for pre-2010 docs without numbered sections

## Locked Technical Decisions

| Component | Choice | Rationale |
|-----------|--------|-----------|
| PDF extraction | pymupdf (fitz) | Best structure preservation |
| Chunking | parent_child | Won eval (preserves hierarchy) |
| Alignment | BM25 (not embeddings) | 0.915 MRR, simpler, faster |
| LLM | Gemini 2.5 Flash | Via OpenRouter |
| Thresholds | MATCH=15.0, NO_MATCH=5.0 | Validated on ground truth |

## Change Taxonomy

For matched pairs (LLM classifies):
- STRICTER / MORE_LENIENT - requirement intensity changed
- CLARIFICATION - same meaning, clearer language
- RESTRUCTURED - moved/reorganized
- EDITORIAL - cosmetic only
- EXPANDED - more detail added

Determined by alignment (no LLM):
- NEW_REQUIREMENT - content in new doc only
- REMOVED - content in old doc only

## Data Files

- `data/raw/*.pdf` - source PDFs (3 doc pairs)
- `data/eval/chunk_queries_cleaned.json` - 116 labeled queries for eval
- `data/output/*_diff.json` - generated diff reports

## Ground Truth Sources

Law firm analyses for validation:
- King & Spalding cybersecurity analysis
- King & Spalding software premarket analysis
- Innolitics HTML transcriptions (section-by-section)

## Config

`.env` file (see `.env.example`):
```
OPENROUTER_API_KEY=sk-or-v1-...
LLM_MODEL=google/gemini-2.5-flash
EMBEDDING_MODEL=BAAI/bge-m3
```

## Demo Site (Portfolio)

Interactive demo at `demo/` - Astro 5 static site showcasing pre-computed diff results.

```bash
cd demo
npm install
npm run dev      # Dev server at localhost:4321
npm run build    # Build to dist/
npm run preview  # Preview build
```

**Structure:**
- `demo/src/pages/index.astro` - Main page
- `demo/src/components/DiffViewer.astro` - Tab switching, filters, stats
- `demo/src/components/ChangeCard.astro` - Individual change display
- `demo/src/data/diffs.ts` - Transforms JSON → component format (deduplication, preview cleanup)

**Data flow:** `data/output/*_diff.json` → copied to `demo/src/data/` → transformed at build time

**Design tokens:** Stone palette only (bg #FAFAF9, text #1C1917, borders #E7E5E4), Instrument Serif headings, Geist body

## Known Limitations

- Old format docs (pre-2010): ~75% detection vs 90-100% for modern docs
- Boilerplate exclusions in `_find_sections()` are FDA-specific domain knowledge
- Demo preview text may have PDF artifacts (cleaned at build time via `cleanPreview()`)
