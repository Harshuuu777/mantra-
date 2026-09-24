from brain.response_engine import ResponseEngine


def main():
    print("================================")
    print("   MANTRA FULL CONVERSATION TEST")
    print("================================")

    engine = ResponseEngine()

    conversation = [
        "Hello",
        "Mera naam Rahul hai",
        "Mujhe BCA mein admission lena hai",
        "BCA kitne saal ka hai?",
        "Eligibility kya hai?",
        "Documents kya lagenge?",
        "Aur fees?",
        "Aur scholarship?",
        "Aur admission process?",
        "Thank you"
    ]

    for question in conversation:

        print(f"\nStudent : {question}")

        response = engine.respond(question)

        print(f"MANTRA  : {response}")

        print(
            f"Profile : {engine.get_student_profile()}"
        )

    print("\n================================")
    print("   FULL CONVERSATION: ONLINE")
    print("================================")


if __name__ == "__main__":
    main()