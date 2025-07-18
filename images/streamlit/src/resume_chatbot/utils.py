"""
utils.py

Utility helpers (can be extended for logging, S3 sync, formatting).
"""

import os
import datetime
import json


def log_question_answer(log_dir: str, question: str, answer: str):
    """
    Save question + answer pair to a local JSONL file.

    Args:
        log_dir (str): Directory to save logs.
        question (str): User query.
        answer (str): Generated answer.
    """
    os.makedirs(log_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(log_dir, f"qa_{ts}.json")

    data = {"timestamp": ts, "question": question, "answer": answer}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def truncate_text(text, max_length=1000):
    """
    Truncates the given text to a specified maximum length, appending ellipsis if needed.
    :param text: The input text to truncate.
    :param max_length: The maximum length of the text after truncation (default is 1000 characters).
    :return: Truncated text with an ellipsis if it exceeds the max_length.
    """
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text
