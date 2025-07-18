# Resume Chatbot — Embedding Pipeline

This module processes resume PDFs, generates semantic embeddings using a HuggingFace model, and stores them in a local Chroma vector database. These embeddings are later used by a Streamlit chatbot interface for question answering.

---

## Directory Structure

```
images/embeddings/
├── Dockerfile
├── requirements.txt
├── README.md
└── src/
    └── resume_chatbot/
        ├── __init__.py
        ├── exceptions.py
        └── main.py
```

---

## How It Works

1. Scans the `./resumes/` directory for `.pdf` files.
2. Uses LangChain’s:
   - `PyPDFLoader` (via `langchain_community`)
   - `RecursiveCharacterTextSplitter`
3. Generates embeddings with:
   - `sentence-transformers/all-MiniLM-L6-v2` via `langchain_huggingface`
4. Saves them into a ChromaDB vector store at `./persist/`

---

## Running Locally (Without Docker)

### 1. Prepare environment

```bash
cd images/embeddings
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Place your resume PDFs in the root-level directory:

```
/resumes/resume_1.pdf
/resumes/resume_2.pdf
```

### 3. Run the script

```bash
python src/resume_chatbot/main.py
```

You should see:

```
Found 2 resumes.
Loaded 2 documents.
Split into 22 chunks.
Stored 22 chunks in ChromaDB at ./persist
```

---

## Running with Docker (Optional)

```bash
docker build -t resume-embedder .
docker run -v $(pwd)/resumes:/app/resumes resume-embedder
```

This will persist the vector database at `/persist`.

---

## Configuration

| Setting         | Default                                  |
|-----------------|-------------------------------------------|
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2` |
| Chunk size      | 500 tokens                               |
| Chunk overlap   | 50 tokens                                |
| Vector DB       | ChromaDB                                 |

You can change these in `main.py`.

---

## Features

- No OpenAI or API keys needed
- Uses HuggingFace models locally
- Adds `source` (filename) metadata to each chunk
- Works offline with `langchain_huggingface` and `Chroma`

---

## Limitations

- Only `.pdf` files are supported (text-based)
- Scanned/image-only PDFs will not extract text correctly
- To support `.docx`, `.txt`, or `.md`, update the loader logic in `main.py`

---

## Next Step

Launch the chatbot UI from:

```
images/streamlit/src/resume_chatbot/streamlit_app.py
```
