from dataset_loader import load_qa_pairs, get_response

# Load QA pairs
qa_pairs, qa_dict, questions_normalized = load_qa_pairs()

# Chat loop
if __name__ == "__main__":
    print("Chatbot is ready! Type 'exit' or 'quit' to stop.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Assistant: Goodbye!")
            break

        answer, suggestions = get_response(user_input, qa_pairs, qa_dict, questions_normalized)
        print("Assistant:", answer)
        if suggestions:
            print("You may also ask:")
            for s in suggestions:
                print("-", s)
