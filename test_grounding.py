from query import ask

INSUFFICIENT = "I don't have enough information on that."


def run_test(label, question, should_answer=True):
    print(f"\n{'=' * 65}")
    print(f"TEST  : {label}")
    print(f"QUERY : {question}")

    result = ask(question)
    answer = result["answer"]
    sources = result["sources"]

    print(f"ANSWER: {answer}")
    print(f"SOURCES: {sources}")

    failures = []

    if should_answer:
        if answer.strip() == INSUFFICIENT:
            failures.append("Expected a grounded answer but got insufficient-info response")
        if not sources:
            failures.append("No sources cited — citation required for grounded answers")
    else:
        if answer.strip() != INSUFFICIENT:
            failures.append(
                f"Expected insufficient-info response but got answer: {answer[:100]}"
            )
        if sources:
            failures.append(
                f"Sources must be empty for unanswerable query, got: {sources}"
            )

    if failures:
        print("GROUNDING FAILURES:")
        for failure in failures:
            print(f"  FAIL: {failure}")
    else:
        print("GROUNDING: PASS")


if __name__ == "__main__":
    # Test 1: Answerable from multiple sources (Reddit, Quora, USC.edu)
    run_test(
        label="Answerable — CS vs CSBA tradeoffs",
        question="What are the pros and cons of choosing CSBA over CS at USC?",
        should_answer=True,
    )

    # Test 2: Professor-specific — RMP reviews
    run_test(
        label="Answerable — Professor Redekopp review",
        question="Is Redekopp a good professor? What do students say about him?",
        should_answer=True,
    )

    # Test 3: Outside the knowledge base — should trigger insufficient-info
    run_test(
        label="Outside knowledge base — ramen near USC",
        question="What is the best ramen restaurant near USC?",
        should_answer=False,
    )
