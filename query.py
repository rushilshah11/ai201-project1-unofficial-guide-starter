import json
import os

from dotenv import load_dotenv
from groq import Groq

from retrieve import retrieve

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = (
    "Answer the question using only the information contained in the provided documents. "
    "Do not use prior knowledge. "
    "If the documents do not contain enough information to answer the question, "
    'respond exactly with: "I don\'t have enough information on that." '
    "Include citations for all information used.\n\n"
    "Your response MUST be a valid JSON object in this exact format:\n"
    '{"answer": "<your answer>", "sources": ["<source_filename_1>", "<source_filename_2>"]}\n\n'
    "Only include the source filenames (e.g. rmp_professors.txt) that you actually drew "
    "information from. "
    "If you cannot answer, return: "
    '{"answer": "I don\'t have enough information on that.", "sources": []}'
)

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return _client


def _format_context(chunks):
    parts = []
    for i, chunk in enumerate(chunks):
        parts.append(f"[Document {i + 1} — Source: {chunk['source']}]\n{chunk['text']}")
    return "\n\n---\n\n".join(parts)


def ask(question):
    chunks = retrieve(question)
    context = _format_context(chunks)
    user_message = f"Documents:\n\n{context}\n\nQuestion: {question}"

    response = _get_client().chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content.strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {
            "answer": raw,
            "sources": list({c["source"] for c in chunks}),
        }

    if "answer" not in result:
        result["answer"] = raw
    if "sources" not in result:
        result["sources"] = []

    return result
