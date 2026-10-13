"""
Generate Chunk-Level Query Labels (DIY)

For each chunk, generate 2-3 questions that the chunk answers.
Output: JSON with query + chunk_id as ground truth.
"""

import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

import sys
sys.path.insert(0, str(Path(__file__).parent))
from chunking_strategies import FDAChunker

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "google/gemini-2.5-flash")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

QUERY_GEN_PROMPT = """You are generating evaluation queries for a retrieval system.

Given this chunk from an FDA cybersecurity guidance document:

---
CHUNK ID: {chunk_id}
SECTION: {section}
TEXT:
{text}
---

Generate 2-3 questions that this specific chunk answers. These questions should:
1. Be natural questions a regulatory affairs professional might ask
2. Have answers that are ONLY found in this chunk (not general knowledge)
3. Vary in specificity (one specific, one broader)

Return JSON only, no markdown:
[
  {{"question": "...", "chunk_id": "{chunk_id}"}},
  {{"question": "...", "chunk_id": "{chunk_id}"}}
]"""


def generate_queries_for_chunk(chunk) -> list[dict]:
    """Generate queries for a single chunk"""
    prompt = QUERY_GEN_PROMPT.format(
        chunk_id=chunk.chunk_id,
        section=" > ".join(chunk.section_hierarchy),
        text=chunk.text[:2500]  # Truncate very long chunks
    )

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,  # Some variety
        )

        content = response.choices[0].message.content

        # Parse JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]

        queries = json.loads(content.strip())
        return queries

    except Exception as e:
        print(f"  Error for {chunk.chunk_id}: {e}")
        return []


def main():
    print("=" * 60)
    print("Generating Chunk-Level Query Labels")
    print("=" * 60)
    print(f"Model: {LLM_MODEL}")

    # Load chunks
    print("\nLoading chunks...")
    chunker = FDAChunker(
        Path("data/raw/cybersecurity_2023.pdf"),
        "cybersecurity_2025",
        "2025"
    )
    chunks = chunker.chunk_parent_child()
    print(f"  Chunks: {len(chunks)}")

    # Generate queries for each chunk
    print("\nGenerating queries...")
    all_queries = []

    for i, chunk in enumerate(chunks):
        print(f"  [{i+1}/{len(chunks)}] {chunk.chunk_id}...")

        queries = generate_queries_for_chunk(chunk)
        all_queries.extend(queries)

        # Rate limiting
        time.sleep(0.5)

    print(f"\nTotal queries generated: {len(all_queries)}")

    # Save results
    output_path = Path("data/eval/chunk_queries_generated.json")
    with open(output_path, "w") as f:
        json.dump(all_queries, f, indent=2)
    print(f"Saved to: {output_path}")

    # Also save chunks for reference
    chunks_ref = []
    for chunk in chunks:
        chunks_ref.append({
            "chunk_id": chunk.chunk_id,
            "heading": chunk.heading,
            "section_hierarchy": chunk.section_hierarchy,
            "pages": chunk.pages,
            "text_preview": chunk.text[:300] + "..."
        })

    chunks_path = Path("data/eval/chunks_reference.json")
    with open(chunks_path, "w") as f:
        json.dump(chunks_ref, f, indent=2)
    print(f"Chunks reference saved to: {chunks_path}")

    # Print sample
    print("\n" + "=" * 60)
    print("SAMPLE QUERIES")
    print("=" * 60)
    for q in all_queries[:5]:
        print(f"\n[{q['chunk_id']}]")
        print(f"  Q: {q['question']}")


if __name__ == "__main__":
    main()
