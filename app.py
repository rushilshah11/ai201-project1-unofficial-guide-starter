import gradio as gr

from inspect_chunks import inspect_chunks
from inspect_retrieval import inspect_retrieval
from query import ask

inspect_chunks()
inspect_retrieval()


def handle_query(question):
    if not question.strip():
        return "", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="The Unofficial Guide to CS & CSBA at USC") as demo:
    gr.Markdown("## The Unofficial Guide to CS & CSBA at USC")
    gr.Markdown(
        "Ask anything about courses, professors, degree requirements, or major comparisons "
        "for the CS and CSBA programs at the University of Southern California."
    )

    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. Is Redekopp a good professor?",
    )
    btn = gr.Button("Ask", variant="primary")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])


demo.launch()
