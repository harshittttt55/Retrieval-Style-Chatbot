import csv
import json

# Paths
csv_file = "AI.csv"
json_file = "output.json"

lines = []

with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        question = row['Question'].strip()
        answer = row['Answer'].strip()
        lines.append({"role": "user", "content": question})
        lines.append({"role": "assistant", "content": answer})

# Write in compact JSON format (one after another with commas)
with open(json_file, "w", encoding="utf-8") as f:
    f.write(",\n".join(json.dumps(line, ensure_ascii=False) for line in lines))

print(f"CSV converted to chatbot JSON and saved to {json_file}")
