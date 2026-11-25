## Campus Knowledge Assistant

A beginner-friendly **Retrieval-Augmented Generation (RAG)** application that answers
student questions using a small collection of college documents (academic rules,
placement guidelines, student FAQs). Built with **LangChain**, **ChromaDB**, and
**Streamlit**, following the "Beginner-Friendly LLM, LangChain & RAG Project" assignment.

---

## 1. Problem Statement

Students often need information scattered across many college documents. A
general-purpose chatbot may answer confidently but incorrectly, because it has no
access to the institution's actual rules. This project builds a small assistant that:

- Answers **only** from the provided documents.
- Clearly shows **which document** an answer came from.
- Says **"information not found"** when the answer isn't in the documents, instead of
  guessing.

## 2. What This Project Demonstrates

| Concept | Where it's implemented |
|---|---|
| Document loading (PDF/TXT) | `src/document_loader.py` |
| Chunking (with configurable size/overlap) | `src/chunking.py` |
| Embeddings (local, free `sentence-transformers`) | `src/vectorstore.py` |
| Vector storage & retrieval (ChromaDB) | `src/vectorstore.py` |
| Prompting + LLM call + grounding rule | `src/rag_chain.py` |
| User interface | `app.py` (Streamlit) |

## 3. Project Structure

```
CampusKnowledgeAssistant/
├── app.py                      # Streamlit UI (entry point)
├── requirements.txt
├── README.md
├── .env.example                # copy to .env and add your API key
├── architecture.png            # system flow diagram
├── presentation.md             # 6-slide project presentation (source)
├── documents/                  # sample source documents (3 .txt files)
│   ├── academic_rules.txt
│   ├── placement_guidelines.txt
│   └── student_faq.txt
├── src/
│   ├── config.py                # all tunable settings in one place
│   ├── document_loader.py       # Milestone 2: load PDF/TXT
│   ├── chunking.py               # Milestone 2: split into chunks
│   ├── vectorstore.py            # Milestone 3: embeddings + ChromaDB
│   └── rag_chain.py              # Milestone 4: retrieval + LLM + grounding
├── tests/
│   ├── test_questions.md         # Milestone 6: 10-question test report
│   └── run_test_questions.py     # script to run all 10 questions at once
├── scripts/
│   └── make_architecture_diagram.py   # regenerates architecture.png
└── chroma_db/                    # auto-created vector index (gitignored)
```

## 4. Setup & Installation

### Step 1 — Clone and create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Add your API key
```bash
cp .env.example .env
# then open .env and paste your OpenAI API key
```
> ⚠️ Never commit your real `.env` file or paste API keys into code/screenshots.
> The default LLM is `gpt-4o-mini` via OpenAI, set in `src/config.py` — swap in any
> other LangChain chat model if you prefer.

### Step 4 — (Optional) Add your own documents
Drop any `.pdf` or `.txt` files into `documents/`. At least 3 sample `.txt` files about
a fictional college are already included so the app works out of the box.

## 5. Running the App

```bash
streamlit run app.py
```

The first run builds the vector index (`chroma_db/`) from the files in `documents/` —
this can take a few seconds to a minute depending on document size. Subsequent runs
reuse the saved index automatically.

To force a full rebuild of the index (e.g., after changing documents or chunk settings):
```bash
python -c "from src.vectorstore import build_vectorstore; from src.config import DOCUMENTS_DIR; build_vectorstore(DOCUMENTS_DIR, rebuild=True)"
```

## 6. Running the Test Suite

```bash
python tests/run_test_questions.py
```
This runs the 10 questions listed in `tests/test_questions.md` and prints each answer,
whether it was grounded, and which source document(s) it used. Copy the results into
the table in `tests/test_questions.md`.

## 7. How It Works (RAG Workflow)

**Ingestion (done once, when the index is built):**
```
Documents → Extract text → Split into chunks → Generate embeddings → Store in ChromaDB
```

**Query (done every time a student asks a question):**
```
Question → Retrieve top-k relevant chunks → Build context-aware prompt
         → Call LLM → Answer + source filename(s)
```

See `architecture.png` for the full visual diagram.

### Grounding rule
Before calling the LLM, the retrieved chunks are checked against a similarity-score
threshold (`MAX_RELEVANT_DISTANCE` in `src/config.py`). If nothing relevant enough is
found, the app skips the LLM call entirely and replies that the information isn't in
the documents — this avoids hallucinated answers for irrelevant or absent questions.

## 8. Tech Stack

- **Language:** Python
- **Framework:** LangChain (loaders, text splitter, prompts, retrieval)
- **LLM:** OpenAI `gpt-4o-mini` (configurable)
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` (local, free, no API key)
- **Vector store:** ChromaDB (persisted to disk)
- **Interface:** Streamlit

## 9. Limitations & Future Enhancements

- Answers are only as good as the documents provided — the assistant does not know
  anything outside `documents/`.
- No authentication, deployment, or multi-user support (per assignment rules, these are
  explicitly out of scope for the core project).
- Possible optional enhancements: support `.docx`/web pages, adjustable top-k in the UI
  (already included), show similarity scores, chat history (already included within a
  session), and a feedback button for flagging bad answers.

## 10. Academic Integrity Note

This project was built by following the official assignment guidelines
(`Final Project_Guidelines.pdf`). Every component (document loading, chunking,
embeddings, vector storage, retrieval, prompting, and the grounding rule) is kept
simple and commented so each part can be explained and demonstrated individually,
per the assignment's evaluation criteria.

## Author

# Smit patel
