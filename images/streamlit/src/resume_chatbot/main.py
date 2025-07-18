import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA

# Dynamically resolve absolute path to the top-level persist directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
persist_directory = os.path.join(project_root, "persist")
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

print(f"Collection contains {vectordb._collection.count()} records.")

# Local LLM (Ollama)
llm = OllamaLLM(model="llama3")

# Build QA chain
retriever = vectordb.as_retriever(search_kwargs={"k": 4})
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

if __name__ == "__main__":
    while True:
        query = input("\nAsk a question about the resumes (or press Enter to quit): ")
        if not query.strip():
            break

        docs = retriever.get_relevant_documents(query)
        print(f"\nRetrieved {len(docs)} relevant documents:")
        for i, doc in enumerate(docs, 1):
            print(f"\n--- Doc #{i} ---\n{doc.page_content.strip()[:1000]}")

        answer = qa_chain.invoke(query)
        print("\nAnswer:", answer)
