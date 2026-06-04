from embed import get_collection, get_embedding_model

TOP_K = 5


def retrieve(query, k=TOP_K):
    model = get_embedding_model()
    collection = get_collection()
    query_embedding = model.encode([query]).tolist()[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({"text": doc, "source": meta["source"], "distance": dist})
    return chunks
