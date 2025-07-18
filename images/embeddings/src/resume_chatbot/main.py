import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import sys

# Config
resume_dir = "./resumes"
persist_dir = "./persist"
collection = "resume-embeddings"
embedding_model = "sentence-transformers/all-MiniLM-L6-v2"

# Step 1: Load all PDF resumes
pdf_files = [f for f in os.listdir(resume_dir) if f.endswith(".pdf")]

if not pdf_files:
    print("No resumes found to process. Skipping embedding.")
    sys.exit(0)

print(f"Found {len(pdf_files)} resumes.")

raw_docs = []
for pdf in pdf_files:
    loader = PyPDFLoader(os.path.join(resume_dir, pdf))
    docs = loader.load()

    # Update each doc with the correct filename in metadata
    for doc in docs:
        doc.metadata["source"] = pdf
    raw_docs.extend(docs)

# Step 2: Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
documents = text_splitter.split_documents(raw_docs)
print(f"Split into {len(documents)} chunks.")

# Step 3: Print out a preview of chunks for debugging
for i, doc in enumerate(documents[:5]):
    print(f"\n--- Chunk #{i+1} ---")
    print(f"Source: {doc.metadata['source']}")
    print(doc.page_content[:300] + ("..." if len(doc.page_content) > 300 else ""))

# Step 4: Generate and persist embeddings
embedding_function = HuggingFaceEmbeddings(model_name=embedding_model)
vectordb = Chroma.from_documents(
    documents=documents,
    embedding=embedding_function,
    persist_directory=persist_dir,
    collection_name=collection,
)
vectordb.persist()
print(f"Stored {len(documents)} chunks in ChromaDB at {persist_dir}")
