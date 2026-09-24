"""
MANTRA - Course Extractor

Extracts the course or branch mentioned in a student's
English, Hindi, or Hinglish question.
"""

import re


class CourseExtractor:
    """Identify a specific college course from user input."""

    COURSE_ALIASES = {
        "bca": [
            "bca",
            "b.c.a",
            "bachelor of computer applications",
            "computer applications",
        ],

        "bba": [
            "bba",
            "b.b.a",
            "bachelor of business administration",
        ],

        "mca": [
            "mca",
            "m.c.a",
            "master of computer applications",
        ],

        "mba": [
            "mba",
            "m.b.a",
            "master of business administration",
        ],

        "b.tech": [
            "b.tech",
            "btech",
            "b tech",
            "bachelor of technology",
        ],

        "m.tech": [
            "m.tech",
            "mtech",
            "m tech",
            "master of technology",
        ],

        "computer engineering": [
            "computer engineering",
            "computer engg",
            "computer eng",
            "ce",
        ],

        "information technology": [
            "information technology",
            "information tech",
            "it engineering",
            "it branch",
        ],

        "mechanical engineering": [
            "mechanical engineering",
            "mechanical engg",
            "mechanical eng",
            "mechanical",
        ],

        "civil engineering": [
            "civil engineering",
            "civil engg",
            "civil eng",
            "civil",
        ],

        "electrical engineering": [
            "electrical engineering",
            "electrical engg",
            "electrical",
        ],

        "electronics and telecommunication engineering": [
            "electronics and telecommunication engineering",
            "electronics & telecommunication engineering",
            "electronics telecommunication",
            "electronics and telecommunication",
            "entc",
            "e&tc",
            "etc engineering",
        ],

        "artificial intelligence": [
            "artificial intelligence",
            "ai engineering",
            "ai branch",
        ],

        "data science": [
            "data science",
            "data science engineering",
            "ds engineering",
            "ds branch",
        ],

        "artificial intelligence and machine learning": [
            "artificial intelligence and machine learning",
            "artificial intelligence & machine learning",
            "ai and ml",
            "ai ml",
            "aiml",
            "ai/ml",
        ],

        "cyber security": [
            "cyber security",
            "cybersecurity",
            "cyber security engineering",
            "cyber branch",
        ],
    }

    def extract(self, user_input: str):
        """
        Extract the most likely course from user input.

        Returns:
            Canonical course name or None.
        """

        if not user_input or not user_input.strip():
            return None

        query = self._normalize(user_input)

        # Check longer phrases first so that specific
        # course names are matched before generic aliases.
        aliases = []

        for course, course_aliases in self.COURSE_ALIASES.items():
            for alias in course_aliases:
                aliases.append((alias, course))

        aliases.sort(
            key=lambda item: len(item[0]),
            reverse=True
        )

        for alias, course in aliases:

            if self._matches(query, alias):
                return course

        return None

    @staticmethod
    def _normalize(text: str) -> str:
        """Normalize user input."""

        text = text.lower().strip()

        # Normalize common separators.
        text = text.replace("-", " ")
        text = text.replace("_", " ")

        # Remove punctuation.
        # This allows inputs such as:
        # BTech?
        # BCA!
        # B.Tech.
        # BCA,
        # B.Tech admission?
        text = re.sub(r"[^\w\s&/]", " ", text)

        return " ".join(text.split())

    @staticmethod
    def _matches(query: str, alias: str) -> bool:
        """
        Match a course alias safely.

        Prevents short aliases from accidentally matching
        inside unrelated words.
        """

        alias = alias.lower().strip()

        if " " in alias:
            return alias in query

        words = set(query.split())

        return alias in words