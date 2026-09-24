"""
MANTRA - Live Conversation Test
"""

from brain.response_engine import ResponseEngine


def main():
    print("=" * 40)
    print("        MANTRA LIVE CHAT")
    print("=" * 40)
    print("Type 'exit', 'quit' or 'bye' to end.\n")

    mantra = ResponseEngine()

    while True:

        try:
            user_input = input("Student : ").strip()

        except (KeyboardInterrupt, EOFError):
            print("\nMANTRA  : Goodbye! 👋 Take care!")
            break

        if not user_input:
            continue

        if user_input.lower() in {
            "exit",
            "quit",
            "bye",
            "goodbye"
        }:
            response = mantra.respond(user_input)
            print(f"MANTRA  : {response}")
            break

        response = mantra.respond(user_input)

        print(f"MANTRA  : {response}")

        print(
            f"Profile : {mantra.get_student_profile()}"
        )

        print()


if __name__ == "__main__":
    main()