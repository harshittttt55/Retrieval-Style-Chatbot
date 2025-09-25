import os
import pickle
import re
import random
from difflib import get_close_matches

# Paths
PROCESSED_DIR = "../retrieval-style-chatbot/data"
PREPROCESS_FILE = os.path.join("data", "preprocess.pkl")

# -------------------------
# Normalize text
def normalize(text: str) -> str:
    """
    Lowercase, remove punctuation, collapse multiple spaces.
    """
    text = re.sub(r"[^\w\s]", "", text)
    return " ".join(text.strip().lower().split())

# -------------------------
# Load QA pairs
def load_qa_pairs():
    """
    Returns:
    - qa_pairs: list of (question, answer) tuples (ordered)
    - qa_dict: normalized question -> answer (for exact match)
    - questions_normalized: list of normalized questions (for fuzzy match)
    """
    print("Loading QA pairs...")
    with open(PREPROCESS_FILE, "rb") as f:
        qa_pairs = pickle.load(f)

    qa_dict = {normalize(q): a for q, a in qa_pairs}
    questions_normalized = [normalize(q) for q, _ in qa_pairs]

    print(f"Loaded {len(qa_pairs)} QA pairs.")
    return qa_pairs, qa_dict, questions_normalized

# -------------------------
# Get chatbot response
def get_response(user_input: str, qa_pairs: list, qa_dict: dict, questions_normalized: list):
    """
    Returns:
    - answer: str
    - suggestions: list of 3 questions randomly selected from next 10 in dataset
    """
    norm_input = normalize(user_input)

    # Exact match
    if norm_input in qa_dict:
        answer = qa_dict[norm_input]
        matched_index = next(i for i, (q, _) in enumerate(qa_pairs) if normalize(q) == norm_input)
        next_qs = [qa_pairs[j][0] for j in range(matched_index+1, min(matched_index+11, len(qa_pairs)))]
        suggestions = random.sample(next_qs, min(3, len(next_qs)))
        return answer, suggestions

    # Fuzzy match
    possible_matches = get_close_matches(norm_input, questions_normalized, n=1, cutoff=0.6)
    if possible_matches:
        matched_norm = possible_matches[0]
        answer = qa_dict[matched_norm]
        matched_index = next(i for i, (q, _) in enumerate(qa_pairs) if normalize(q) == matched_norm)
        next_qs = [qa_pairs[j][0] for j in range(matched_index+1, min(matched_index+11, len(qa_pairs)))]
        suggestions = random.sample(next_qs, min(3, len(next_qs)))
        return answer, suggestions

    # No match
    return "Sorry, I don't know the answer.", []
