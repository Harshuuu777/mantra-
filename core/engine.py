"""
MANTRA Core Engine

Responsible for receiving student queries and routing them
to the appropriate MANTRA component.
"""


class MantraEngine:
    """Main processing engine for MANTRA."""

    def __init__(self):
        self.name = "MANTRA"
        self.status = "ONLINE"

    def process(self, user_input: str) -> str:
        """
        Process a user query.

        This is the initial routing layer.
        AI, database and RAG will be connected later.
        """

        if not user_input or not user_input.strip():
            return "Please tell me how I can help you."

        query = user_input.strip().lower()

        if self._is_greeting(query):
            return "Hello! Welcome to our college. How can I help you?"

        if self._is_admission_query(query):
            return "I can help you with the college admission process."

        return "I can help you with courses, fees, documents, eligibility, and the admission process."

    @staticmethod
    def _is_greeting(query: str) -> bool:
        """Check whether the student is greeting MANTRA."""

        greetings = [
            "hello",
            "hi",
            "hey",
            "namaste",
            "good morning",
            "good afternoon",
            "good evening",
        ]

        return any(word in query for word in greetings)

    @staticmethod
    def _is_admission_query(query: str) -> bool:
        """Check whether the query is related to admission."""

        keywords = [
            "admission",
            "admit",
            "apply",
            "application",
            "enroll",
            "enrolment",
        ]

        return any(word in query for word in keywords)