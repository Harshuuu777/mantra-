"""
MANTRA - Database Seeder

Synchronizes college_data.json with the local SQLite database.
"""

import json
import sys
from pathlib import Path


# ---------------------------------------------------------
# PROJECT PATH
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ---------------------------------------------------------
# IMPORT DATABASE
# ---------------------------------------------------------

from database.db import (
    get_connection,
    initialize_database
)


# ---------------------------------------------------------
# DATA FILE
# ---------------------------------------------------------

DATA_FILE = BASE_DIR / "data" / "college_data.json"


# ---------------------------------------------------------
# LOAD JSON
# ---------------------------------------------------------

def load_college_data():
    """Load college information from JSON."""

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"College data file not found: {DATA_FILE}"
        )

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ---------------------------------------------------------
# CLEAR TABLES
# ---------------------------------------------------------

def clear_tables(connection):
    """Clear existing synchronized data."""

    cursor = connection.cursor()

    cursor.execute("DELETE FROM courses")
    cursor.execute("DELETE FROM fees")
    cursor.execute("DELETE FROM documents")
    cursor.execute("DELETE FROM admission_process")
    cursor.execute("DELETE FROM faqs")


# ---------------------------------------------------------
# INSERT COURSES
# ---------------------------------------------------------

def seed_courses(cursor, courses):

    for course in courses:

        cursor.execute(
            """
            INSERT OR REPLACE INTO courses
            (
                name,
                duration,
                eligibility,
                description
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                course.get("name"),
                course.get("duration"),
                course.get("eligibility"),
                course.get("description")
            )
        )


# ---------------------------------------------------------
# INSERT FEES
# ---------------------------------------------------------

def seed_fees(cursor, fees):

    for fee in fees:

        cursor.execute(
            """
            INSERT INTO fees
            (
                course_name,
                academic_year,
                amount,
                notes
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                fee.get("course_name"),
                fee.get("academic_year"),
                fee.get("amount"),
                fee.get("notes")
            )
        )


# ---------------------------------------------------------
# INSERT DOCUMENTS
# ---------------------------------------------------------

def seed_documents(cursor, documents):

    for document in documents:

        # JSON currently uses:
        # "name": "Aadhaar Card"
        #
        # Database expects:
        # document_name

        document_name = document.get(
            "document_name",
            document.get("name")
        )

        description = document.get(
            "description",
            ""
        )

        required_for = document.get(
            "required_for",
            "all"
        )

        if not document_name:
            print(
                "⚠️ Skipping document with no name:",
                document
            )
            continue

        cursor.execute(
            """
            INSERT INTO documents
            (
                document_name,
                description,
                required_for
            )
            VALUES (?, ?, ?)
            """,
            (
                document_name,
                description,
                required_for
            )
        )


# ---------------------------------------------------------
# INSERT ADMISSION PROCESS
# ---------------------------------------------------------

def seed_admission_process(cursor, steps):

    for step in steps:

        # JSON currently uses:
        # "step": 1
        #
        # Database expects:
        # step_number
        #
        # Support both formats safely.

        step_number = step.get(
            "step_number",
            step.get("step")
        )

        title = step.get(
            "title"
        )

        description = step.get(
            "description",
            ""
        )

        if step_number is None:
            print(
                "⚠️ Skipping admission step with no step number:",
                step
            )
            continue

        cursor.execute(
            """
            INSERT INTO admission_process
            (
                step_number,
                title,
                description
            )
            VALUES (?, ?, ?)
            """,
            (
                step_number,
                title,
                description
            )
        )


# ---------------------------------------------------------
# INSERT FAQS
# ---------------------------------------------------------

def seed_faqs(cursor, faqs):

    for faq in faqs:

        cursor.execute(
            """
            INSERT INTO faqs
            (
                question,
                answer
            )
            VALUES (?, ?)
            """,
            (
                faq.get("question"),
                faq.get("answer")
            )
        )


# ---------------------------------------------------------
# SYNCHRONIZE
# ---------------------------------------------------------

def synchronize_database():

    print()
    print(f"Data file: {DATA_FILE}")
    print()
    print("Loading college data...")

    data = load_college_data()

    initialize_database()

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # -------------------------------------------------
        # Clear old synchronized records
        # -------------------------------------------------

        clear_tables(connection)

        # -------------------------------------------------
        # Insert courses
        # -------------------------------------------------

        seed_courses(
            cursor,
            data.get("courses", [])
        )

        # -------------------------------------------------
        # Insert fees
        # -------------------------------------------------

        seed_fees(
            cursor,
            data.get("fees", [])
        )

        # -------------------------------------------------
        # Insert documents
        # -------------------------------------------------

        seed_documents(
            cursor,
            data.get("documents", [])
        )

        # -------------------------------------------------
        # Insert admission process
        # -------------------------------------------------

        admission_steps = data.get(
            "admission_steps",
            data.get("admission_process", [])
        )

        seed_admission_process(
            cursor,
            admission_steps
        )

        # -------------------------------------------------
        # Insert FAQs
        # -------------------------------------------------

        seed_faqs(
            cursor,
            data.get("faqs", [])
        )

        # -------------------------------------------------
        # Commit
        # -------------------------------------------------

        connection.commit()

        # -------------------------------------------------
        # Counts
        # -------------------------------------------------

        cursor.execute(
            "SELECT COUNT(*) FROM courses"
        )
        courses_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM documents"
        )
        documents_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM admission_process"
        )
        admission_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM fees"
        )
        fees_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM faqs"
        )
        faqs_count = cursor.fetchone()[0]

        # -------------------------------------------------
        # Output
        # -------------------------------------------------

        print()
        print("Database synchronization completed.")
        print()

        print(
            f"Courses loaded          : {courses_count}"
        )

        print(
            f"Documents loaded        : {documents_count}"
        )

        print(
            f"Admission steps loaded  : {admission_count}"
        )

        print(
            f"Fees loaded             : {fees_count}"
        )

        print(
            f"FAQs loaded             : {faqs_count}"
        )

        print()
        print("MANTRA DATABASE: SYNCHRONIZED")

    except Exception:

        connection.rollback()
        raise

    finally:

        connection.close()


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

if __name__ == "__main__":

    try:

        synchronize_database()

    except Exception as error:

        print()
        print("MANTRA DATABASE: FAILED")
        print(f"Error: {error}")
        print()

        sys.exit(1)