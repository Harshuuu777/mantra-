from brain.course_extractor import CourseExtractor


def main():
    extractor = CourseExtractor()

    test_queries = [
        "BCA ke baare mein batao",
        "BCA kitne saal ka hai?",
        "BCA available hai kya?",
        "B Tech mein kaunse courses hain?",
        "Computer Engineering ki fees kitni hai?",
        "Mechanical Engineering available hai?",
        "Civil engineering ka duration kya hai?",
        "Electrical Engineering ke baare mein batao",
        "Information Technology branch hai kya?",
        "ENTC available hai?",
        "AI branch ke baare mein batao",
        "Data Science course hai kya?",
        "AI and ML course available hai?",
        "Cyber Security branch hai?",
        "Mujhe admission ke documents chahiye",
    ]

    print("================================")
    print("      MANTRA COURSE EXTRACTOR")
    print("================================")

    for query in test_queries:

        course = extractor.extract(query)

        print(f"\nQuestion : {query}")
        print(f"Course   : {course}")

    print("\nCOURSE EXTRACTOR: ONLINE")


if __name__ == "__main__":
    main()