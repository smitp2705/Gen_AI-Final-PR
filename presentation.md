# Campus Knowledge Assistant
### A Beginner RAG Project with LangChain, ChromaDB & Streamlit

---

## Slide 1 — Title
**Campus Knowledge Assistant**
Retrieval-Augmented Generation for College Documents

- Team / Student name(s): _____________
- Course / Subject: _____________
- Date: _____________

---

## Slide 2 — Problem Statement

- Students need answers from scattered college documents (rules, placement
  guidelines, FAQs).
- Manually searching multiple PDFs/notices is slow and error-prone.
- General-purpose chatbots can hallucinate — giving confident but **wrong**
  answers about *our specific* college.
- **Goal:** Build an assistant that answers *only* from our own documents, and
  clearly says "not found" when it doesn't know.

---

## Slide 3 — Objectives

1. Understand how LLMs, embeddings, and vector search work together.
2. Build a working Retrieval-Augmented Generation (RAG) pipeline end-to-end.
3. Process real documents → chunks → embeddings → vector index.
4. Retrieve relevant chunks for a question and generate a grounded answer.
5. Always show the **source document** behind an answer.
6. Wrap everything in a simple, usable Streamlit interface.

---

## Slide 4 — System Architecture

*(See `architecture.png` for the full diagram)*

**Ingestion pipeline (run once):**
Documents → Extract text → Split into chunks → Generate embeddings → Store in ChromaDB

**Query pipeline (run per question):**
Question → Retrieve top-k chunks → Build grounded prompt → Call LLM → Answer + Sources

---

## Slide 5 — Implementation Details

| Stage | Tool / Technique | File |
|---|---|---|
| Document loading | `PyPDFLoader`, `TextLoader` | `src/document_loader.py` |
| Chunking | `RecursiveCharacterTextSplitter` (800 chars, 120 overlap) | `src/chunking.py` |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` (local, free) | `src/vectorstore.py` |
| Vector store | ChromaDB (persisted on disk) | `src/vectorstore.py` |
| LLM | OpenAI `gpt-4o-mini` via LangChain | `src/rag_chain.py` |
| Grounding | Similarity-score threshold + explicit "not found" rule | `src/rag_chain.py` |
| Interface | Streamlit (question box, answer, sources, debug chunks) | `app.py` |

---

## Slide 6 — Demo Walkthrough

1. Launch app: `streamlit run app.py`
2. Ask a **factual** question → correct answer + source file shown.
3. Ask a question needing **two documents** → combined, grounded answer.
4. Ask an **irrelevant** question (e.g., "capital of France") → assistant
   politely declines, no hallucination.
5. Ask about something **absent** from documents (e.g., Wi-Fi password) →
   "information not found" response.

---

## Slide 7 — Results & Testing

- Tested 10 questions across 4 categories (see `tests/test_questions.md`):
  factual, multi-document, irrelevant, and absent-information questions.
- Experimented with chunk size/overlap (500/50, 800/120, 1200/200) —
  **800/120 chosen** as the best balance of precision and context.
- Grounding rule successfully prevented hallucinated answers on irrelevant
  and out-of-scope questions during testing.

---

## Slide 8 — Limitations & Future Work

**Limitations**
- Only knows what's inside `documents/` — no general knowledge.
- No authentication, deployment pipeline, or multi-user handling (out of
  scope per assignment rules).

**Possible Enhancements**
- Support DOCX / webpage sources.
- Adjustable top-k and visible similarity scores (partially implemented).
- Persistent chat history across sessions.
- User feedback button to flag incorrect/unsupported answers.
