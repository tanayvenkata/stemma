"""
FDA Guidance Diff Pipeline

Semantic document comparison using BM25 alignment + LLM classification.

Pipeline:
1. Parse PDFs → Extract text
2. Chunk with parent_child strategy
3. Align chunks using BM25 (find matches across versions)
4. Classify changes (NEW, REMOVED, STRICTER, etc.)
5. Generate diff report
"""

import os
import json
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
import numpy as np
from dotenv import load_dotenv
from rank_bm25 import BM25Okapi
from openai import OpenAI

import sys
sys.path.insert(0, str(Path(__file__).parent))
from chunking_strategies import FDAChunker, Chunk

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "google/gemini-2.5-flash")

# Alignment thresholds (BM25 scores vary by corpus, these are relative)
MATCH_THRESHOLD = 15.0  # Above this = likely match
NO_MATCH_THRESHOLD = 5.0  # Below this = no match


def tokenize(text: str) -> list[str]:
    """Simple tokenizer for BM25"""
    tokens = re.findall(r'\b[a-z0-9]+\b', text.lower())
    return [t for t in tokens if len(t) > 2]


@dataclass
class ChunkMatch:
    """A matched pair of chunks across versions"""
    old_chunk: Optional[Chunk]
    new_chunk: Optional[Chunk]
    score: float
    match_type: str  # "matched", "new", "removed"


@dataclass
class ClassifiedChange:
    """A classified change between document versions"""
    match: ChunkMatch
    change_type: str  # NEW_REQUIREMENT, REMOVED, STRICTER, etc.
    summary: str
    impact: str  # HIGH, MEDIUM, LOW
    confidence: float = 0.0


class BM25Index:
    """BM25 index for chunk retrieval"""

    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        self.chunk_ids = [c.chunk_id for c in chunks]
        self.texts = [c.text for c in chunks]
        self.tokenized = [tokenize(text) for text in self.texts]
        self.bm25 = BM25Okapi(self.tokenized)

    def search(self, query: str, k: int = 5) -> list[tuple[Chunk, float]]:
        """Search for matching chunks"""
        query_tokens = tokenize(query)
        scores = self.bm25.get_scores(query_tokens)
        top_indices = np.argsort(scores)[::-1][:k]
        return [(self.chunks[i], float(scores[i])) for i in top_indices]

    def search_by_chunk(self, chunk: Chunk, k: int = 3) -> list[tuple[Chunk, float]]:
        """Find best matches for a chunk"""
        return self.search(chunk.text, k=k)


# Change taxonomy for matched pairs (both old and new content exist)
# REMOVED and NEW_REQUIREMENT are NOT valid here - those are determined by matching, not LLM
MATCHED_TAXONOMY = """
CHANGE TYPES (for content that exists in both versions):
- STRICTER: Same topic, but requirements are now more stringent
- MORE_LENIENT: Same topic, but requirements are now less stringent
- CLARIFICATION: Same meaning, but clearer language
- RESTRUCTURED: Content moved/reorganized, not substantively changed
- EDITORIAL: Cosmetic changes only, no regulatory impact
- EXPANDED: Same topic, significantly more detail added
"""

CLASSIFICATION_PROMPT = """You are analyzing changes between two versions of an FDA regulatory guidance document.

These two passages were matched as covering similar regulatory topics. Your job is to classify HOW the content changed.

{taxonomy}

OLD VERSION (2014):
"{old_text}"

NEW VERSION (2025):
"{new_text}"

Classify this change into exactly ONE category from the list above. Since both passages exist, this is NOT a removal or addition - focus on how the requirements evolved.

Respond in JSON format only:
{{
  "change_type": "TYPE_HERE",
  "summary": "One sentence describing what changed",
  "impact": "HIGH/MEDIUM/LOW"
}}"""


class DiffPipeline:
    """Main pipeline for semantic document comparison"""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.llm_client = None

    def _log(self, msg: str):
        if self.verbose:
            print(msg)

    def _init_llm(self):
        if self.llm_client is None:
            self.llm_client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=OPENROUTER_API_KEY,
            )

    def chunk_document(self, pdf_path: Path, doc_id: str, doc_version: str) -> list[Chunk]:
        """Chunk a document using parent_child strategy"""
        self._log(f"Chunking {doc_id}...")
        chunker = FDAChunker(pdf_path, doc_id, doc_version)
        chunks = chunker.chunk_parent_child()
        self._log(f"  → {len(chunks)} chunks")
        return chunks

    def align_chunks(
        self,
        old_chunks: list[Chunk],
        new_chunks: list[Chunk]
    ) -> list[ChunkMatch]:
        """
        Align chunks across document versions using BM25.

        Strategy:
        1. For each new chunk, find best match in old doc
        2. Deduplicate: each old chunk can only be matched ONCE (keep highest score)
        3. Unmatched old chunks = removed content
        4. New chunks that lost their match = new content
        """
        self._log("Aligning chunks with BM25...")

        # Build index of old chunks
        old_index = BM25Index(old_chunks)

        # Phase 1: Find best old match for each new chunk
        # Track: old_chunk_id → (new_chunk, score) - keep only the best match per old chunk
        best_match_per_old: dict[str, tuple[Chunk, float]] = {}
        new_chunks_without_match: list[Chunk] = []

        for new_chunk in new_chunks:
            results = old_index.search_by_chunk(new_chunk, k=1)

            if not results:
                new_chunks_without_match.append(new_chunk)
                continue

            best_old, score = results[0]

            if score < NO_MATCH_THRESHOLD:
                # No meaningful match - this is new content
                new_chunks_without_match.append(new_chunk)
            elif best_old.chunk_id in best_match_per_old:
                # This old chunk was already matched - keep the better match
                existing_new, existing_score = best_match_per_old[best_old.chunk_id]
                if score > existing_score:
                    # New match is better - swap
                    best_match_per_old[best_old.chunk_id] = (new_chunk, score)
                    new_chunks_without_match.append(existing_new)  # Old winner becomes unmatched
                else:
                    # Existing match is better - current new chunk is unmatched
                    new_chunks_without_match.append(new_chunk)
            else:
                # First match for this old chunk
                best_match_per_old[best_old.chunk_id] = (new_chunk, score)

        # Phase 2: Build match list from deduplicated results
        matches = []
        matched_old_ids = set()

        # Add all deduplicated matches
        for old_chunk in old_chunks:
            if old_chunk.chunk_id in best_match_per_old:
                new_chunk, score = best_match_per_old[old_chunk.chunk_id]
                matches.append(ChunkMatch(
                    old_chunk=old_chunk,
                    new_chunk=new_chunk,
                    score=score,
                    match_type="matched"
                ))
                matched_old_ids.add(old_chunk.chunk_id)

        # Add new content (unmatched new chunks)
        for new_chunk in new_chunks_without_match:
            matches.append(ChunkMatch(
                old_chunk=None,
                new_chunk=new_chunk,
                score=0.0,
                match_type="new"
            ))

        # Phase 3: Find removed content (old chunks with no match)
        for old_chunk in old_chunks:
            if old_chunk.chunk_id not in matched_old_ids:
                matches.append(ChunkMatch(
                    old_chunk=old_chunk,
                    new_chunk=None,
                    score=0.0,
                    match_type="removed"
                ))

        # Summary
        matched = sum(1 for m in matches if m.match_type == "matched")
        new = sum(1 for m in matches if m.match_type == "new")
        removed = sum(1 for m in matches if m.match_type == "removed")
        self._log(f"  → {matched} matched, {new} new, {removed} removed")

        return matches

    def _call_llm(self, prompt: str) -> dict:
        """Call LLM and parse JSON response"""
        self._init_llm()

        response = self.llm_client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )

        content = response.choices[0].message.content

        # Parse JSON
        try:
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            return json.loads(content.strip())
        except (json.JSONDecodeError, IndexError):
            return {"error": "parse_failed", "raw": content}

    def classify_change(self, match: ChunkMatch) -> ClassifiedChange:
        """Classify a single change using LLM"""

        # Handle new content (no LLM needed)
        if match.match_type == "new":
            return ClassifiedChange(
                match=match,
                change_type="NEW_REQUIREMENT",
                summary=f"New content: {match.new_chunk.heading}",
                impact="HIGH",
                confidence=0.95
            )

        # Handle removed content (no LLM needed)
        if match.match_type == "removed":
            return ClassifiedChange(
                match=match,
                change_type="REMOVED",
                summary=f"Removed: {match.old_chunk.heading}",
                impact="HIGH",
                confidence=0.95
            )

        # For matched content, use LLM to classify the change type
        # IMPORTANT: Only allow valid types for matched pairs (not REMOVED or NEW_REQUIREMENT)
        valid_matched_types = {"STRICTER", "MORE_LENIENT", "CLARIFICATION", "RESTRUCTURED", "EDITORIAL", "EXPANDED"}

        old_text = match.old_chunk.text[:2000]
        new_text = match.new_chunk.text[:2000]

        prompt = CLASSIFICATION_PROMPT.format(
            taxonomy=MATCHED_TAXONOMY,
            old_text=old_text,
            new_text=new_text
        )

        result = self._call_llm(prompt)

        if "error" in result:
            return ClassifiedChange(
                match=match,
                change_type="UNKNOWN",
                summary="Classification failed",
                impact="UNKNOWN",
                confidence=0.0
            )

        # Validate and fix invalid responses
        change_type = result.get("change_type", "UNKNOWN")
        if change_type not in valid_matched_types:
            # LLM returned invalid type (e.g., REMOVED) - default to RESTRUCTURED
            change_type = "RESTRUCTURED"

        return ClassifiedChange(
            match=match,
            change_type=change_type,
            summary=result.get("summary", ""),
            impact=result.get("impact", "MEDIUM"),
            confidence=0.85
        )

    def classify_all_changes(self, matches: list[ChunkMatch]) -> list[ClassifiedChange]:
        """Classify all changes"""
        self._log("Classifying changes...")

        classified = []
        total = len(matches)

        for i, match in enumerate(matches):
            if self.verbose and (i + 1) % 5 == 0:
                print(f"  [{i+1}/{total}]...")
            classified.append(self.classify_change(match))

        self._log(f"  → {len(classified)} changes classified")
        return classified

    def generate_report(self, changes: list[ClassifiedChange], output_path: Optional[Path] = None) -> dict:
        """Generate a structured diff report"""

        report = {
            "summary": {
                "total_changes": len(changes),
                "by_type": {},
                "by_impact": {"HIGH": 0, "MEDIUM": 0, "LOW": 0},
            },
            "changes": []
        }

        # Count by type and impact
        for change in changes:
            ct = change.change_type
            report["summary"]["by_type"][ct] = report["summary"]["by_type"].get(ct, 0) + 1

            if change.impact in report["summary"]["by_impact"]:
                report["summary"]["by_impact"][change.impact] += 1

        # Add change details
        for change in changes:
            detail = {
                "change_type": change.change_type,
                "summary": change.summary,
                "impact": change.impact,
                "bm25_score": change.match.score,
                "match_type": change.match.match_type,
            }

            if change.match.old_chunk:
                detail["old_section"] = {
                    "heading": change.match.old_chunk.heading,
                    "hierarchy": change.match.old_chunk.section_hierarchy,
                    "pages": change.match.old_chunk.pages,
                    "preview": change.match.old_chunk.text[:300] + "..."
                }

            if change.match.new_chunk:
                detail["new_section"] = {
                    "heading": change.match.new_chunk.heading,
                    "hierarchy": change.match.new_chunk.section_hierarchy,
                    "pages": change.match.new_chunk.pages,
                    "preview": change.match.new_chunk.text[:300] + "..."
                }

            report["changes"].append(detail)

        # Sort: HIGH impact first, then by type
        impact_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        report["changes"].sort(key=lambda x: (
            impact_order.get(x["impact"], 3),
            x["change_type"]
        ))

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                json.dump(report, f, indent=2)
            self._log(f"Report saved to: {output_path}")

        return report

    def run(
        self,
        old_pdf: Path,
        new_pdf: Path,
        old_doc_id: str,
        new_doc_id: str,
        output_path: Optional[Path] = None
    ) -> dict:
        """Run the full diff pipeline"""

        self._log("=" * 60)
        self._log("FDA Guidance Diff Pipeline")
        self._log("=" * 60)
        self._log(f"Old: {old_pdf.name}")
        self._log(f"New: {new_pdf.name}")
        self._log("")

        # Step 1: Chunk documents
        old_chunks = self.chunk_document(old_pdf, old_doc_id, "2014")
        new_chunks = self.chunk_document(new_pdf, new_doc_id, "2025")

        # Step 2: Align chunks
        matches = self.align_chunks(old_chunks, new_chunks)

        # Step 3: Classify changes
        changes = self.classify_all_changes(matches)

        # Step 4: Generate report
        report = self.generate_report(changes, output_path)

        # Print summary
        self._log("")
        self._log("=" * 60)
        self._log("SUMMARY")
        self._log("=" * 60)
        self._log(f"Total changes: {report['summary']['total_changes']}")
        self._log(f"By type: {report['summary']['by_type']}")
        self._log(f"By impact: {report['summary']['by_impact']}")

        return report


def main():
    """Run diff on cybersecurity guidance documents"""

    pipeline = DiffPipeline(verbose=True)

    report = pipeline.run(
        old_pdf=Path("data/raw/cybersecurity_2014.pdf"),
        new_pdf=Path("data/raw/cybersecurity_2023.pdf"),
        old_doc_id="cybersecurity_2014",
        new_doc_id="cybersecurity_2025",
        output_path=Path("data/output/cybersecurity_diff.json")
    )

    # Print high-impact changes
    print("\n" + "=" * 60)
    print("HIGH IMPACT CHANGES")
    print("=" * 60)

    for change in report["changes"]:
        if change["impact"] == "HIGH":
            section = change.get("new_section", change.get("old_section", {}))
            heading = section.get("heading", "Unknown")
            print(f"\n[{change['change_type']}] {heading}")
            print(f"  {change['summary']}")


if __name__ == "__main__":
    main()
