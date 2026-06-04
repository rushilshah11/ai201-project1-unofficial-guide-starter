"""
Prints 5 representative chunks at startup (one per source type) and reports
total chunk count. For each chunk we ask:
  - Does it make sense on its own?
  - Could a question be answered from this chunk alone?
"""

from embed import get_collection

# One chunk sampled from each of the five distinct source types in the corpus.
SAMPLE_SOURCES = [
    "rmp_professors.txt",
    "reddit_guide_to_core_curriculum.txt",
    "reddit_pros_cons_csba.txt",
    "quora_usc_cs_difficulty.txt",
    "usc_cs_course_plan.txt",
]


def inspect_chunks():
    collection = get_collection()
    total = collection.count()

    print("\n" + "=" * 70)
    print(f"CHUNK INSPECTION  |  Total chunks in index: {total}")
    print("=" * 70)

    shown = 0
    for source in SAMPLE_SOURCES:
        results = collection.get(
            where={"source": source},
            include=["documents", "metadatas"],
            limit=1,
        )
        if not results["documents"]:
            print(f"\n[SKIPPED — no chunks found for source: {source}]")
            continue

        chunk_text = results["documents"][0]
        shown += 1

        print(f"\n--- Chunk {shown} of 5 ---")
        print(f"Source : {source}")
        print(f"Length : {len(chunk_text)} chars")
        print(f"Text   :\n{chunk_text}")

    print("\n" + "=" * 70)
    print(f"Total chunks indexed: {total}")
    print("=" * 70 + "\n")
