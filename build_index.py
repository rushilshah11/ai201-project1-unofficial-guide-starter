from embed import embed_and_store
from ingest import load_and_chunk_all


def main():
    print("Loading and chunking documents...")
    chunks = load_and_chunk_all()
    print(f"Total chunks: {len(chunks)}")
    print("Embedding and storing in ChromaDB...")
    embed_and_store(chunks)
    print("Index build complete.")


if __name__ == "__main__":
    main()
