"""
MANTRA - Admission Database

Local SQLite database for verified college admission information.
"""

import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "college.db"


def get_connection():
    """Create and return a SQLite database connection."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Create MANTRA's admission database tables."""

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            duration TEXT,
            eligibility TEXT,
            description TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            academic_year TEXT,
            amount REAL,
            notes TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_name TEXT NOT NULL,
            description TEXT,
            required_for TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admission_process (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            step_number INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def database_status():
    """Check whether the database exists and is accessible."""

    try:
        connection = get_connection()
        connection.execute("SELECT 1")
        connection.close()
        return True

    except sqlite3.Error:
        return False


if __name__ == "__main__":
    initialize_database()

    if database_status():
        print("MANTRA Database: ONLINE")
        print(f"Database: {DATABASE_PATH}")
    else:
        print("MANTRA Database: FAILED")