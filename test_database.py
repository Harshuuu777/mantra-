from database.db import initialize_database
from database.manager import DatabaseManager


def main():
    initialize_database()

    database = DatabaseManager()

    courses = database.get_courses()
    documents = database.get_documents()
    faqs = database.get_faqs()
    process = database.get_admission_process()

    print("================================")
    print("       MANTRA DATABASE TEST")
    print("================================")

    print(f"\nCourses: {len(courses)}")
    print(f"Documents: {len(documents)}")
    print(f"FAQs: {len(faqs)}")
    print(f"Admission Steps: {len(process)}")

    print("\nDATABASE MANAGER: ONLINE")


if __name__ == "__main__":
    main()