from brain.response_engine import ResponseEngine


def main():
    print("================================")
    print("       MANTRA PROFILE TEST")
    print("================================")

    engine = ResponseEngine()

    conversation = [
        "Hello",
        "Mera naam Rahul hai",
        "Mujhe BCA mein admission lena hai",
        "Documents kya lagenge?",
        "Aur process kya hai?"
    ]

    for question in conversation:

        print(f"\nStudent : {question}")

        response = engine.respond(question)

        print(f"MANTRA  : {response}")

        print(
            f"Profile : {engine.get_student_profile()}"
        )

    print("\nSTUDENT PROFILE: ONLINE")


if __name__ == "__main__":
    main()