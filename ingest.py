from pathlib import Path

DOCUMENTS_DIR = Path(__file__).parent / "documents"
CHUNK_SIZE = 700
OVERLAP = 100


def load_sources():
    sources = []
    for path in sorted(DOCUMENTS_DIR.glob("*.txt")):
        sources.append({"source": path.name, "text": path.read_text(encoding="utf-8")})
    return sources


def chunk_text(text, source):
    chunks = []
    start = 0
    chunk_id = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()
        if chunk:
            chunks.append({"id": f"{source}_{chunk_id}", "text": chunk, "source": source})
            chunk_id += 1
        start += CHUNK_SIZE - OVERLAP
    return chunks


def load_and_chunk_all():
    all_chunks = []
    for doc in load_sources():
        all_chunks.extend(chunk_text(doc["text"], doc["source"]))
    return all_chunks
