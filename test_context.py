from brain.response_engine import ResponseEngine


def main():
    engine = ResponseEngine()

    print("================================")
    print("       MANTRA CONTEXT TEST")
    print("================================")

    questions = [
        "Mujhe BCA mein admission lena hai",
        "Documents kya lagenge?",
        "BCA kitne saal ka hai?",
        "Eligibility kya hai?",
        "Fees kitni hai?"
    ]

    for question in questions:

        print(f"\nStudent : {question}")

        response = engine.respond(question)

        print(f"MANTRA  : {response}")

        print(
            f"Context : {engine.get_current_course()}"
        )

    print("\nCONTEXT ENGINE: ONLINE")


if __name__ == "__main__":
    main()