"""
MANTRA - Conversation Brain v2

Connects:
    Intent Router
    Course Extractor
    Database Manager
    Conversation Context
    Student Profile
    FAQ Database

Goals:
    - Natural conversation
    - Hinglish support
    - Short follow-up questions
    - Course context
    - Student name memory
    - Friendly responses
    - Voice-assistant friendly behaviour
    - Fast local processing
"""

import re

from brain.intent_router import IntentRouter
from brain.course_extractor import CourseExtractor
from database.manager import DatabaseManager


class ResponseEngine:
    """Generate friendly college-admission responses."""

    def __init__(self):

        self.router = IntentRouter()
        self.course_extractor = CourseExtractor()
        self.database = DatabaseManager()

        # =========================================================
        # CONVERSATION STATE
        # =========================================================

        self.current_course = None
        self.last_intent = None
        self.last_topic = None
        self.last_user_input = None
        self.turn_count = 0

        # =========================================================
        # STUDENT PROFILE
        # =========================================================

        self.student_name = None

    # =============================================================
    # TEXT NORMALIZATION
    # =============================================================

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Normalize text for matching."""

        if not text:
            return ""

        text = str(text).lower().strip()

        replacements = {
            "?": " ",
            "!": " ",
            ",": " ",
            ".": " ",
            ":": " ",
            ";": " ",
            "-": " ",
            "_": " ",
            "/": " ",
        }

        for old, new in replacements.items():
            text = text.replace(old, " ")

        return " ".join(text.split())

    # =============================================================
    # NAME EXTRACTION
    # =============================================================

    def _extract_student_name(self, user_input: str):
        """
        Extract a student's name from common English/Hinglish
        introductions.

        Examples:
            my name is Rahul
            my name's Rahul
            I am Rahul
            I'm Rahul
            mera naam Rahul hai
            main Rahul hoon
            Rahul naam hai mera
        """

        text = user_input.strip()

        patterns = [
            r"\bmy\s+name\s+is\s+([a-zA-Z][a-zA-Z]{1,20})\b",
            r"\bmy\s+name'?s\s+([a-zA-Z][a-zA-Z]{1,20})\b",
            r"\bi\s+am\s+([a-zA-Z][a-zA-Z]{1,20})\b",
            r"\bi'?m\s+([a-zA-Z][a-zA-Z]{1,20})\b",
            r"\bmera\s+naam\s+([a-zA-Z][a-zA-Z]{1,20})\s+hai\b",
            r"\bmera\s+naam\s+([a-zA-Z][a-zA-Z]{1,20})\b",
            r"\bmain\s+([a-zA-Z][a-zA-Z]{1,20})\s+hoon\b",
            r"\bmai\s+([a-zA-Z][a-zA-Z]{1,20})\s+hoon\b",
            r"\bme\s+([a-zA-Z][a-zA-Z]{1,20})\s+hoon\b",
            r"\b([a-zA-Z][a-zA-Z]{1,20})\s+naam\s+hai\s+mera\b",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                name = match.group(1).strip()
                name = name.rstrip(".,!?")

                if self._looks_like_name(name):
                    return name.title()

        return None

    @staticmethod
    def _looks_like_name(name: str) -> bool:
        """Basic protection against accidentally saving normal words."""

        blocked = {
            "what",
            "why",
            "how",
            "where",
            "when",
            "which",
            "please",
            "help",
            "student",
            "admission",
            "course",
            "bca",
            "fees",
            "documents",
            "eligibility",
            "scholarship",
        }

        name_lower = name.lower().strip()

        return (
            2 <= len(name_lower) <= 20
            and name_lower not in blocked
            and name_lower.isalpha()
        )

    # =============================================================
    # COURSE DETECTION
    # =============================================================

    def _detect_course(self, user_input: str):

        course = self.course_extractor.extract(
            user_input
        )

        if course:
            self.current_course = course

        return course

    # =============================================================
    # FOLLOW-UP INTENT
    # =============================================================

    def _detect_followup_intent(self, text: str):
        """
        Understand short/follow-up questions that keyword routing
        can sometimes miss.

        Examples:
            aur fees?
            fees?
            aur documents?
            documents?
            eligibility?
            iska process?
            iska kya scene hai?
        """

        text = self._normalize_text(text)

        if not text:
            return None

        # ---------------------------------------------------------
        # FEES
        # ---------------------------------------------------------

        fee_words = {
            "fee",
            "fees",
            "cost",
            "charges",
            "kharcha",
            "paisa",
            "paise",
            "kitna",
            "kitne",
        }

        if any(word in text.split() for word in fee_words):

            # "kitna" alone is ambiguous.
            if text.strip() == "kitna":
                if self.last_intent == "FEES_QUERY":
                    return "FEES_QUERY"
            else:
                return "FEES_QUERY"

        # ---------------------------------------------------------
        # DOCUMENTS
        # ---------------------------------------------------------

        document_words = {
            "document",
            "documents",
            "docs",
            "doc",
            "papers",
            "paper",
            "kagaz",
            "certificate",
            "certificates",
        }

        if any(word in text.split() for word in document_words):
            return "DOCUMENT_QUERY"

        # ---------------------------------------------------------
        # ELIGIBILITY
        # ---------------------------------------------------------

        eligibility_words = {
            "eligibility",
            "eligible",
            "qualification",
            "criteria",
            "marks",
            "percentage",
            "qualification",
        }

        if any(word in text.split() for word in eligibility_words):
            return "ELIGIBILITY_QUERY"

        # ---------------------------------------------------------
        # SCHOLARSHIP
        # ---------------------------------------------------------

        scholarship_words = {
            "scholarship",
            "scholarships",
            "scholar",
            "stipend",
            "madhat",
        }

        if any(word in text.split() for word in scholarship_words):
            return "SCHOLARSHIP_QUERY"

        # ---------------------------------------------------------
        # PROCESS
        # ---------------------------------------------------------

        process_words = {
            "process",
            "steps",
            "procedure",
            "processes",
            "kaise",
            "kese",
            "aise",
        }

        if any(word in text.split() for word in process_words):

            if (
                "admission" in text
                or self.last_intent == "ADMISSION_PROCESS_QUERY"
            ):
                return "ADMISSION_PROCESS_QUERY"

        # Natural admission-process follow-ups.
        process_followups = {
            "admission kaise hoga",
            "admission kese hoga",
            "admission kaise hoga isme",
            "admission kese hoga isme",
            "isme admission kaise hoga",
            "isme admission kese hoga",
            "iske liye admission kaise hoga",
            "iske liye admission kese hoga",
            "admission kaise milega",
            "admission kese milega",
        }

        if text in process_followups:
            return "ADMISSION_PROCESS_QUERY"

        # ---------------------------------------------------------
        # COURSE / DURATION
        # ---------------------------------------------------------

        course_words = {
            "course",
            "courses",
            "degree",
            "branch",
            "branches",
            "duration",
            "years",
        }

        if any(word in text.split() for word in course_words):
            return "COURSE_QUERY"

        # ---------------------------------------------------------
        # NATURAL ELIGIBILITY FOLLOW-UPS
        # ---------------------------------------------------------

        eligibility_followups = {
            "main eligible hu",
            "kya main eligible hu",
            "mai eligible hu",
            "kya mai eligible hu",
            "main eligible hoon",
            "kya main eligible hoon",
            "kitne percentage chahiye",
            "kitna percentage chahiye",
            "kitne percent chahiye",
            "kitna percent chahiye",
            "minimum percentage kitna chahiye",
            "minimum percentage kitne chahiye",
            "iske liye kya qualification chahiye",
            "is ke liye kya qualification chahiye",
            "kya qualification chahiye",
            "qualification kya chahiye",
        }

        if text in eligibility_followups:
            if self.current_course or self.last_intent in {
                "COURSE_QUERY",
                "ADMISSION_QUERY",
                "ELIGIBILITY_QUERY",
            }:
                return "ELIGIBILITY_QUERY"

        return None

    # =============================================================
    # NATURAL LANGUAGE INTENT
    # =============================================================

    def _understand_intent(self, user_input: str):
        """
        Main intent understanding layer.

        Existing IntentRouter remains the first source.
        Follow-up understanding is used as a safety layer.
        """

        intent = self.router.detect(user_input)

        followup_intent = self._detect_followup_intent(
            user_input
        )

        if intent == "UNKNOWN" and followup_intent:
            return followup_intent

        return intent

    # =============================================================
    # FAQ SEARCH
    # =============================================================

    def _find_faq_answer(self, user_input: str):

        faqs = self.database.get_faqs()

        if not faqs:
            return None

        query = self._normalize_text(user_input)
        query_words = set(query.split())

        stop_words = {
            "the",
            "is",
            "a",
            "an",
            "are",
            "am",
            "i",
            "me",
            "my",
            "you",
            "your",
            "hai",
            "h",
            "kya",
            "ka",
            "ke",
            "ki",
            "ko",
            "mein",
            "me",
            "mujhe",
            "batao",
            "bata",
            "please",
            "about",
            "tell",
            "what",
            "where",
            "which",
            "can",
            "do",
            "aur",
            "bhi",
            "ye",
            "yeh",
            "iska",
            "iske",
            "milega",
        }

        meaningful_query_words = {
            word
            for word in query_words
            if len(word) > 2
            and word not in stop_words
        }

        best_answer = None
        best_score = 0

        for faq in faqs:

            question = faq.get("question", "")
            answer = faq.get("answer", "")

            if not question or not answer:
                continue

            faq_question = self._normalize_text(
                question
            )

            if query == faq_question:
                return answer

            faq_words = set(
                faq_question.split()
            )

            meaningful_faq_words = {
                word
                for word in faq_words
                if len(word) > 2
                and word not in stop_words
            }

            common_words = (
                meaningful_query_words
                .intersection(
                    meaningful_faq_words
                )
            )

            score = len(common_words)

            if score > best_score:

                best_score = score
                best_answer = answer

        if best_score >= 1:
            return best_answer

        return None

    # =============================================================
    # CLEAN TEXT
    # =============================================================

    @staticmethod
    def _clean_sentence(text: str) -> str:

        if not text:
            return ""

        text = " ".join(
            str(text).split()
        )

        text = re.sub(
            r"\.{2,}",
            ".",
            text
        )

        text = re.sub(
            r"\?{2,}",
            "?",
            text
        )

        text = re.sub(
            r"!{2,}",
            "!",
            text
        )

        text = re.sub(
            r"\s+([,.!?;:])",
            r"\1",
            text
        )

        return text.strip()

    # =============================================================
    # DURATION
    # =============================================================

    @staticmethod
    def _format_duration(duration: str) -> str:

        if not duration:
            return ""

        duration = str(duration).strip()

        duration = re.sub(
            r"(\d+)\s*(Years?)",
            r"\1 \2",
            duration,
            flags=re.IGNORECASE
        )

        duration = re.sub(
            r"(\d+)\s*(year)",
            r"\1 \2",
            duration,
            flags=re.IGNORECASE
        )

        duration = re.sub(
            r"\s*Full\s*Time",
            " Full Time",
            duration,
            flags=re.IGNORECASE
        )

        return " ".join(
            duration.split()
        )

    # =============================================================
    # PERIOD
    # =============================================================

    @staticmethod
    def _add_period(text: str) -> str:

        if not text:
            return ""

        text = text.strip()

        if text.endswith(
            (".", "!", "?")
        ):
            return text

        return text + "."

    # =============================================================
    # NAME PREFIX
    # =============================================================

    def _name_prefix(self):

        if self.student_name:
            return f"{self.student_name}, "

        return ""

    # =============================================================
    # MAIN RESPONSE
    # =============================================================

    def respond(self, user_input: str) -> str:
        """
        Process one conversation turn.
        """

        if not user_input:
            return (
                "I didn't catch that. "
                "Could you say it again?"
            )

        user_input = str(
            user_input
        ).strip()

        if not user_input:
            return (
                "I didn't catch that. "
                "Could you say it again?"
            )

        # ---------------------------------------------------------
        # TURN MEMORY
        # ---------------------------------------------------------

        self.turn_count += 1
        self.last_user_input = user_input

        # ---------------------------------------------------------
        # NAME
        # ---------------------------------------------------------

        detected_name = (
            self._extract_student_name(
                user_input
            )
        )

        if detected_name:

            self.student_name = detected_name

            if self.current_course:

                return (
                    f"Nice to meet you, "
                    f"{self.student_name}! 😊 "
                    f"I'll remember that you're "
                    f"interested in "
                    f"{self.current_course.upper()}. "
                    "What would you like to know?"
                )

            return (
                f"Nice to meet you, "
                f"{self.student_name}! 😊 "
                "What would you like to know "
                "about admission?"
            )

        # ---------------------------------------------------------
        # COURSE
        # ---------------------------------------------------------

        self._detect_course(
            user_input
        )

        # ---------------------------------------------------------
        # INTENT
        # ---------------------------------------------------------

        intent = self._understand_intent(
            user_input
        )

        self.last_intent = intent

        # ---------------------------------------------------------
        # TOPIC MEMORY
        # ---------------------------------------------------------

        topic_map = {
            "COURSE_QUERY": "course",
            "FEES_QUERY": "fees",
            "DOCUMENT_QUERY": "documents",
            "ELIGIBILITY_QUERY": "eligibility",
            "SCHOLARSHIP_QUERY": "scholarship",
            "ADMISSION_PROCESS_QUERY": "admission process",
            "ADMISSION_QUERY": "admission",
            "FAQ_QUERY": "college information",
        }

        if intent in topic_map:
            self.last_topic = topic_map[intent]

        # =========================================================
        # GREETING
        # =========================================================

        if intent == "GREETING":

            if self.student_name:

                return (
                    f"Hello again, "
                    f"{self.student_name}! 👋 "
                    "What can I help you with?"
                )

            return (
                "Hello! 👋 Welcome to G H Raisoni "
                "College of Engineering & Management, "
                "Jalgaon. How can I help you with "
                "admission?"
            )

        # =========================================================
        # THANK YOU
        # =========================================================

        if intent == "THANK_YOU":

            if self.student_name:

                return (
                    f"You're welcome, "
                    f"{self.student_name}! 😊"
                )

            return (
                "You're welcome! 😊 "
                "I'm happy to help."
            )

        # =========================================================
        # GOODBYE
        # =========================================================

        if intent == "GOODBYE":

            if self.student_name:

                return (
                    f"Goodbye, "
                    f"{self.student_name}! 👋 "
                    "All the best for your admission!"
                )

            return (
                "Goodbye! 👋 "
                "All the best for your admission!"
            )

        # =========================================================
        # FAQ
        # =========================================================

        if intent == "FAQ_QUERY":

            answer = self._find_faq_answer(
                user_input
            )

            if answer:
                return self._clean_sentence(
                    answer
                )

            return self._friendly_unknown_response()

        # =========================================================
        # COURSE
        # =========================================================

        if intent == "COURSE_QUERY":

            return self._course_response(
                user_input
            )

        # =========================================================
        # FEES
        # =========================================================

        if intent == "FEES_QUERY":

            return self._fee_response(
                user_input
            )

        # =========================================================
        # DOCUMENTS
        # =========================================================

        if intent == "DOCUMENT_QUERY":

            return self._document_response(
                user_input
            )

        # =========================================================
        # ELIGIBILITY
        # =========================================================

        if intent == "ELIGIBILITY_QUERY":

            return self._eligibility_response(
                user_input
            )

        # =========================================================
        # ADMISSION PROCESS
        # =========================================================

        if intent == "ADMISSION_PROCESS_QUERY":

            return self._admission_process_response()

        # =========================================================
        # SCHOLARSHIP
        # =========================================================

        if intent == "SCHOLARSHIP_QUERY":

            faq_answer = self._find_faq_answer(
                user_input
            )

            if faq_answer:

                return self._clean_sentence(
                    faq_answer
                )

            return (
                "Yes 😊 Scholarship opportunities may "
                "be available depending on your "
                "eligibility and the applicable scheme. "
                "The current scheme and eligibility "
                "should be verified with the college."
            )

        # =========================================================
        # ADMISSION
        # =========================================================

        if intent == "ADMISSION_QUERY":

            if self.current_course:

                if self.student_name:

                    return (
                        f"Sure, {self.student_name}! 😊 "
                        f"I can help you with your "
                        f"{self.current_course.upper()} "
                        "admission — documents, "
                        "eligibility, fees, scholarship, "
                        "or the admission process. "
                        "What do you want to know?"
                    )

                return (
                    f"Sure! 😊 I can help you with "
                    f"{self.current_course.upper()} "
                    "admission — documents, eligibility, "
                    "fees, scholarship, or the admission "
                    "process. What do you want to know?"
                )

            if self.student_name:

                return (
                    f"Sure, {self.student_name}! 😊 "
                    "Tell me which course you're "
                    "interested in, and I'll help "
                    "you with the admission details."
                )

            return (
                "Sure! 😊 Tell me which course you're "
                "interested in, and I'll help you "
                "with the admission details."
            )

        # =========================================================
        # UNKNOWN
        # =========================================================

        return self._friendly_unknown_response()

    # =============================================================
    # COURSE RESPONSE
    # =============================================================

    def _course_response(
        self,
        user_input: str
    ) -> str:

        course = (
            self.course_extractor.extract(
                user_input
            )
        )

        if course:
            self.current_course = course

        else:
            course = self.current_course

        if course:

            courses = self.database.search_course(
                course
            )

            if courses:

                course_data = courses[0]

                course_name = self._clean_sentence(
                    course_data.get(
                        "name",
                        course.upper()
                    )
                )

                duration = self._format_duration(
                    course_data.get(
                        "duration",
                        ""
                    )
                )

                eligibility = self._clean_sentence(
                    course_data.get(
                        "eligibility",
                        ""
                    )
                )

                description = self._clean_sentence(
                    course_data.get(
                        "description",
                        ""
                    )
                )

                response = (
                    f"{course_name} is available at "
                    "G H Raisoni College of Engineering "
                    "& Management, Jalgaon."
                )

                if duration:

                    response += (
                        f" The duration is {duration}."
                    )

                if (
                    eligibility
                    and eligibility.lower()
                    not in {
                        "as per applicable admission rules",
                        "as per applicable admission rules.",
                    }
                ):

                    response += (
                        " Eligibility: "
                        + self._add_period(
                            eligibility
                        )
                    )

                if description:

                    response += (
                        " "
                        + self._add_period(
                            description
                        )
                    )

                return self._clean_sentence(
                    response
                )

            return (
                f"I understood that you're asking "
                f"about {course.upper()}, but I don't "
                "currently have verified information "
                "about this course in my database."
            )

        # ---------------------------------------------------------
        # No course
        # ---------------------------------------------------------

        courses = self.database.get_courses()

        if not courses:

            return (
                "Course information is currently "
                "unavailable in my database."
            )

        names = []

        for course_data in courses:

            name = self._clean_sentence(
                course_data.get(
                    "name",
                    ""
                )
            )

            if name:
                names.append(name)

        if not names:

            return (
                "Course information is currently "
                "unavailable in my database."
            )

        return (
            "I currently have information about: "
            + ", ".join(names)
            + ". Which course are you interested in?"
        )

    # =============================================================
    # FEES RESPONSE
    # =============================================================

    def _fee_response(
        self,
        user_input: str
    ) -> str:

        course = (
            self.course_extractor.extract(
                user_input
            )
        )

        if course:
            self.current_course = course

        else:
            course = self.current_course

        if course:

            if self.student_name:

                return (
                    f"{self.student_name}, you're asking "
                    f"about the fees for "
                    f"{course.upper()}. "
                    "I don't have verified current fee "
                    "information in my database right now."
                )

            return (
                f"You're asking about the fees for "
                f"{course.upper()}. "
                "I don't have verified current fee "
                "information in my database right now."
            )

        return (
            "I don't have verified current fee "
            "information in my database right now. "
            "If you tell me the course, I can keep "
            "that context for the next questions."
        )

    # =============================================================
    # DOCUMENT RESPONSE
    # =============================================================

    def _document_response(
        self,
        user_input: str
    ) -> str:

        course = (
            self.course_extractor.extract(
                user_input
            )
        )

        if course:
            self.current_course = course

        course = course or self.current_course

        documents = self.database.get_documents(
            course_name=course
        )

        if not documents:

            return (
                "I don't currently have verified "
                "document information for that "
                "course."
            )

        names = []

        for document in documents:

            name = self._clean_sentence(
                document.get(
                    "document_name",
                    ""
                )
            )

            if name:
                names.append(name)

        if not names:

            return (
                "Required document information is "
                "currently unavailable."
            )

        document_text = ", ".join(
            names
        )

        if course:

            if self.student_name:

                return (
                    f"{self.student_name}, for "
                    f"{course.upper()} admission, "
                    "the required documents include: "
                    + document_text
                    + "."
                )

            return (
                f"For {course.upper()} admission, "
                "the required documents include: "
                + document_text
                + "."
            )

        return (
            "The required documents include: "
            + document_text
            + "."
        )

    # =============================================================
    # ELIGIBILITY RESPONSE
    # =============================================================

    def _eligibility_response(
        self,
        user_input: str
    ) -> str:

        course = (
            self.course_extractor.extract(
                user_input
            )
        )

        if course:
            self.current_course = course

        else:
            course = self.current_course

        if course:

            courses = self.database.search_course(
                course
            )

            if courses:

                course_data = courses[0]

                eligibility = self._clean_sentence(
                    course_data.get(
                        "eligibility",
                        ""
                    )
                )

                if (
                    eligibility
                    and eligibility.lower()
                    not in {
                        "as per applicable admission rules",
                        "as per applicable admission rules.",
                    }
                ):

                    return (
                        f"For {course_data.get('name', course.upper())}, "
                        "the eligibility is: "
                        + self._add_period(
                            eligibility
                        )
                    )

        return (
            "I don't currently have verified "
            "eligibility information for that course."
        )

    # =============================================================
    # ADMISSION PROCESS
    # =============================================================

    def _admission_process_response(self):

        steps = (
            self.database.get_admission_process()
        )

        if not steps:

            return (
                "The admission process information "
                "is currently unavailable."
            )

        response_parts = [
            "Sure! 😊 The admission process is:"
        ]

        for step in steps:

            step_number = step.get(
                "step_number",
                ""
            )

            title = self._clean_sentence(
                step.get(
                    "title",
                    ""
                )
            )

            description = self._clean_sentence(
                step.get(
                    "description",
                    ""
                )
            )

            description = self._add_period(
                description
            )

            response_parts.append(
                f"Step {step_number}: "
                f"{title}. "
                f"{description}"
            )

        return " ".join(
            response_parts
        )

    # =============================================================
    # FRIENDLY UNKNOWN
    # =============================================================

    def _friendly_unknown_response(self):

        if self.student_name:

            if self.current_course:

                return (
                    f"{self.student_name}, I'm with you. 😊 "
                    f"You're asking about "
                    f"{self.current_course.upper()} "
                    "admission. You can ask me about "
                    "fees, documents, eligibility, "
                    "scholarship, course details, "
                    "or the admission process."
                )

            return (
                f"{self.student_name}, I'm here to help! 😊 "
                "You can ask me about courses, "
                "eligibility, documents, fees, "
                "scholarships, or the admission process."
            )

        return (
            "I'm here to help! 😊 You can ask me "
            "about courses, eligibility, documents, "
            "fees, scholarships, or the admission process."
        )

    # =============================================================
    # STUDENT PROFILE
    # =============================================================

    def get_student_profile(self):

        return {
            "name": self.student_name,
            "course": self.current_course,
            "last_intent": self.last_intent,
            "last_topic": self.last_topic,
            "turn_count": self.turn_count,
        }

    # =============================================================
    # CURRENT COURSE
    # =============================================================

    def get_current_course(self):

        return self.current_course

    # =============================================================
    # LAST TOPIC
    # =============================================================

    def get_last_topic(self):

        return self.last_topic

    # =============================================================
    # CLEAR CONTEXT
    # =============================================================

    def clear_context(self):

        self.current_course = None
        self.last_intent = None
        self.last_topic = None
        self.last_user_input = None
        self.turn_count = 0
        self.student_name = None