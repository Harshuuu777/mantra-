from brain.response_engine import ResponseEngine


def run_test():

    brain = ResponseEngine()

    tests = [
        "Mera naam Harshal hai",
        "Mujhe BCA mein admission lena hai",
        "Documents kya lagenge?",
        "Aur BTech?",
        "Documents?",
        "Aur BCA ke documents?",
        "Fees?",
        "Eligibility?",
        "Scholarship?",
    ]

    print("\n========================================")
    print("   MANTRA STEP 29 - CONTEXT TEST")
    print("========================================\n")

    for user_input in tests:

        print(f"👤 You: {user_input}")

        response = brain.respond(user_input)

        print(f"🤖 MANTRA: {response}")

        print(
            f"🧠 Context -> "
            f"Course: {brain.get_current_course()} | "
            f"Topic: {brain.get_last_topic()}"
        )

        print("-" * 60)


if __name__ == "__main__":
    run_test()