"""
Chunking Strategies for FDA Guidance Documents

Strategies to test:
1. document_aware - Split on section headers
2. document_aware_split - Split on headers, split large sections into paragraphs
3. parent_child - Index subsections, keep parent reference
4. fixed_512_baseline - Fixed size baseline
"""

import re
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import fitz


@dataclass
class Chunk:
    """A chunk of text with metadata"""
    chunk_id: str
    text: str
    doc_id: str
    doc_version: str
    pages: list[int]
    section_hierarchy: list[str]
    heading: str
    strategy: str
    parent_chunk_id: Optional[str] = None  # For parent-child strategy

    def to_dict(self) -> dict:
        return {
            "chunk_id": self.chunk_id,
            "text": self.text,
            "metadata": {
                "doc_id": self.doc_id,
                "doc_version": self.doc_version,
                "pages": self.pages,
                "section_hierarchy": self.section_hierarchy,
                "heading": self.heading,
                "strategy": self.strategy,
                "parent_chunk_id": self.parent_chunk_id
            }
        }


class FDAChunker:
    """Chunker for FDA guidance documents"""

    def __init__(self, pdf_path: Path, doc_id: str, doc_version: str):
        self.pdf_path = pdf_path
        self.doc_id = doc_id
        self.doc_version = doc_version
        self.full_text = ""
        self.page_offsets = []
        self._extract_text()

    def _extract_text(self):
        """Extract text with page tracking"""
        doc = fitz.open(self.pdf_path)
        offset = 0
        for page in doc:
            self.page_offsets.append(offset)
            text = page.get_text()
            self.full_text += text
            offset += len(text)
        self.page_offsets.append(offset)
        doc.close()

    def _get_pages_for_range(self, start: int, end: int) -> list[int]:
        """Get page numbers for a character range"""
        pages = []
        for i, offset in enumerate(self.page_offsets[:-1]):
            if offset < end and self.page_offsets[i + 1] > start:
                pages.append(i + 1)
        return pages

    def _find_sections(self) -> list[dict]:
        """Find all sections with their boundaries"""
        sections = []

        # Patterns for section headers (ordered by specificity)
        numbered_patterns = [
            (1, re.compile(r'^(I{1,3}|IV|V|VI{1,3}|VII|VIII|IX|X)\.\s+(.+)$', re.MULTILINE)),  # Roman
            (1, re.compile(r'^(\d+)\.\s+([A-Z][^.]{3,80})$', re.MULTILINE)),  # Arabic main
            (2, re.compile(r'^([A-Z])\.\s+([A-Z].{3,80})$', re.MULTILINE)),  # Letter subsection
        ]

        # Fallback for older docs without numbered sections (only used if numbered patterns find < 5 sections)
        fallback_pattern = (1, re.compile(r'^(([A-Z][a-z]+[-]?)+(?:\s+(?:[a-z]+\s+)?(?:[A-Z][a-z]+[-]?|of|for|to|and|the)+){0,6})\s*$', re.MULTILINE))

        # Common boilerplate to exclude from fallback matching
        boilerplate = {
            'contains nonbinding recommendations', 'food and drug administration',
            'center for devices', 'center for biologics', 'office of device',
            'office of in vitro', 'office of blood', 'guidance for industry',
            'public comment', 'additional copies', 'table of contents', 'preface',
            'contained in medical', 'guidance for the content', 'submissions for software',
            'premarket submissions', 'medical devices', 'draft guidance',
        }

        all_matches = []

        # First try numbered patterns
        for level, pattern in numbered_patterns:
            for match in pattern.finditer(self.full_text):
                # Skip table of contents (lines with dots or ending in page numbers)
                line = match.group(0)
                if '...' in line or re.search(r'\s\d+\s*$', line):
                    continue
                if len(line) > 120:  # Too long to be a header
                    continue

                # Handle patterns with marker+title (groups 1,2) vs title-only (group 1)
                try:
                    marker = match.group(1)
                    title = match.group(2).strip() if match.lastindex >= 2 else None
                except IndexError:
                    title = None

                if title:
                    # Numbered pattern: "I. Introduction" or "1. Overview"
                    heading = f"{marker}. {title}"
                else:
                    # Unnumbered fallback: "Introduction" (marker IS the title)
                    heading = marker.strip()
                    title = heading
                    marker = ""

                all_matches.append({
                    "level": level,
                    "marker": marker,
                    "title": title,
                    "start": match.start(),
                    "heading": heading
                })

        # If numbered patterns found too few sections, try fallback pattern
        if len(all_matches) < 5:
            level, pattern = fallback_pattern
            for match in pattern.finditer(self.full_text):
                line = match.group(0)
                if '...' in line or re.search(r'\s\d+\s*$', line):
                    continue
                if len(line) > 60:  # Stricter length limit for fallback
                    continue

                heading = match.group(1).strip()

                # Skip boilerplate text
                if any(bp in heading.lower() for bp in boilerplate):
                    continue

                all_matches.append({
                    "level": level,
                    "marker": "",
                    "title": heading,
                    "start": match.start(),
                    "heading": heading
                })

        # Sort by position
        all_matches.sort(key=lambda x: x["start"])

        # Calculate end positions
        for i, section in enumerate(all_matches):
            if i + 1 < len(all_matches):
                section["end"] = all_matches[i + 1]["start"]
            else:
                section["end"] = len(self.full_text)

            section["text"] = self.full_text[section["start"]:section["end"]]
            section["pages"] = self._get_pages_for_range(section["start"], section["end"])

        return all_matches

    def chunk_document_aware(self) -> list[Chunk]:
        """Strategy 1: Split on section headers only"""
        sections = self._find_sections()
        chunks = []
        hierarchy = []

        for i, section in enumerate(sections):
            # Update hierarchy
            if section["level"] == 1:
                hierarchy = [section["heading"]]
            elif section["level"] == 2:
                hierarchy = hierarchy[:1] + [section["heading"]]

            chunk = Chunk(
                chunk_id=f"{self.doc_id}_doc_aware_{i}",
                text=section["text"].strip(),
                doc_id=self.doc_id,
                doc_version=self.doc_version,
                pages=section["pages"],
                section_hierarchy=list(hierarchy),
                heading=section["heading"],
                strategy="document_aware"
            )
            chunks.append(chunk)

        return chunks

    def chunk_document_aware_split(self, max_chars: int = 2000) -> list[Chunk]:
        """Strategy 2: Split on headers, split large sections into paragraphs"""
        sections = self._find_sections()
        chunks = []
        hierarchy = []
        chunk_counter = 0

        for section in sections:
            # Update hierarchy
            if section["level"] == 1:
                hierarchy = [section["heading"]]
            elif section["level"] == 2:
                hierarchy = hierarchy[:1] + [section["heading"]]

            text = section["text"].strip()

            if len(text) <= max_chars:
                # Small enough, keep as is
                chunk = Chunk(
                    chunk_id=f"{self.doc_id}_doc_split_{chunk_counter}",
                    text=text,
                    doc_id=self.doc_id,
                    doc_version=self.doc_version,
                    pages=section["pages"],
                    section_hierarchy=list(hierarchy),
                    heading=section["heading"],
                    strategy="document_aware_split"
                )
                chunks.append(chunk)
                chunk_counter += 1
            else:
                # Split into paragraphs
                paragraphs = re.split(r'\n\s*\n', text)
                current_chunk = ""

                for para in paragraphs:
                    para = para.strip()
                    if not para:
                        continue

                    if len(current_chunk) + len(para) <= max_chars:
                        current_chunk += "\n\n" + para if current_chunk else para
                    else:
                        if current_chunk:
                            chunk = Chunk(
                                chunk_id=f"{self.doc_id}_doc_split_{chunk_counter}",
                                text=current_chunk,
                                doc_id=self.doc_id,
                                doc_version=self.doc_version,
                                pages=section["pages"],
                                section_hierarchy=list(hierarchy),
                                heading=section["heading"],
                                strategy="document_aware_split"
                            )
                            chunks.append(chunk)
                            chunk_counter += 1
                        current_chunk = para

                # Don't forget last chunk
                if current_chunk:
                    chunk = Chunk(
                        chunk_id=f"{self.doc_id}_doc_split_{chunk_counter}",
                        text=current_chunk,
                        doc_id=self.doc_id,
                        doc_version=self.doc_version,
                        pages=section["pages"],
                        section_hierarchy=list(hierarchy),
                        heading=section["heading"],
                        strategy="document_aware_split"
                    )
                    chunks.append(chunk)
                    chunk_counter += 1

        return chunks

    def chunk_parent_child(self, max_chars: int = 1500) -> list[Chunk]:
        """Strategy 3: Index subsections, keep parent reference"""
        sections = self._find_sections()
        chunks = []
        chunk_counter = 0
        current_parent = None
        parent_chunk_id = None

        for section in sections:
            if section["level"] == 1:
                # This is a parent section
                current_parent = section
                parent_chunk_id = f"{self.doc_id}_parent_{chunk_counter}"

                # Create parent chunk
                text = section["text"].strip()
                if len(text) > max_chars:
                    text = text[:max_chars] + "..."

                chunk = Chunk(
                    chunk_id=parent_chunk_id,
                    text=text,
                    doc_id=self.doc_id,
                    doc_version=self.doc_version,
                    pages=section["pages"],
                    section_hierarchy=[section["heading"]],
                    heading=section["heading"],
                    strategy="parent_child",
                    parent_chunk_id=None  # Parents have no parent
                )
                chunks.append(chunk)
                chunk_counter += 1

            elif section["level"] == 2 and current_parent:
                # This is a child section
                text = section["text"].strip()

                chunk = Chunk(
                    chunk_id=f"{self.doc_id}_child_{chunk_counter}",
                    text=text[:max_chars] if len(text) > max_chars else text,
                    doc_id=self.doc_id,
                    doc_version=self.doc_version,
                    pages=section["pages"],
                    section_hierarchy=[current_parent["heading"], section["heading"]],
                    heading=section["heading"],
                    strategy="parent_child",
                    parent_chunk_id=parent_chunk_id
                )
                chunks.append(chunk)
                chunk_counter += 1

        return chunks

    def chunk_fixed_size(self, size: int = 512, overlap: int = 50) -> list[Chunk]:
        """Strategy 4: Fixed size baseline"""
        chunks = []
        text = self.full_text
        start = 0
        chunk_counter = 0

        while start < len(text):
            end = start + size
            chunk_text = text[start:end]

            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk_text.rfind('. ')
                if last_period > size * 0.5:
                    end = start + last_period + 1
                    chunk_text = text[start:end]

            pages = self._get_pages_for_range(start, end)

            chunk = Chunk(
                chunk_id=f"{self.doc_id}_fixed_{chunk_counter}",
                text=chunk_text.strip(),
                doc_id=self.doc_id,
                doc_version=self.doc_version,
                pages=pages,
                section_hierarchy=[],  # No section awareness
                heading="",
                strategy="fixed_512"
            )
            chunks.append(chunk)
            chunk_counter += 1

            start = end - overlap

        return chunks


def chunk_all_strategies(pdf_path: Path, doc_id: str, doc_version: str) -> dict[str, list[Chunk]]:
    """Run all chunking strategies on a document"""
    chunker = FDAChunker(pdf_path, doc_id, doc_version)

    return {
        "document_aware": chunker.chunk_document_aware(),
        "document_aware_split": chunker.chunk_document_aware_split(),
        "parent_child": chunker.chunk_parent_child(),
        "fixed_512": chunker.chunk_fixed_size(),
    }


def main():
    """Test chunking on both documents"""
    from pathlib import Path

    docs = [
        ("data/raw/cybersecurity_2014.pdf", "cybersecurity_2014", "2014"),
        ("data/raw/cybersecurity_2023.pdf", "cybersecurity_2025", "2025"),
    ]

    for pdf_path, doc_id, version in docs:
        print(f"\n{'='*60}")
        print(f"Document: {doc_id}")
        print(f"{'='*60}")

        strategies = chunk_all_strategies(Path(pdf_path), doc_id, version)

        for strategy_name, chunks in strategies.items():
            total_chars = sum(len(c.text) for c in chunks)
            avg_chars = total_chars / len(chunks) if chunks else 0
            print(f"\n{strategy_name}:")
            print(f"  Chunks: {len(chunks)}")
            print(f"  Avg size: {avg_chars:.0f} chars")
            print(f"  Sample: {chunks[0].heading if chunks else 'N/A'}")


if __name__ == "__main__":
    main()
