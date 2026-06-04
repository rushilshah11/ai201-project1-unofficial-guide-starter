# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section _after_ you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

I chose course and professor reviews for Computer Science and Computer Science and Business Administration at the University of Southern California. This knowledge is valuable to computer science students because it gives context to the difficulty of the class and professor preparation. There are times where one professor can make the class more difficult than another professor through difficult exams, lack of office hours, or simply not doing a better job at making complex topics digestible.

This information is valuable for a student who is really interested in a class topic, wants to prepare their course plan ahead of time, or wants raw insight from previous students to be prepared for a class. It also helps with picking a major, switching majors, or choosing between very similar majors.

The university does not provide this information. The professor does not provide insight into their teaching style, syllabus or expectations prior to the first day of class. This information is not accessible unless physically asked for to a professor, alumni, or counselor.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| #   | Source             | Description                                                                                          | URL or location                                                                                   |
| --- | ------------------ | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| 1   | Rate My Professors | All USC reviews including courses, food, housing, professors, etc                                    | https://www.ratemyprofessors.com/school/1381                                                      |
| 2   | Rate My Professors | All professors in computer science at USC                                                            | https://www.ratemyprofessors.com/search/professors/1381?q=*&did=11                                |
| 3   | Reddit             | Current Student's experiences with professors at USC                                                 | https://www.reddit.com/r/USC/comments/1mfmw0w/why_are_all_the_cs_professors_at_usc_meh/           |
| 4   | Reddit             | Description of Core CS Classes at USC                                                                | https://www.reddit.com/r/USC/comments/rrvjj1/small_guide_to_the_cs_core_curriculum_at_usc/        |
| 5   | Reddit             | Description of Difficulty of CS Major at USC                                                         | https://www.reddit.com/r/USC/comments/8x3ar3/how_difficult_is_the_cs_major/                       |
| 6   | Quora              | General Overview of CS Major at USC focused on difficulty of classes                                 | https://www.quora.com/How-is-the-Computer-Science-major-at-USC-How-hard-are-the-CS-classes-at-USC |
| 7   | usc.edu            | Official Course Plan for Computer Science major                                                      | https://www.cs.usc.edu/academic-programs/undergrad/computer-science/                              |
| 8   | usc.edu            | Official Course Plan for Computer Science & Business Administration major                            | https://www.cs.usc.edu/academic-programs/undergrad/computer-science-business-administration/      |
| 9   | Reddit             | Current Student debating between Computer Science or Computer Science & Business Admistration majors | https://www.reddit.com/r/USC/comments/zw1pp4/cant_decide_between_internal_transfer_to_csba_or/    |
| 10  | Reddit             | Pros and Cons of Computer Science & Business Administration major                                    | https://www.reddit.com/r/USC/comments/1mp1bf/what_are_the_pros_and_cons_of_majoring_in/           |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

700 Characters

**Overlap:**

100 Characters

**Why these choices fit your documents:**

I wanted one consistent strategy across all sources. My sources are either naturally grouped (RMP by professor) or naturally segmented (Reddit/Quora by paragraph/class/topic), so chunks tend to capture coherent units of meaning.

For RMP specifically, reviews are already grouped by professor on the page, so a chunk of 2 reviews is essentially "what students think of Professor X" — which is exactly what you'd want to retrieve for that query. The only edge case is the tail end of one professor's reviews bleeding into the next, but the signal ratio is still heavily weighted toward the right professor, and the LLM can use the professor's name in each review to attribute opinions correctly.

For Reddit and Quora sources, posts are already broken into paragraphs or sections by class, topic, or question. Reddit paragraphs tend to be shorter and more concise than typical, closer to 5 sentences and 550 characters, so one paragraph fits comfortably within the 700 character range without needing a separate strategy.

A typical paragraph is estimated at around 6 sentences and 650 characters, so one paragraph fits within a single chunk. The 100 character overlap covers 1–2 sentences, enough to avoid cutting a thought at a boundary without being so long that one class's difficulty bleeds into another's.

**Update (Milestone 5):** Original chunk size was 1200–1500 characters (targeting 2 paragraphs per chunk), producing only 53 total chunks — too few to give the retriever meaningful signal diversity. Reduced to 700 characters (1 paragraph per chunk) with overlap halved proportionally to 100 characters, targeting ~100 chunks. Smaller chunks also embed more precisely against all-MiniLM-L6-v2's 256-token context window, which was silently truncating the tail of every 1400-character chunk.

Known limitation:
Sources 7 and 8 (USC.edu official course pages) are structured as bulleted lists rather than paragraphs. A single chunk from these sources may contain 8–10 course requirements or course names, each a short bullet. This means the chunk's embedding points in multiple directions simultaneously, which can hurt retrieval precision for specific course queries. This is a known tradeoff accepted in favor of keeping one consistent chunking strategy for a first project.

**Final chunk count:**

96

**Sample chunks:**

> **Chunk 1 — Source: `rmp_professors.txt`**
> "CS104 is a very difficult and very time intensive class. Redekopp is probably the best teacher you can get as far as this class goes. He goes a little fast at times, but is thorough and explains things clearly and in multiple ways. Very fair grading policies and criteria. Also the most respected professor in CS. Be ready to spend hours on homework."

> **Chunk 2 — Source: `reddit_cs_difficulty.txt`**
> "Now that I've graduated, there are a couple things I would have done differently that would 1, make my life easier, and 2, get me better grades. Go to class, pay attention, and actually THINK through all your problems, homework, and projects. Don't just copy the solution, actually understand why it works. Go to office hours and talk to the CPs. Form study groups."

> **Chunk 3 — Source: `reddit_pros_cons_csba.txt`**
> "I am a current CS/BA student and I have to say, the program is exceptional. You don't go as heavy into CS or as heavy into the BUAD program compared to if you were a pure CS or BA major but you get a really really solid background. In terms of job search, it sets you up exceptionally well if you're looking for a management position at a tech company and it looks really really good on the resume."

> **Chunk 4 — Source: `quora_usc_cs_difficulty.txt`**
> "Curriculum difficulty: solid-to-challenging. Expect steep learning curves in core courses — Data Structures & Algorithms, Systems/OS, Computer Architecture, and Theory are widely considered the toughest. Grading and workload: competitive environment with substantial programming assignments, projects, and exams. Group projects are common and assess real engineering skills."

> **Chunk 5 — Source: `usc_cs_course_plan.txt`**
> "A grade of C (2.0) or better is required for each of the core computer science courses: CSCI 102L, CSCI 103L, CSCI 170, CSCI 104L and CSCI 201L. Core computer science courses with a grade of C- or below must be repeated; these courses may only be retaken once. Departmental approval is required in order to retake a course."

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:**

For a production deployment the tradeoffs get more complex. General models may not understand USC specific terminology like course codes, professor nicknames, or student slang like "weedout class," so a model trained on more domain specific text would perform better. USC also has a large international student population, so multilingual support would be an important consideration. Context length matters too because the model needs to comfortably handle 1200-1500 character chunks without cutting them off and losing meaning. Latency is not ultra critical but students looking up classes during registration periods need reasonable response times.

---

## Retrieval Test Examples

**Query 1: "What are the pros and cons of choosing CSBA over CS?"**

| Rank | Source | Distance | Chunk preview |
|------|--------|----------|---------------|
| 1 | `reddit_csba_or_cs.txt` | 0.6408 | "I really want to learn an intensive amount of CS topics, and learn business as I'd like to have a career in both, but the course requirements for CS/BUAD are…" |
| 2 | `reddit_csba_or_cs.txt` | 0.7972 | "CSBA is much less work, but I think that's a con, rather than a pro. By foregoing the pure CS degree, you'll miss out on a lot of really interesting parts of computer science…" |
| 3 | `reddit_csba_or_cs.txt` | 0.8783 | "A lot of ppl say that if you care about having that technical background, you should probably do CS and then minor in something in Marshall… CSBA isn't super technical — even the CS minor has more requirements…" |
| 4 | `reddit_pros_cons_csba.txt` | 0.9180 | "I'm currently a freshman at USC and was hoping someone could explain the pros and cons between majoring in CSBA and double majoring in CS and BA…" |
| 5 | `reddit_csba_or_cs.txt` | 0.9823 | "If you're interested in business, I'd just do CSBA." |

*Why these chunks are relevant:* All 5 chunks came from Reddit threads that debate the CS vs. CSBA decision directly. The query phrase "pros and cons" and "CSBA over CS" embedded close to posts where students use exactly that framing — weighing the tradeoff between technical depth and business breadth. Chunks 1–3 and 5 are from the same thread (`reddit_csba_or_cs.txt`), which is expected because that thread is entirely about this decision. Chunk 4 pulls from a second thread (`reddit_pros_cons_csba.txt`) that addresses the same question from a different angle, adding perspective from a student comparing CSBA to a full double major. The retrieval correctly surfaced multiple viewpoints rather than over-indexing on a single post.

---

**Query 2: "Is Redekopp a good professor?"**

| Rank | Source | Distance | Chunk preview |
|------|--------|----------|---------------|
| 1 | `reddit_professor_ranking.txt` | 0.8097 | "Was Redekopp not on the list? Because he is absolutely GOAT." |
| 2 | `rmp_professors.txt` | 0.9299 | "Prof. Redekopp is charismatic and it's easy to ask questions in class…" |
| 3 | `rmp_professors.txt` | 0.9768 | "CS104 is a very difficult and very time intensive class. Redekopp is probably the best teacher you can get as far as this class goes…" |
| 4 | `rmp_professors.txt` | 0.9930 | "Overall Quality: 4.4/5 based on 368 ratings. Mark Redekopp, Professor in the Engineering department at USC…" |
| 5 | `reddit_professor_ranking.txt` | 1.1146 | "…as great humor and really excels at theoretical topics. Marco Paolieri is one of the nicest professors I have ever seen…" |

*Why these chunks are relevant:* The proper noun "Redekopp" acts as a strong anchor — the embedding model clustered all top results around chunks where that name appears. Chunks 1–4 are directly about Redekopp, pulling from both his RMP profile and a Reddit ranking thread. Chunk 5 is the weakest result (distance 1.1146, above the warning threshold flagged in `inspect_retrieval.py`) and drifts toward other professor names in the same thread; it contributed little to the final answer. The retrieval correctly prioritized RMP reviews as the most information-dense source for professor quality questions.

---

**Query 3: "What do students say about CSCI 270 difficulty?"**

| Rank | Source | Distance | Chunk preview |
|------|--------|----------|---------------|
| 1 | `quora_usc_cs_difficulty.txt` | 0.7802 | "For the whole semester, we just wrote three AI-related programs, and two of them are pretty easy…" |
| 2 | `reddit_guide_to_core_curriculum.txt` | 0.8081 | "CSCI 350: OS. You die in this class. CSCI 360: This class feels very theoretical, but surprisingly useful during interviews…" |
| 3 | `rmp_professors.txt` | 0.8737 | "Difficult class in general. Great professor who makes a complicated class pretty straightforward grading-wise…" (CSCI 170 review) |
| 4 | `reddit_guide_to_core_curriculum.txt` | 0.8812 | "CSCI 356: The system intro class at USC. I took it with Marco and have absolutely no complaints…" |
| 5 | `rmp_professors.txt` | 0.8863 | "Difficulty: 5.0 — CS270. Exams are insane but…" |

Only chunk 5 directly addresses CSCI 270. Chunks 1–4 retrieved adjacent content about general CS difficulty and nearby course numbers (350, 360, 356), which is the failure described in the Failure Case Analysis — CSCI 270 appears in only one chunk across all 96, so the retriever padded the results with tangentially related material.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

The system prompt explicitly restricts the model to the retrieved documents only:

> "Answer the question using only the information contained in the provided documents. Do not use prior knowledge. If the documents do not contain enough information to answer the question, respond exactly with: 'I don't have enough information on that.' Include citations for all information used."

Two mechanisms enforce this beyond just the instruction. First, the model is required to return a structured JSON object (`{"answer": "...", "sources": [...]}`) via Groq's `response_format: json_object` setting — this schema constraint makes it harder for the model to embed unsourced prose. Second, `temperature=0.1` is used to minimize hallucination-prone creative generation.

The retrieved context is formatted with explicit document boundaries and source labels before being passed to the model:

```
[Document 1 — Source: reddit_cs_difficulty.txt]
<chunk text>

---

[Document 2 — Source: rmp_usc_stats.txt]
<chunk text>
```

This labeling makes it straightforward for the model to identify which file each piece of information came from, supporting accurate citation.

**How source attribution is surfaced in the response:**

The model is instructed to populate the `"sources"` field in its JSON response with only the filenames it actually drew information from (e.g., `["rmp_usc_stats.txt", "reddit_cs_difficulty.txt"]`). The calling code in [app.py](app.py) reads this field and surfaces the source filenames alongside the answer to the user, so every response is accompanied by the specific documents it was grounded in.

**Out-of-scope query example** — *"Should I take CSCI 103 or skip to CSCI 104?"*

```
Answer:
I don't have enough information on that.

Retrieved from:
*(empty)*
```

This demonstrates the grounding fallback working as intended. No relevant chunks existed in the corpus for this question, so the model returned the exact fallback phrase specified in the system prompt rather than generating an answer from prior knowledge. The empty sources field confirms no documents were cited.

**Example system response 1** — *"What are the pros and cons of choosing CSBA over CS?"*

```
Answer:
The pros of choosing CSBA over CS include less work and the ability to learn business
topics in addition to CS. However, the cons include missing out on interesting parts of
computer science, potentially restricting technical background, and the degree being
considered less technical and less valuable by some.

Retrieved from:
• reddit_csba_or_cs.txt
• reddit_pros_cons_csba.txt
```

**Example system response 2** — *"Is Redekopp a good professor?"*

```
Answer:
Yes, according to the documents, Redekopp is considered a good professor. He is described
as charismatic, able to break complex problems into simple analogies, and having fair
grading policies. Many students have given him high ratings and would take his classes again.

Retrieved from:
• reddit_professor_ranking.txt
• rmp_professors.txt
```

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| #   | Question                                             | Expected answer                                                                                                                       | System response (summarized)                                                                                                                              | Retrieval quality                                                                               | Response accuracy                                                                                                       |
| --- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| 1   | What are the pros and cons of choosing CSBA over CS? | CSBA covers core CS but adds business courses; better for broad/less-technical goals. Cons: fewer advanced electives, no OS coverage. | Pros: less work, business topics alongside CS. Cons: misses interesting CS areas, restricts technical background, degree seen as less technical/valuable. | Good — 5 relevant chunks from `reddit_csba_or_cs.txt` and `reddit_pros_cons_csba.txt`           | Accurate — captured the key tradeoffs; cons framing slightly different but grounded correctly                           |
| 2   | Is Redekopp a good professor?                        | Yes, excellent teacher; makes 103/104 content very digestible.                                                                        | Yes — charismatic, breaks complex problems into simple analogies, fair grading, high ratings, students would take him again.                              | Good — pulled from both `reddit_professor_ranking.txt` and `rmp_professors.txt`                 | Accurate — consistent with expected answer and well-sourced                                                             |
| 3   | Should I take CSCI 103 or skip to CSCI 104?          | Not recommended — 104 is a big DSA step up, 103 prepares you well.                                                                    | "I don't have enough information on that."                                                                                                                | Poor — no relevant chunks retrieved; no documents directly address the 103-vs-104 skip question | Inaccurate — this is a gap in the document corpus; the answer exists in some sources but no chunk captured it directly  |
| 4   | Who are the best professors for CSCI 170?            | Aaron Cote — makes complex theory very digestible.                                                                                    | Cote is highly recommended for CSCI-170 per `rmp_professors.txt`.                                                                                         | Good — retrieved the right professor from the right source                                      | Accurate — matches expected answer                                                                                      |
| 5   | What do students say about CSCI 270 difficulty?      | One of the hardest math classes; theoretically challenging but rewarding if you like math.                                            | High difficulty — one student rated it 5.0 difficulty and described exams as "insane."                                                                    | Acceptable — retrieved from `rmp_professors.txt` only; missed Reddit perspectives               | Partially accurate — captured the difficulty signal but lost the "rewarding if you like math" nuance from other sources |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

_Should I take CSCI 103 or skip to CSCI 104?_

**What the system returned:**

`"I don't have enough information on that."` with an empty sources list — the grounding fallback triggered correctly, but the question itself is answerable from student experience.

**Root cause (tied to a specific pipeline stage):**

The failure originates at the **document ingestion stage**, not retrieval or generation. The most relevant document, `reddit_guide_to_core_curriculum.txt`, explicitly states in its opening line: _"I have taken the majority of CS core classes besides CSCI 102–104."_ That means no chunk in the entire corpus discusses 103 or 104 as a course experience. At retrieval time, `all-MiniLM-L6-v2` encodes the query into an embedding that searches for semantic similarity to "CSCI 103 vs 104 skip decision" — but no chunk in ChromaDB carries that meaning. The top-5 results would have come back with high cosine distance (low similarity), and whatever was retrieved contained nothing about the topic, so the model correctly reported insufficient information rather than hallucinating.

The ingestion stage simply never captured a source that addresses introductory course sequencing at USC.

**What you would change to fix it:**

Add at least one source that specifically covers 103 and 104 — for example, a Reddit thread about CSCI 103 prerequisites, Redekopp's RMP profile (since he teaches 103/104 and student reviews often mention the course sequence), or a USC advising FAQ page. The chunking and retrieval stages are working correctly; the fix is upstream at document selection. An alternative mitigation at query time would be a small metadata filter that flags when all top-k chunks exceed a distance threshold and prompts the user to ask something else, rather than silently failing.

---

## Query Interface

The interface is built with Gradio (`gr.Blocks`) and launched via `app.py`. It exposes three visible elements:

| Field | Type | Description |
|-------|------|-------------|
| **Your question** | Text input | Text box where the user types any question about USC CS/CSBA courses, professors, or major comparisons. Placeholder: *"e.g. Is Redekopp a good professor?"* |
| **Answer** | Text output | The grounded answer generated by `llama-3.3-70b-versatile` via Groq, drawn strictly from the retrieved documents. Displays the fallback message *"I don't have enough information on that."* when no relevant chunks are found. |
| **Retrieved from** | Text output | Bullet-formatted list of source filenames the model cited, populated from the `"sources"` field of the JSON response. Empty when the system cannot answer. |

**Sample interaction transcript:**

---

> **User:** Who are the best professors for CSCI 170?

> **Answer:**
> Cote is a highly recommended professor for CSCI-170, as stated in the rmp_professors.txt document.

> **Retrieved from:**
> • rmp_professors.txt

---

> **User:** Should I take CSCI 103 or skip to CSCI 104?

> **Answer:**
> I don't have enough information on that.

> **Retrieved from:**
> *(empty)*

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

The architecture diagram in planning.md decomposed the pipeline into five discrete stages with specific tools assigned to each — all-MiniLM-L6-v2 for embedding, ChromaDB as the vector store, and Groq's llama-3.3-70b-versatile for generation. This meant each stage could be implemented as its own module (`ingest.py`, `embed.py`, `retrieve.py`, `query.py`) with clear inputs and outputs, and when prompting Claude to generate each module I could hand it the relevant section of planning.md directly rather than re-explaining the architecture from scratch each time.

**One way your implementation diverged from the spec, and why:**

The original chunking spec called for 1200–1500 character chunks (approximately 2 paragraphs per chunk), but the implementation settled at 700 characters. After running the pipeline, only 53 total chunks were produced at the larger size — too few to give the retriever meaningful signal diversity across 10 sources. A second issue emerged from the embedding model: all-MiniLM-L6-v2 has a 256-token context window (~950 characters), which silently truncated the tail of every 1400-character chunk during embedding, meaning retrieval was effectively searching on only the first half of each chunk anyway. Reducing to 700 characters fixed both problems and brought the chunk count up to 96, which is a much healthier corpus for top-5 retrieval.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- _What I gave the AI:_

  > You are an expert Python software engineer helping me build my Applied AI class project. First, read `planning.md` to understand the system architecture, data flow, chunking strategy, retrieval pipeline, embedding model, vector database, and generation requirements before making any code changes.
  >
  > I am building The Unofficial Guide to CS and CSBA at USC, a RAG chatbot where USC students can ask questions about courses, majors, degree requirements, and professors. The knowledge base has already been created from Reddit discussions, Quora discussions, Rate My Professor reviews, and official USC degree plans.
  >
  > Grounding requirements: Pass retrieved chunks into the LLM as context. Instruct the model to answer ONLY using the provided context, never use outside knowledge, and respond exactly with "I don't have enough information on that." if the documents are insufficient. Every answer must cite the source documents used. Return a structured JSON object: `{"answer": "...", "sources": [...]}`. Use Groq with `llama-3.3-70b-versatile` and credentials from `.env`. Include end-to-end grounding tests covering an answerable question, a professor question, and an out-of-scope question — flag any grounding failures.

- _What it produced:_ `query.py` with the `ask()` function, a `_format_context()` helper labeling each chunk as `[Document N — Source: filename]`, a Groq API call with `response_format: json_object` and `temperature=0.1`, and `test_grounding.py` with labeled test cases that print sources, the generated answer, and flag grounding failures.
- _What I changed or overrode:_ I updated the system prompt Claude generated to be more specific — the original was close to my example but I tightened it to explicitly require that every source cited in the answer must appear in the retrieved chunks by filename.

**Instance 2**

- _What I gave the AI:_

  > Add a Gradio web interface. Add `gradio>=6.9.0` to requirements if not already present. Implement an `app.py` using `gr.Blocks` with a textbox input, an Ask button, an answer output (8 lines), and a sources output (4 lines), wired to a `handle_query()` function that calls `ask()` and formats sources as a bulleted list. Wire both `btn.click` and `inp.submit` to the handler. The interface should clearly show the user question, grounded answer, and retrieved sources.

- _What it produced:_ `app.py` with a `gr.Blocks` layout matching the spec — two output textboxes, both `btn.click` and `inp.submit` wired to `handle_query`, and bullet-formatted source display using `• {s}` for each source filename.
- _What I changed or overrode:_ It did a pretty good job for the interface, especially since I have never used gradio before. I added a descriptive title, a `gr.Markdown` subtitle with domain context, a placeholder on the input textbox, and `variant="primary"` on the Ask button.
