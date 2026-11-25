"""
app.py
------
Milestone 5: Build the interface.

A simple Streamlit front-end for the Campus Knowledge Assistant. Lets a
student type a question, see the generated answer, the source document(s)
it was grounded on, and (optionally) the raw retrieved chunks for
transparency/debugging.

Run with:  streamlit run app.py
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st

from config import DOCUMENTS_DIR, TOP_K
from vectorstore import get_or_build_vectorstore
from rag_chain import answer_question

st.set_page_config(page_title="Campus Knowledge Assistant", page_icon="🎓", layout="centered")


@st.cache_resource(show_spinner="Loading / building document index...")
def load_db():
    return get_or_build_vectorstore(DOCUMENTS_DIR)


def main():
    st.title("🎓 Campus Knowledge Assistant")
    st.caption(
        "Ask questions about academic rules, placement guidelines, and student FAQs. "
        "Answers are grounded in the uploaded college documents only."
    )

    with st.sidebar:
        st.header("About")
        st.write(
            "This is a beginner RAG (Retrieval-Augmented Generation) project built with "
            "LangChain, ChromaDB and Streamlit, as described in `README.md`."
        )
        st.divider()
        st.subheader("Settings")
        top_k = st.slider("Chunks to retrieve (top-k)", min_value=1, max_value=8, value=TOP_K)
        show_chunks = st.checkbox("Show retrieved chunks (debug view)", value=False)
        st.divider()
        st.subheader("Indexed documents")
        if os.path.isdir(DOCUMENTS_DIR):
            for f in sorted(os.listdir(DOCUMENTS_DIR)):
                st.write(f"- {f}")

    try:
        db = load_db()
    except Exception as e:
        st.error(f"Could not load the document index: {e}")
        st.stop()

    if "history" not in st.session_state:
        st.session_state.history = []

    question = st.text_input(
        "Ask a question about your college:",
        placeholder="e.g. What is the minimum attendance required for exams?",
    )
    ask_clicked = st.button("Ask", type="primary")

    if ask_clicked and question.strip():
        with st.spinner("Retrieving relevant information and generating an answer..."):
            try:
                result = answer_question(db, question, top_k=top_k)
            except RuntimeError as e:
                st.error(str(e))
                st.stop()

        st.session_state.history.insert(0, {"question": question, "result": result})

    for item in st.session_state.history:
        q = item["question"]
        result = item["result"]

        st.markdown(f"**Q: {q}**")
        if result["grounded"]:
            st.success(result["answer"])
        else:
            st.warning(result["answer"])

        if result["sources"]:
            st.markdown("**Sources:** " + ", ".join(f"`{s}`" for s in result["sources"]))

        if show_chunks:
            with st.expander("Retrieved chunks (debug)"):
                for doc, score in result["retrieved_chunks"]:
                    st.markdown(
                        f"- score=`{score:.4f}` | source=`{doc.metadata.get('source')}`"
                    )
                    st.caption(doc.page_content[:300] + "...")

        st.divider()


if __name__ == "__main__":
    main()
