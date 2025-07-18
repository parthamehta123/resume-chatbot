"""
embeddings.py

Provides vectorstore query logic and (optional) reranking for resume search.
"""

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction


def get_vector_collection(persist_dir: str = "persist", collection: str = "resumes"):
    """
    Get the Chroma collection for resumes.

    Args:
        persist_dir (str): Path to the persisted Chroma DB.
        collection (str): Collection name.

    Returns:
        Chroma Collection
    """
    embedding_function = SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    client = chromadb.PersistentClient(path=persist_dir)
    return client.get_or_create_collection(
        name=collection, embedding_function=embedding_function
    )


def query_collection(query: str, collection, top_k: int = 5):
    """
    Query a Chroma collection and return matching docs + metadata.

    Args:
        query (str): The search query.
        collection: Chroma collection instance.
        top_k (int): Number of top documents to return.

    Returns:
        Tuple[List[str], List[Dict]]: documents, metadatas
    """
    results = collection.query(
        query_texts=[query], n_results=top_k, include=["documents", "metadatas"]
    )
    return results.get("documents")[0], results.get("metadatas")[0]
