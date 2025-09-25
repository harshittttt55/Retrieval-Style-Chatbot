import os
import json
import pickle

# Paths
RAW_DIR = "../retrieval style chat/data"
PROCESSED_DIR = "../retrieval style chat/data"
os.makedirs(PROCESSED_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(PROCESSED_DIR, "preprocess.pkl")

# Load all JSON files
json_files = [f for f in os.listdir(RAW_DIR) if f.lower().endswith(".json")]
if not json_files:
    raise FileNotFoundError(f"No JSON files found in {RAW_DIR}")

qa_pairs = []

for file_name in json_files:
    file_path = os.path.join(RAW_DIR, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"Skipping invalid JSON: {file_name}")
            continue

        # Handle wrapped "dialogue" key
        if isinstance(data, dict) and "dialogue" in data:
            data = data["dialogue"]

        # Ensure it's a list
        if not isinstance(data, list):
            print(f"Skipping non-list JSON: {file_name}")
            continue

        # Extract user → assistant pairs
        for i in range(len(data) - 1):
            if data[i]["role"] == "user" and data[i + 1]["role"] == "assistant":
                question = data[i]["content"].strip()
                answer = data[i + 1]["content"].strip()
                qa_pairs.append((question, answer))

print(f"Preprocessing complete! Total QA pairs: {len(qa_pairs)}")

# Save as pickle
with open(OUTPUT_FILE, "wb") as f:
    pickle.dump(qa_pairs, f)
