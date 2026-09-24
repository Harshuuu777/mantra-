from brain.response_engine import ResponseEngine


def main():
    engine = ResponseEngine()

    test_queries = [
        "Hello",
        "BCA ke courses kya hai?",
        "Admission ke liye documents kya chahiye?",
        "Admission ka process kya hai?",
        "Mujhe admission mein help chahiye."
    ]

    print("================================")
    print("       MANTRA RESPONSE TEST")
    print("================================")

    for query in test_queries:
        print(f"\nStudent : {query}")
        print(f"MANTRA  : {engine.respond(query)}")

    print("\nRESPONSE ENGINE: ONLINE")


if __name__ == "__main__":
    main()