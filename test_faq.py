"""
MANTRA - FAQ Engine Test
"""

from brain.response_engine import ResponseEngine


def main():

    bot = ResponseEngine()

    questions = [
        "College kaha hai?",
        "College kahan hai?",
        "College ka address kya hai?",
        "College ka contact number kya hai?",
        "College ki website kya hai?",
        "Hostel hai kya?",
        "Placement ke bare mein batao",
        "BCA available hai kya?",
        "Scholarship available hai?",
    ]

    print("=" * 40)
    print("       MANTRA FAQ ENGINE TEST")
    print("=" * 40)

    for question in questions:

        response = bot.respond(question)

        print()
        print("Student :", question)
        print("Intent  :", bot.last_intent)
        print("MANTRA  :", response)

    print()
    print("FAQ ENGINE: ONLINE")


if __name__ == "__main__":
    main()