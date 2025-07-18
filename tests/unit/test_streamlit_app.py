import sys
import os

# Add the correct path to sys.path
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../images/streamlit/src")
    ),
)

import pytest
import streamlit as st
from resume_chatbot.streamlit_app import (
    get_qa_chain,
)  # Import the method you want to test


# Test for checking the retrieval of the QA chain
def test_get_qa_chain():
    qa_chain, retriever = get_qa_chain()
    assert qa_chain is not None
    assert retriever is not None


# Test the function to ensure it can handle a basic query
def test_query_answer():
    qa_chain, retriever = get_qa_chain()
    result = qa_chain.invoke("What is the full name of the candidate?")
    assert result["result"] is not None
    assert (
        "Poorvik Gambheer" in result["result"]
    )  # Check if expected name appears in the answer


# Additional test: Verify the query for an empty string is handled
def test_empty_query():
    qa_chain, retriever = get_qa_chain()
    result = qa_chain.invoke("")
    assert "I don't know" in result["result"]  # Check if response mentions uncertainty
    assert (
        "context" in result["result"]
    )  # Ensure that context is mentioned, indicating the model can't provide an answer.
