from brain.intent_router import IntentRouter


def main():
    router = IntentRouter()

    test_queries = [
        "Hello",
        "BCA ke courses kya hai?",
        "BCA kitne saal ka hai?",
        "BCA ka duration kya hai?",
        "BCA available hai kya?",
        "Computer Engineering ki fees kitni hai?",
        "Admission ke time kaunse documents lagenge?",
        "BCA ke liye eligibility kya hai?",
        "Admission kaise milega?",
        "Scholarship available hai?",
        "Mujhe admission lena hai",
        "Good morning",
        "Mujhe kuch aur puchna hai"
        "Haaan fees batao",
        "Aur fees?",
        "Fees ka kya hai?",
        "Aur eligibility?",
        "Eligibility batao",
        "Aur documents?",
        "Documents batao",
        "Aur process?",
        "Process batao",
        "Aur scholarship?",
    ]

    print("================================")
    print("       MANTRA SMART INTENT TEST")
    print("================================")

    for query in test_queries:
        intent = router.detect(query)

        print(f"\nQuestion : {query}")
        print(f"Intent   : {intent}")

    print("\nSMART INTENT ROUTER: ONLINE")


if __name__ == "__main__":
    main()