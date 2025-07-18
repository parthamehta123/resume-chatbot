import sys
import os
import streamlit as st
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM

try:
    from utils import truncate_text
except ImportError:
    from resume_chatbot.utils import truncate_text

# Add the path to the 'resume_chatbot' module (src/resume_chatbot)
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../src"))
)

st.set_page_config(page_title="Resume Chatbot", layout="wide")
st.title("Resume Chatbot")
st.markdown("Ask questions about the resumes you've embedded.")

# Setup sidebar
with st.sidebar:
    st.header("Instructions")
    st.markdown(
        "1. Ensure you've run the embeddings pipeline.\n"
        "2. Ask any question about the resumes.\n"
        "3. Citations and sources will be shown per answer."
    )

# Dynamically resolve absolute path to the shared persist directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
persist_dir = os.path.join(project_root, "persist")
collection = "resume-embeddings"


# VectorDB + LLM setup
@st.cache_resource
def get_qa_chain():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectordb = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings,
        collection_name=collection,
    )
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})
    llm = OllamaLLM(model="llama3")
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever), retriever


qa_chain, retriever = get_qa_chain()

# Chat history state
if "history" not in st.session_state:
    st.session_state.history = []

# Chat input UI
user_query = st.chat_input("Ask a question about any resume...")
if user_query:
    # Show user message
    st.chat_message("user").markdown(user_query)

    # Retrieve docs and show assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Retrieve relevant documents
            retrieved_docs = retriever.get_relevant_documents(user_query)
            answer = qa_chain.invoke(user_query)["result"]

            st.markdown(answer)

            with st.expander("Sources (Top documents)"):
                for i, doc in enumerate(retrieved_docs, 1):
                    source = doc.metadata.get("source", "unknown")
                    st.markdown(f"**Doc {i}** — *{source}*")
                    st.code(truncate_text(doc.page_content), language="text")

    # Save history
    st.session_state.history.append({"role": "user", "content": user_query})
    st.session_state.history.append({"role": "assistant", "content": answer})
