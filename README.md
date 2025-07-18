# Resume Chatbot
A fully local AI chatbot that answers questions about resumes using semantic search and a local LLM — no OpenAI or cloud APIs needed.

## Overview
This project provides a two-part system:
- An embedding pipeline that processes resume PDFs into semantic chunks using HuggingFace and ChromaDB → See `images/embeddings/README.md` -> [here](https://github.com/parthamehta123/resume-chatbot/blob/main/images/embeddings/README.md) for setup and instructions.
- A chatbot UI built with Streamlit that uses LangChain’s RetrievalQA over a local Ollama LLM to answer resume-specific questions — no cloud APIs or keys required → See `images/streamlit/README.md` [here](https://github.com/parthamehta123/resume-chatbot/blob/resume-chatbot-full/images/streamlit/README.md) for running the chatbot app.
