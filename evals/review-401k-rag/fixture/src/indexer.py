"""
Indexer - Load PDFs, chunk, embed, store in ChromaDB.

Simple recursive character chunking to start.
"""

import fitz  # PyMuPDF
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
from datetime import datetime

# Paths
DOCS_DIR = Path(__file__).parent.parent / "docs"
CHROMA_DIR = Path(__file__).parent.parent / "data" / "chroma"

# Chunking params (tested - 1000/200 performed best at 61.6% coverage)
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def extract_text_from_pdf(pdf_path: Path) -> list[dict]:
    """Extract text from PDF, one entry per page."""
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if text:  # Skip empty pages
            pages.append({
                "text": text,
                "source": pdf_path.name,
                "page": i + 1
            })
    return pages


def recursive_chunk(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Simple recursive character chunking.
    Tries to split on paragraphs, then sentences, then words, then characters.
    """
    if len(text) <= chunk_size:
        return [text]

    # Try splitting on double newlines (paragraphs)
    separators = ["\n\n", "\n", ". ", " ", ""]

    for sep in separators:
        if sep in text:
            parts = text.split(sep)
            chunks = []
            current = ""

            for part in parts:
                # Add separator back (except for empty string)
                part_with_sep = part + sep if sep else part

                if len(current) + len(part_with_sep) <= chunk_size:
                    current += part_with_sep
                else:
                    if current:
                        chunks.append(current.strip())
                    current = part_with_sep

            if current:
                chunks.append(current.strip())

            # If we got reasonable chunks, return them
            if all(len(c) <= chunk_size * 1.2 for c in chunks):  # Allow 20% overflow
                # Add overlap
                result = []
                for i, chunk in enumerate(chunks):
                    if i > 0 and overlap > 0:
                        # Prepend overlap from previous chunk
                        prev_overlap = chunks[i-1][-overlap:] if len(chunks[i-1]) > overlap else chunks[i-1]
                        chunk = prev_overlap + " " + chunk
                    result.append(chunk)
                return result

    # Fallback: hard split
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks


def chunk_pages(pages: list[dict]) -> list[dict]:
    """Chunk pages into smaller pieces, preserving metadata."""
    chunks = []
    for page in pages:
        page_chunks = recursive_chunk(page["text"])
        for i, chunk_text in enumerate(page_chunks):
            chunks.append({
                "text": chunk_text,
                "source": page["source"],
                "page": page["page"],
                "chunk_index": i
            })
    return chunks


def index_documents(doc_paths: list[Path] = None, collection_name: str = "401k_docs"):
    """Index documents into ChromaDB."""

    # Default to all PDFs in docs directory
    if doc_paths is None:
        doc_paths = list(DOCS_DIR.rglob("*.pdf"))

    print(f"Indexing {len(doc_paths)} documents...")
    print(f"Chunk size: {CHUNK_SIZE}, Overlap: {CHUNK_OVERLAP}")
    print(f"Embedding model: {EMBEDDING_MODEL}")
    print()

    # Extract and chunk all documents
    all_chunks = []
    for pdf_path in doc_paths:
        print(f"  Processing: {pdf_path.name}")
        pages = extract_text_from_pdf(pdf_path)
        chunks = chunk_pages(pages)
        all_chunks.extend(chunks)
        print(f"    → {len(pages)} pages → {len(chunks)} chunks")

    print(f"\nTotal chunks: {len(all_chunks)}")

    # Setup ChromaDB
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Delete existing collection if it exists
    try:
        client.delete_collection(collection_name)
        print(f"Deleted existing collection: {collection_name}")
    except:
        pass

    # Create collection with embedding function
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )
    collection = client.create_collection(
        name=collection_name,
        embedding_function=embedding_fn
    )

    # Add chunks to collection
    print(f"\nEmbedding and storing chunks...")

    ids = [f"chunk_{i}" for i in range(len(all_chunks))]
    documents = [c["text"] for c in all_chunks]
    metadatas = [{"source": c["source"], "page": c["page"], "chunk_index": c["chunk_index"]} for c in all_chunks]

    # Add in batches
    batch_size = 100
    for i in range(0, len(all_chunks), batch_size):
        batch_end = min(i + batch_size, len(all_chunks))
        collection.add(
            ids=ids[i:batch_end],
            documents=documents[i:batch_end],
            metadatas=metadatas[i:batch_end]
        )
        print(f"  Added chunks {i+1}-{batch_end}")

    print(f"\n✅ Indexed {len(all_chunks)} chunks into '{collection_name}'")
    print(f"   Stored at: {CHROMA_DIR}")

    return {
        "collection_name": collection_name,
        "total_chunks": len(all_chunks),
        "documents": [p.name for p in doc_paths],
        "timestamp": datetime.now().isoformat()
    }


def main():
    """Index all documents in docs/ directory."""
    print("="*70)
    print("401(k) Document Indexer")
    print("="*70)

    result = index_documents()

    print("\n" + "="*70)
    print("Indexing Complete")
    print("="*70)
    print(f"Documents: {len(result['documents'])}")
    print(f"Chunks: {result['total_chunks']}")


if __name__ == "__main__":
    main()
