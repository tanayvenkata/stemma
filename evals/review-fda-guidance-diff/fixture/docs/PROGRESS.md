# Project Progress Summary

**Last updated:** 2026-01-10

---

## What This Project Is

**FDA Guidance Diff** - A semantic document comparison tool that detects, classifies, and visualizes meaningful changes between versions of FDA regulatory guidance documents.

**Input:** Two PDF versions of any FDA guidance
**Output:** Semantic diff (what changed, what type, what's new, what's gone)

---

## What We've Done

### Phase 1: Spikes (De-risking) ✅ COMPLETE

| Spike | Goal | Result |
|-------|------|--------|
| 1. PDF Extraction | Can we get clean text? | ✅ pymupdf works well |
| 2. Embedding Similarity | Can embeddings align content? | ✅ 0.784 mean similarity |
| 3. Alignment Validation | Would we catch real changes? | ✅ 5/5 documented changes detected |
| 4. Classification Prompt | Can LLM classify consistently? | ✅ Works, 100% valid JSON |

### Phase 2: Region Labeling ✅ COMPLETE

Created **stable region labels** as initial ground truth.

**Files created:**
- `data/regions/cybersecurity_2014_regions.json` - 18 regions
- `data/regions/cybersecurity_2025_regions.json` - 16 regions
- `data/eval/query_region_pairs.json` - 71 query-region pairs

### Phase 3: Chunking Evaluation ✅ COMPLETE

Tested 4 chunking strategies against 71 query-region pairs.

**Decision:** Use `parent_child` chunking strategy.

See `docs/chunking-strategy.md` for full details.

### Phase 4: Embedding Evaluation ✅ COMPLETE (REVISED)

**Round 1 (Region-Level Labels):** bge-large won
**Round 2 (Chunk-Level Labels):** bge-m3 won ← FINAL

| Model | MRR | Recall@10 | NDCG |
|-------|-----|-----------|------|
| **bge-m3** | **0.871** | **0.983** | **0.898** |
| bge-large-en-v1.5 | 0.832 | 0.966 | 0.866 |
| bge-base-en-v1.5 | 0.828 | 0.983 | 0.866 |
| all-MiniLM-L6-v2 | 0.790 | 0.931 | 0.825 |

**Decision:** Use `BAAI/bge-m3`

**Key Learning:** Precise chunk-level labels changed the winner. Label quality matters.

See `docs/embedding-strategy.md` for full details.

### Phase 5: Chunk-Level Labeling ✅ COMPLETE

Generated precise chunk-level ground truth using DIY + Gemini review.

**Files created:**
- `data/eval/chunk_queries_generated.json` - 122 synthetic queries
- `data/eval/chunk_queries_cleaned.json` - 116 queries after review
- `data/eval/query_review_report.md` - Gemini's review notes
- `data/eval/chunks_reference.json` - Chunk metadata for reference

### Phase 6: Retrieval Evaluation ✅ COMPLETE

Tested dense vs sparse (BM25) vs hybrid (RRF) with chunk-level labels.

| Strategy | MRR | Recall@10 | NDCG |
|----------|-----|-----------|------|
| dense | 0.871 | 0.983 | 0.898 |
| sparse_bm25 | 0.915 | 0.991 | 0.934 |
| **hybrid_rrf** | **0.926** | **0.991** | **0.943** |

**Decision:** Use `hybrid_rrf` (Reciprocal Rank Fusion)

**Key Finding:** BM25 is surprisingly strong for regulatory text (0.915 MRR). Hybrid adds small but consistent lift.

See `docs/retrieval-strategy.md` for full details.

### Phase 7: Full Diff Pipeline ✅ COMPLETE

Built end-to-end diff pipeline with BM25 alignment + LLM classification.

**Pipeline:** `src/diff_pipeline.py`
1. Parse PDFs with pymupdf
2. Chunk with parent_child strategy
3. Align chunks across versions using BM25
4. Classify changes with LLM (Gemini 2.5 Flash)
5. Generate structured JSON diff report

**Key fixes during development:**
1. **Taxonomy separation** - LLM can't classify matched pairs as "REMOVED" (logical impossibility)
2. **Deduplication** - Each old chunk matches to only ONE new chunk (best score wins)

### Phase 8: Ground Truth Validation ✅ COMPLETE

Validated pipeline against human-reviewed ground truth (King & Spalding law firm analyses).

| Doc Pair | Age Gap | Detection | Type Accuracy | Notes |
|----------|---------|-----------|---------------|-------|
| **Cybersecurity 2014→2023** | 9 years | **6/6 (100%)** | **6/6 (100%)** | Modern format, works great |
| **PCCP AI 2023→2024** | 1.5 years | **9/10 (90%)** | **9/9 (100%)** | Modern format, draft→final |
| **Software Premarket 2005→2023** | 18 years | **3/4 (75%)** | **2/3 (67%)** | Old format, stress test |

**Cybersecurity ground truth (all detected):**
- SPDF (Secure Product Development Framework) ✅
- SBOM (Software Bill of Materials) ✅
- Cybersecurity-specific labeling ✅
- Vulnerability management plans ✅
- AI/ML and cloud in scope ✅
- IDE submission appendix ✅

**PCCP AI ground truth (9/10 detected):**
- AI/ML → AI terminology change ✅
- Training, tuning, testing data categories ✅
- Submission types (PMA, 510k, De Novo) ✅
- Labeling requirements ✅
- Version control section (V.F) ✅
- Automatic implementation support ✅
- Update frequency recommendation ✅
- Combination products ✅
- UDI requirements ✅
- Rollback plans ❌ (not surfaced in summary)

**Software Premarket ground truth (3/4 detected):**
- Level of Concern → Documentation Level ✅
- IEC 62304 alignment ❌ (content captured but not highlighted in summary)
- AI/ML requirements ✅
- SDS for both levels ⚠️ (detected, wrong type)

**Key insights:**
- Modern FDA docs (post-2010): 90-100% detection, 100% type accuracy
- Old format docs (pre-2010): 75% detection - still useful but harder
- Draft→Final comparisons work well (similar structure)

### Design Decision: Boilerplate Exclusions

The chunker excludes common FDA boilerplate from section detection:
- "Contains Nonbinding Recommendations" (page header)
- "Food and Drug Administration" (cover page)
- "Center for Devices and Radiological Health" (org name)
- etc.

**Why this is NOT overfitting:**
- These strings appear in ALL FDA guidance documents, not just our test pairs
- It's domain knowledge (like knowing "Page X of Y" isn't a section header)
- Contrast with overfitting: tuning BM25 threshold to 17.3 for one specific doc

**Why this is honest:**
- Software 2005 results (75%) show limitations on old formats
- We report both strong (Cybersecurity) and weaker (Software) results
- The boilerplate list would help ANY FDA document, not just these pairs

---

## Locked Decisions

| Component | Decision | Doc |
|-----------|----------|-----|
| PDF extraction | pymupdf | - |
| Chunking | parent_child + fallback patterns | `docs/chunking-strategy.md` |
| Alignment | BM25 (not embeddings) | `docs/retrieval-strategy.md` |
| Classification | Gemini 2.5 Flash | `.env` |
| Thresholds | MATCH=15.0, NO_MATCH=5.0 | `src/diff_pipeline.py` |

---

## What's Next

### Future: Demo/Frontend

- Pre-compute results for both doc pairs
- Build simple frontend to display diffs
- Side-by-side view with change highlighting

### Future: Additional Validation

- Find third FDA guidance pair with law firm analysis
- Test on non-cybersecurity/non-software domain

---

## File Structure

```
fda-guidance-diff/
├── .env                  # API keys + config (gitignored)
├── .env.example          # Template
├── CLAUDE.md             # Project context
├── venv/                 # Python environment
│
├── data/
│   ├── raw/              # Downloaded PDFs
│   │   ├── cybersecurity_2014.pdf
│   │   ├── cybersecurity_2023.pdf
│   │   ├── pccp_ai_2023_draft.pdf
│   │   ├── pccp_ai_2024_final.pdf
│   │   ├── software_premarket_2005.pdf
│   │   └── software_premarket_2023.pdf
│   ├── regions/          # Region labels (kept for reference)
│   ├── eval/             # Evaluation data
│   │   ├── query_region_pairs.json
│   │   ├── chunk_queries_cleaned.json
│   │   └── retrieval_eval_chunklevel_results.json
│   └── output/           # Generated diff reports
│       ├── cybersecurity_diff.json
│       ├── pccp_ai_diff.json
│       └── software_premarket_diff.json
│
├── docs/
│   ├── PROGRESS.md           # This file
│   ├── chunking-strategy.md
│   ├── embedding-strategy.md
│   └── retrieval-strategy.md
│
├── src/
│   ├── diff_pipeline.py          # Main pipeline
│   ├── chunking_strategies.py    # Chunking with fallback patterns
│   ├── embedding_eval_chunklevel.py
│   ├── retrieval_eval_chunklevel.py
│   ├── generate_chunk_queries.py
│   └── embedding_viz.py
│
└── spikes/               # Spike test results
```

---

## Config

All in `.env`:
```
OPENROUTER_API_KEY=sk-or-v1-...
LLM_MODEL=google/gemini-2.5-flash
EMBEDDING_MODEL=BAAI/bge-m3
```
