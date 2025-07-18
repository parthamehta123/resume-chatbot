# Resume Chatbot — Streamlit App

This module provides an interactive chatbot UI for querying resumes using semantic search and a local LLM. Built with Streamlit + LangChain.

---

## Directory Structure

```
images/streamlit/
├── Dockerfile
├── requirements.txt
├── README.md
├── ask_question.sh
└── src/
    └── resume_chatbot/
        ├── __init__.py
        ├── embeddings.py
        ├── exceptions.py
        ├── main.py
        ├── streamlit_app.py
        └── utils.py
```

---

## How It Works

1. Loads previously embedded resumes from `./persist/`
2. Uses LangChain’s `RetrievalQA` over ChromaDB
3. Answers user queries using `llama3` via `ollama`
4. Displays response with sources via Streamlit UI

---

## Running Locally

### 1. Set up environment

```bash
cd images/streamlit
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start Ollama (if using local LLM)

```bash
ollama run llama3
```

### 3. Launch the Streamlit app

```bash
make run
```

---

## Testing the App

```bash
make test
```

This will run unit tests from `tests/unit`.

---

## Features

- Local vector DB with Chroma
- Local LLM via `ollama run llama3`
- No OpenAI or external API keys required
- Chat UI with persistent history and citation display
- `truncate_text` helper for chunk preview

---

## GitHub Workflows

- `ci.yml`: Runs linting and formatting checks
- `cd.yml`: Deploys both embeddings and UI via Docker
- `streamlit.yml`: Verifies Streamlit app compiles
- `test.yml`: Runs unit tests in GitHub Actions

---

## Next Step

To embed new resumes, run the embedding pipeline:

```bash
cd images/embeddings
python src/resume_chatbot/main.py
```
