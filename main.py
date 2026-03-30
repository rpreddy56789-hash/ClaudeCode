import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

def chatbot():
    messages = []
    print("Claude Chatbot (type 'quit' to exit)\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit"):
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        print("Claude: ", end="", flush=True)

        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=8096,
            messages=messages,
        ) as stream:
            response_text = ""
            for text in stream.text_stream:
                print(text, end="", flush=True)
                response_text += text

        print()  # newline after response
        messages.append({"role": "assistant", "content": response_text})

if __name__ == "__main__":
    chatbot()
