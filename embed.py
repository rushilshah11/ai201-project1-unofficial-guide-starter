from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "usc_cs_guide"
CHROMA_PATH = str(Path(__file__).parent / "chroma_db")

_model = None


def get_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(COLLECTION_NAME)


def embed_and_store(chunks):
    model = get_embedding_model()
    collection = get_collection()
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True).tolist()
    collection.upsert(
        ids=[c["id"] for c in chunks],
        embeddings=embeddings,
        documents=texts,
        metadatas=[{"source": c["source"]} for c in chunks],
    )
    print(f"Stored {len(chunks)} chunks in ChromaDB collection '{COLLECTION_NAME}'.")
