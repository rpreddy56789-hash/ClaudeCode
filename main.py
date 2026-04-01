import anthropic
import json
from datetime import datetime

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

COMMANDS = """
Commands:
  /clear    - Reset conversation history
  /history  - Show number of messages in conversation
  /save     - Save conversation to a timestamped file
  quit/exit - Exit the chatbot
"""

def save_conversation(messages):
    if not messages:
        print("No conversation to save.\n")
        return
    filename = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(messages, f, indent=2)
    print(f"Conversation saved to {filename}\n")

def chatbot():
    messages = []
    print("Claude Chatbot")
    print(COMMANDS)

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ("quit", "exit"):
            break
        if not user_input:
            continue
        if user_input.lower() == "/clear":
            messages = []
            print("Conversation history cleared.\n")
            continue
        if user_input.lower() == "/history":
            print(f"Messages in conversation: {len(messages)}\n")
            continue
        if user_input.lower() == "/save":
            save_conversation(messages)
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
