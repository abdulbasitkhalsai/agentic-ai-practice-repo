from .openrouter_client import chat_with_openrouter

def main():
    user_input = input("Please ask a question from the assistant: ")
    if not user_input.strip():
        print("Input cannot be empty. Please enter a valid question.")
        return
    reply = chat_with_openrouter(user_input)
    print("\nAssistant:", reply)

if __name__ == "__main__":
    main()
