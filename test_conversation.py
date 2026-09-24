from brain.response_engine import ResponseEngine


def main():
    print("================================")
    print("     MANTRA CONVERSATION TEST")
    print("================================")

    engine = ResponseEngine()

    conversation = [
        "Hello",
        "Mujhe BCA mein admission lena hai",
        "Haan documents batao",
        "Aur process kya hai?",
        "Kitne saal ka hai?",
        "Eligibility bhi batao",
        "Fees ka kya hai?"
    ]

    for question in conversation:

        print(f"\nStudent : {question}")

        response = engine.respond(question)

        print(f"MANTRA  : {response}")

        print(
            f"Context : {engine.get_current_course()}"
        )

    print("\nCONVERSATION ENGINE: ONLINE")


if __name__ == "__main__":
    main()