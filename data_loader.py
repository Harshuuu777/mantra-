"""
MANTRA - College Data Loader

Loads verified college information from JSON
into the MANTRA SQLite database.
"""

import json
from pathlib import Path

from database.db import get_connection, initialize_database


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "college_data.json"


def load_data():
    """Load college information from JSON into SQLite."""

    initialize_database()

    if not DATA_FILE.exists():
        print("College data file not found.")
        return False

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    connection = get_connection()
    cursor = connection.cursor()

    try:
        for course in data.get("courses", []):
            cursor.execute(
                """
                INSERT OR IGNORE INTO courses
                (name, duration, eligibility, description)
                VALUES (?, ?, ?, ?)
                """,
                (
                    course["name"],
                    course.get("duration"),
                    course.get("eligibility"),
                    course.get("description")
                )
            )

        for fee in data.get("fees", []):
            cursor.execute(
                """
                INSERT INTO fees
                (course_name, academic_year, amount, notes)
                VALUES (?, ?, ?, ?)
                """,
                (
                    fee["course_name"],
                    fee.get("academic_year"),
                    fee.get("amount"),
                    fee.get("notes")
                )
            )

        for document in data.get("documents", []):
            cursor.execute(
                """
                INSERT INTO documents
                (document_name, description, required_for)
                VALUES (?, ?, ?)
                """,
                (
                    document["document_name"],
                    document.get("description"),
                    document.get("required_for", "all")
                )
            )

        for step in data.get("admission_process", []):
            cursor.execute(
                """
                INSERT INTO admission_process
                (step_number, title, description)
                VALUES (?, ?, ?)
                """,
                (
                    step["step_number"],
                    step["title"],
                    step["description"]
                )
            )

        for faq in data.get("faqs", []):
            cursor.execute(
                """
                INSERT INTO faqs
                (question, answer)
                VALUES (?, ?)
                """,
                (
                    faq["question"],
                    faq["answer"]
                )
            )

        connection.commit()

    except (KeyError, json.JSONDecodeError) as error:
        connection.rollback()
        print(f"Data loading failed: {error}")
        return False

    finally:
        connection.close()

    print("College data loaded successfully.")
    return True


if __name__ == "__main__":
    load_data()