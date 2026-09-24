"""
MANTRA - Database Manager

Provides simple functions for reading and writing
college admission information.
"""

from database.db import get_connection


class DatabaseManager:
    """Manage MANTRA's admission database."""

    # ---------------------------------------------------------
    # COURSES
    # ---------------------------------------------------------

    def get_courses(self):
        """Return all available courses."""

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    name,
                    duration,
                    eligibility,
                    description
                FROM courses
                ORDER BY name
                """
            )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

        finally:

            connection.close()

    # ---------------------------------------------------------

    def get_course(self, course_name):
        """Return information about a specific course."""

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    name,
                    duration,
                    eligibility,
                    description
                FROM courses
                WHERE LOWER(name) = LOWER(?)
                """,
                (course_name,)
            )

            row = cursor.fetchone()

            return dict(row) if row else None

        finally:

            connection.close()

    # ---------------------------------------------------------

    def search_course(self, query):
        """Find courses using a partial course name."""

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    name,
                    duration,
                    eligibility,
                    description
                FROM courses
                WHERE LOWER(name) LIKE ?
                ORDER BY name
                LIMIT 5
                """,
                (f"%{query.lower()}%",)
            )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

        finally:

            connection.close()

    # ---------------------------------------------------------
    # DOCUMENTS
    # ---------------------------------------------------------

    def get_documents(self, course_name=None):
        """Return required admission documents."""

        connection = get_connection()

        try:

            cursor = connection.cursor()

            if course_name:

                cursor.execute(
                    """
                    SELECT
                        document_name,
                        description,
                        required_for
                    FROM documents
                    WHERE LOWER(required_for) = LOWER(?)
                       OR LOWER(required_for) = 'all'
                    ORDER BY document_name
                    """,
                    (course_name,)
                )

            else:

                cursor.execute(
                    """
                    SELECT
                        document_name,
                        description,
                        required_for
                    FROM documents
                    ORDER BY document_name
                    """
                )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

        finally:

            connection.close()

    # ---------------------------------------------------------
    # FEES
    # ---------------------------------------------------------

    def get_fees(self, course_name=None):
        """Return fee information."""

        connection = get_connection()

        try:

            cursor = connection.cursor()

            if course_name:

                cursor.execute(
                    """
                    SELECT
                        course_name,
                        academic_year,
                        amount,
                        notes
                    FROM fees
                    WHERE LOWER(course_name) = LOWER(?)
                    ORDER BY academic_year DESC
                    """,
                    (course_name,)
                )

            else:

                cursor.execute(
                    """
                    SELECT
                        course_name,
                        academic_year,
                        amount,
                        notes
                    FROM fees
                    ORDER BY course_name
                    """
                )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

        finally:

            connection.close()

    # ---------------------------------------------------------
    # ADMISSION PROCESS
    # ---------------------------------------------------------

    def get_admission_process(self):
        """Return admission process steps."""

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    step_number,
                    title,
                    description
                FROM admission_process
                ORDER BY step_number
                """
            )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

        finally:

            connection.close()

    # ---------------------------------------------------------
    # FAQS
    # ---------------------------------------------------------

    def get_faqs(self):
        """Return all frequently asked questions."""

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    question,
                    answer
                FROM faqs
                ORDER BY id
                """
            )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

        finally:

            connection.close()

    # ---------------------------------------------------------

    def search_faq(self, query):
        """
        Search FAQs using words from the student's question.
        """

        if not query or not query.strip():
            return []

        normalized_query = query.lower().strip()

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    question,
                    answer
                FROM faqs
                WHERE LOWER(question) LIKE ?
                   OR LOWER(answer) LIKE ?
                ORDER BY id
                LIMIT 5
                """,
                (
                    f"%{normalized_query}%",
                    f"%{normalized_query}%"
                )
            )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

        finally:

            connection.close()

    def search_faq(self, query):

        """
        Search FAQ questions using simple keyword matching.
        Returns the best matching FAQ answer.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT question, answer
                FROM faqs
                ORDER BY id
            """)

            faqs = cursor.fetchall()

        finally:
            connection.close()

        if not faqs:
            return None

        query_words = set(
            query.lower().split()
        )

        best_match = None
        best_score = 0

        for faq in faqs:

            question = faq["question"].lower()

            question_words = set(
                question.split()
            )

            score = len(
                query_words.intersection(
                    question_words
                )
            )

            if score > best_score:
                best_score = score
                best_match = dict(faq)

        # Require at least one meaningful match.
        if best_score >= 1:
            return best_match

        return None