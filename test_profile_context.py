from brain.response_engine import ResponseEngine


def main():
    print("================================")
    print("   MANTRA PROFILE + CONTEXT TEST")
    print("================================")

    engine = ResponseEngine()

    conversation = [
        "Hello",
        "Mera naam Rahul hai",
        "Mujhe BCA mein admission lena hai",
        "Documents kya lagenge?",
        "Aur fees?",
        "Aur eligibility?",
        "Kitne saal ka hai?",
        "Aur admission process?"
    ]

    for question in conversation:

        print(f"\nStudent : {question}")

        response = engine.respond(question)

        print(f"MANTRA  : {response}")

        profile = engine.get_student_profile()

        print(f"Profile : {profile}")

    print("\nPROFILE + CONTEXT ENGINE: ONLINE")


if __name__ == "__main__":
    main()