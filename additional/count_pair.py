import json

# Path to your JSON file
json_file = "data/training_data3.json"

# Load JSON
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Flatten nested lists if needed
def flatten(data):
    flat = []
    if isinstance(data, list):
        for item in data:
            flat.extend(flatten(item))
    elif isinstance(data, dict) and "role" in data and "content" in data:
        flat.append(data)
    return flat

flat_data = flatten(data)

# Count user → assistant pairs
count = 0
i = 0
while i < len(flat_data) - 1:
    if flat_data[i]["role"] == "user" and flat_data[i + 1]["role"] == "assistant":
        count += 1
        i += 2  # skip to next potential pair
    else:
        i += 1

print(f"Total user → assistant pairs: {count}")
