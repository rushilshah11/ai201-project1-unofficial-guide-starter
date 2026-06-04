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
    # Q1: CS vs CSBA tradeoffs
    run_test(
        label="Q1 — CS vs CSBA pros and cons",
        question="What are the pros and cons of choosing CSBA over CS?",
        should_answer=True,
    )

    # Q2: Professor Redekopp quality
    run_test(
        label="Q2 — Professor Redekopp review",
        question="Is Redekopp a good professor?",
        should_answer=True,
    )

    # Q3: CSCI 103 vs skipping to 104
    run_test(
        label="Q3 — Should I take CSCI 103 or skip to CSCI 104?",
        question="Should I take CSCI 103 or skip to CSCI 104?",
        should_answer=True,
    )

    # Q4: Best professors for CSCI 170
    run_test(
        label="Q4 — Best professors for CSCI 170",
        question="Who are the best professors for CSCI 170?",
        should_answer=True,
    )

    # Q5: CSCI 270 difficulty
    run_test(
        label="Q5 — CSCI 270 difficulty",
        question="What do students say about CSCI 270 difficulty?",
        should_answer=True,
    )
