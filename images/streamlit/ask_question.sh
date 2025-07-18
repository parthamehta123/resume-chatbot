#!/bin/bash

# Usage: ./ask_question.sh "What is the full name?"
QUESTION="$1"

# Ensure Ollama is installed
echo "==================================="
echo "Ensure Ollama is installed"
echo "-----------------------------------"
if ! command -v ollama >/dev/null 2>&1; then
    echo "Ollama isn't installed. Please run:"
    echo "brew install ollama"
else
    echo "Ollama is installed!"
fi
echo "==================================="

# Start Ollama server in another terminal (if using local LLM)
echo "Start Ollama server in another terminal"
osascript -e 'tell app "Terminal" to do script "ollama serve"'
echo "==================================="

# Ensure you are in the root directory
echo "Ensure you are in the root directory"
if [[ ! -f "README.md" || ! -f "sonar-project.properties" ]]; then
    echo "You are not in the root directory. You are in:"
    pwd
else
    echo "You are in the right directory."
fi
echo "==================================="

# Run Python script to ask a question
echo "Run Python script to ask a question"
python3 <<EOF
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM  # Corrected import for Ollama
from langchain.chains import RetrievalQA

# Vector store config
persist_directory = "./persist"
collection_name = "resume-embeddings"

# Load local embeddings model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load vector store
vectordb = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding_model,
    collection_name=collection_name,
)

# Local LLM (Ollama)
llm = OllamaLLM(model="llama3")  # Use OllamaLLM as it was correctly imported

# Build QA chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectordb.as_retriever())

# Question passed from CLI argument
question = "$QUESTION"
result = qa_chain.invoke(question)

# Output the question and answer
print(f"Q: {question}")
print(f"A: {result['result']}")
EOF
