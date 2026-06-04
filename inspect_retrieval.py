"""
Runs 3 test queries against the vector store at startup and prints the top
retrieved chunks with distance scores. Flags any result with distance >= 0.5
as a potential retrieval quality issue.
"""

from retrieve import retrieve

DISTANCE_THRESHOLD = 1.0

TEST_QUERIES = [
    {
        "label": "CS vs CSBA comparison",
        "query": "What are the pros and cons of choosing CSBA over CS at USC?",
    },
    {
        "label": "Professor Redekopp review",
        "query": "Is Redekopp a good professor?",
    },
    {
        "label": "CSCI 270 difficulty",
        "query": "What do students say about CSCI 270 difficulty?",
    },
]


def inspect_retrieval():
    print("\n" + "=" * 70)
    print("RETRIEVAL INSPECTION  |  Top-5 chunks per test query")
    print("=" * 70)

    for test in TEST_QUERIES:
        print(f"\n--- Query: {test['label']} ---")
        print(f"Q: {test['query']}")

        chunks = retrieve(test["query"])

        for i, chunk in enumerate(chunks):
            flag = "  <<< DISTANCE WARNING" if chunk["distance"] >= DISTANCE_THRESHOLD else ""
            print(f"\n  Result {i + 1} | dist={chunk['distance']:.4f} | source={chunk['source']}{flag}")
            preview = chunk["text"][:300].replace("\n", " ")
            print(f"  {preview}...")

    print("\n" + "=" * 70 + "\n")
