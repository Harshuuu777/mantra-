# brain/faq_engine.py

import re


class FAQEngine:
    """
    MANTRA FAQ Engine

    Reads FAQ data from DatabaseManager and finds the
    best matching answer for a student's question.
    """

    def __init__(self, database):
        self.database = database

    # ---------------------------------------------------------
    # PUBLIC METHOD
    # ---------------------------------------------------------

    def answer(self, user_input):
        """
        Find the best FAQ answer for the user's question.

        Returns:
            str  -> FAQ answer if a good match is found
            None -> if no suitable FAQ is found
        """

        if not user_input:
            return None

        query = self._normalize(user_input)

        if not query:
            return None

        faqs = self._get_faqs()

        if not faqs:
            return None

        best_answer = None
        best_score = 0

        for faq in faqs:
            question = faq.get("question", "")
            answer = faq.get("answer", "")

            if not question or not answer:
                continue

            score = self._calculate_score(query, question)

            if score > best_score:
                best_score = score
                best_answer = answer

        # Minimum confidence threshold
        if best_score >= 35:
            return best_answer

        return None

    # ---------------------------------------------------------
    # GET FAQ DATA
    # ---------------------------------------------------------

    def _get_faqs(self):
        """
        Get FAQs from DatabaseManager.

        DatabaseManager should provide:
            get_faqs()
        """

        try:
            getter = getattr(self.database, "get_faqs", None)

            if getter is None:
                return []

            rows = getter()

            if not rows:
                return []

            faqs = []

            for row in rows:
                faq = self._convert_row(row)

                if faq:
                    faqs.append(faq)

            return faqs

        except Exception as error:
            print(f"FAQ ENGINE ERROR: {error}")
            return []

    # ---------------------------------------------------------
    # ROW CONVERTER
    # ---------------------------------------------------------

    def _convert_row(self, row):
        """
        Convert SQLite row / dictionary / tuple into a
        standard dictionary.
        """

        try:

            # Dictionary
            if isinstance(row, dict):
                return {
                    "question": str(row.get("question", "")),
                    "answer": str(row.get("answer", ""))
                }

            # SQLite Row
            if hasattr(row, "keys"):
                keys = row.keys()

                question = ""

                answer = ""

                if "question" in keys:
                    question = row["question"]

                if "answer" in keys:
                    answer = row["answer"]

                return {
                    "question": str(question),
                    "answer": str(answer)
                }

            # Tuple / List
            if isinstance(row, (tuple, list)):

                if len(row) >= 2:
                    return {
                        "question": str(row[0]),
                        "answer": str(row[1])
                    }

        except Exception as error:
            print(f"FAQ ROW ERROR: {error}")

        return None

    # ---------------------------------------------------------
    # NORMALIZATION
    # ---------------------------------------------------------

    def _normalize(self, text):
        """
        Normalize Hindi/Hinglish/English style questions.
        """

        text = str(text).lower().strip()

        # Remove punctuation
        text = re.sub(r"[^\w\s]", " ", text)

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # ---------------------------------------------------------
    # SCORE CALCULATION
    # ---------------------------------------------------------

    def _calculate_score(self, query, question):
        """
        Calculate similarity score between user query
        and FAQ question.
        """

        question = self._normalize(question)

        if not query or not question:
            return 0

        # Exact match
        if query == question:
            return 100

        # Full question contained inside query
        if question in query:
            return 90

        # Query contained inside FAQ question
        if query in question:
            return 85

        query_words = set(query.split())
        question_words = set(question.split())

        if not query_words or not question_words:
            return 0

        common_words = query_words.intersection(question_words)

        if not common_words:
            return 0

        # Remove very common conversational words
        stop_words = {
            "hai",
            "kya",
            "ka",
            "ke",
            "ki",
            "mein",
            "me",
            "mujhe",
            "batao",
            "please",
            "the",
            "is",
            "a",
            "an",
            "what",
            "is",
            "about"
        }

        useful_query_words = {
            word for word in query_words
            if word not in stop_words
        }

        useful_question_words = {
            word for word in question_words
            if word not in stop_words
        }

        if not useful_query_words:
            return 0

        useful_common = (
            useful_query_words.intersection(useful_question_words)
        )

        if not useful_common:
            return 0

        # Calculate percentage
        query_match = (
            len(useful_common) / len(useful_query_words)
        ) * 100

        question_match = (
            len(useful_common) / len(useful_question_words)
        ) * 100

        # Weighted score
        score = (
            query_match * 0.65
            + question_match * 0.35
        )

        return int(score)