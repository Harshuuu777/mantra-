"""
MANTRA - Interactive Chat

Terminal interface for the MANTRA college admission assistant.
"""

from brain.response_engine import ResponseEngine


def print_header():
    """Display MANTRA chat header."""

    print()
    print("==============================================")
    print("              MANTRA AI ASSISTANT")
    print("       College Admission Assistant")
    print("==============================================")
    print()
    print("Type 'exit' or 'quit' to end the conversation.")
    print()


def main():
    """Start the MANTRA interactive chat."""

    engine = ResponseEngine()

    print_header()

    print(
        "MANTRA: Hello! Welcome to our college. "
        "How can I help you with the admission process?"
    )

    while True:

        try:
            user_input = input("\nYou: ").strip()

        except (KeyboardInterrupt, EOFError):
            print("\n\nMANTRA: Goodbye! Have a great day. 👋")
            break

        if not user_input:
            print("MANTRA: Please tell me how I can help you.")
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("MANTRA: Goodbye! Have a great day. 👋")
            break

        response = engine.respond(user_input)

        print(f"MANTRA: {response}")

if __name__ == "__main__":
    main()