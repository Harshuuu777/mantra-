"""
MANTRA - Smart Intent Router v2

Fast local intent detection for:
English + Hindi + Hinglish + common voice/STT variations.
"""


class IntentRouter:
    """Detect the purpose of a student's question."""

    INTENTS = {

        # =========================================================
        # GREETING
        # =========================================================

        "GREETING": [
            "hello",
            "hi",
            "hey",
            "namaste",
            "namaskar",
            "good morning",
            "good afternoon",
            "good evening",
            "hii",
            "hiii",
            "helo",
            "helloo",
        ],

        # =========================================================
        # THANK YOU
        # =========================================================

        "THANK_YOU": [
            "thank you",
            "thanks",
            "thank u",
            "thankyou",
            "thankyou so much",
            "thanks a lot",
            "dhanyawad",
            "dhanyavad",
            "shukriya",
            "bahut thanks",
            "thanks bro",
            "thank you bro",
        ],

        # =========================================================
        # GOODBYE
        # =========================================================

        "GOODBYE": [
            "bye",
            "goodbye",
            "good bye",
            "see you",
            "see ya",
            "take care",
            "phir milte hain",
            "fir milte hain",
            "milte hain",
            "exit",
            "quit",
            "close",
            "stop",
        ],

        # =========================================================
        # FAQ / COLLEGE INFORMATION
        # =========================================================

        "FAQ_QUERY": [
            "college kaha",
            "college kahan",
            "college kaha hai",
            "college kahan hai",
            "college kidhar",
            "college kidhar hai",
            "college location",
            "college ka address",
            "college address",
            "address",
            "location",
            "contact",
            "contact number",
            "contact no",
            "phone number",
            "phone no",
            "mobile number",
            "mobile no",
            "email",
            "email id",
            "email address",
            "website",
            "official website",
            "college ke bare",
            "college ke baare",
            "college ke bare me",
            "college ke baare me",
            "college information",
            "college info",
            "college timing",
            "college timings",
            "college time",
            "working hours",
            "office timing",
            "office timings",
            "campus",
            "campus kaha",
            "campus kahan",
            "hostel",
            "hostel hai",
            "hostel available",
            "bus",
            "bus facility",
            "transport",
            "transport facility",
            "library",
            "canteen",
            "placement",
            "placements",
            "placement hai",
        ],

        # =========================================================
        # COURSE
        # =========================================================

        "COURSE_QUERY": [
            "course",
            "courses",
            "program",
            "programs",
            "degree",
            "degrees",
            "branch",
            "branches",
            "stream",
            "streams",

            "bca",
            "bba",
            "mca",
            "mba",

            "b tech",
            "b.tech",
            "btech",
            "m tech",
            "m.tech",
            "mtech",

            "computer engineering",
            "computer science",
            "information technology",
            "information tech",
            "mechanical engineering",
            "civil engineering",
            "electrical engineering",
            "electronics",
            "telecommunication",
            "electronics and telecommunication",

            "data science",
            "artificial intelligence",
            "machine learning",
            "ai ml",
            "ai and ml",
            "cyber security",
            "cybersecurity",

            "available hai",
            "available h",
            "available hai kya",
            "available h kya",
            "course hai",
            "course hai kya",
            "kaunse course",
            "konse course",
            "konsa course",
            "kaunsa course",
            "mujhe bca chahiye",
            "mujhe bba chahiye",
            "mujhe mca chahiye",
            "mujhe mba chahiye",
            "mujhe btech chahiye",
            "mujhe b tech chahiye",
            "mujhe mtech chahiye",
            "mujhe m tech chahiye",
        ],

        # =========================================================
        # FEES
        # =========================================================

        "FEES_QUERY": [
            "fee",
            "fees",
            "fee structure",
            "fees structure",
            "fees ka structure",
            "fee ka structure",

            "kitna paisa",
            "kitne paise",
            "kitni fees",
            "fees kitni",
            "fee kitni",
            "fees kitne",
            "fee kitne",

            "fees kitna",
            "fee kitna",
            "kitna fee",
            "kitna fees",

            "cost",
            "price",
            "charges",
            "tuition",
            "tuition fee",
            "tuition fees",
            "payment",

            "paisa lagega",
            "paise lagenge",
            "kitna paisa lagega",
            "kitne paise lagenge",

            "fee deni hai",
            "fees deni hai",
            "fee bharni hai",
            "fees bharni hai",
            "fee pay",
            "fees pay",
            "fee batao",
            "fees batao",
            "fees bataiye",
            "fee bataiye",

            # Follow-up
            "aur fee",
            "aur fees",
            "aur fee batao",
            "aur fees batao",
            "fees bhi",
            "fee bhi",
            "iski fees",
            "iska fee",
            "iska fees",
            "fees kitni hai",
            "fee kitni hai",
            "fees batao",
            "fee batao",
        ],

        # =========================================================
        # DOCUMENTS
        # =========================================================

        "DOCUMENT_QUERY": [
            "document",
            "documents",
            "doc",
            "docs",
            "paper",
            "papers",
            "certificate",
            "certificates",
            "marksheet",
            "marksheets",
            "mark sheet",
            "mark sheets",

            "marksheet chahiye",
            "marksheets chahiye",
            "document chahiye",
            "documents chahiye",
            "docs chahiye",
            "papers chahiye",

            "kya documents",
            "kaunse documents",
            "konse documents",
            "konsa document",
            "kaunsa document",
            "documents lagenge",
            "document lagenge",
            "papers lagenge",

            "kya kya chahiye",
            "kya chahiye",
            "kya kya lagega",
            "kya lagega",
            "kaunse paper",
            "konse paper",

            # Follow-up
            "aur document",
            "aur documents",
            "aur docs",
            "documents bhi",
            "document bhi",
            "docs bhi",
            "papers bhi",
            "iske documents",
            "iske docs",
            "iske papers",
            "iske certificates",
            "iske liye documents",
            "iske liye docs",
            "iske liye papers",
            "iske liye kaunse documents",
            "iske liye konse documents",
            "iske liye kya documents",
        ],

        # =========================================================
        # ELIGIBILITY
        # =========================================================

        "ELIGIBILITY_QUERY": [
            "eligibility",
            "eligible",
            "eligibility criteria",
            "qualification",
            "qualifications",
            "criteria",
            "percentage",
            "percent",
            "percentage required",
            "marks required",
            "minimum marks",
            "minimum percentage",
            "kitne marks",
            "kitna percentage",
            "kitni percentage",
            "kitna percent",
            "kitni percent",

            "eligible hu",
            "eligible hoon",
            "eligible hun",
            "eligible hai",
            "mai eligible",
            "main eligible",

            "12th ke baad",
            "12th pass",
            "12th passed",
            "hsc pass",
            "hsc passed",

            "qualification kya",
            "qualification kya hai",
            "criteria kya",
            "criteria kya hai",
            "eligibility kya",
            "eligibility kya hai",

            # Follow-up
            "aur eligibility",
            "eligibility bhi",
            "qualification bhi",
            "criteria bhi",
            "iske liye eligibility",
            "iske liye qualification",
            "iske liye kya qualification",
            "iske liye kitne marks",
            "iske liye kitna percentage",
            "main iske liye eligible",
        ],

        # =========================================================
        # ADMISSION PROCESS
        # =========================================================

        "ADMISSION_PROCESS_QUERY": [
            "admission process",
            "admission ka process",
            "admission kaise process",
            "admission kese process",
            "admission procedure",
            "admission ki process",
            "admission ka procedure",
            "admission ki procedure",

            "procedure",
            "process",
            "steps",
            "admission steps",

            "admission kaise",
            "admission kese",
            "admission kaise milega",
            "admission kese milega",

            "admission kaise lena",
            "admission kese lena",
            "admission kaise le",
            "admission kese le",

            "apply kaise",
            "apply kese",
            "application kaise",
            "application kese",

            "form kaise",
            "form kese",
            "form bharna",
            "form kaise bharna",
            "form kese bharna",

            "registration kaise",
            "registration kese",
            "registration process",

            # Follow-up
            "aur process",
            "aur admission process",
            "process bhi",
            "steps bhi",
            "procedure bhi",
        ],

        # =========================================================
        # SCHOLARSHIP
        # =========================================================

        "SCHOLARSHIP_QUERY": [
            "scholarship",
            "scholarships",
            "scholarship hai",
            "scholarship hai kya",
            "scholarship milegi",
            "scholarship available",
            "scholarship available hai",
            "scholarship kaise",
            "scholarship kaise milegi",
            "scholarship eligibility",

            "financial aid",
            "fee concession",
            "fees concession",
            "concession",
            "financial help",

            # Follow-up
            "aur scholarship",
            "iske liye scholarship",
            "is course ki scholarship",
            "is course ke liye scholarship",
            "scholarship milega",
            "scholarship mil sakti hai",
            "scholarship bhi",
            "aur scholarships",
        ],

        # =========================================================
        # GENERAL ADMISSION
        # =========================================================

        "ADMISSION_QUERY": [
            "admission",
            "admit",
            "apply",
            "application",
            "enroll",
            "enrolment",
            "enrollment",
            "registration",

            "admission chahiye",
            "admission lena hai",
            "admission leni hai",
            "admission lena",
            "admission leni",
            "admission ke liye",
            "admission karna hai",
            "admission karwana hai",

            "mujhe admission chahiye",
            "mujhe admission lena hai",
            "mujhe admission leni hai",
        ],
    }

    # =============================================================
    # COURSE DURATION
    # =============================================================

    DURATION_WORDS = [
        "duration",
        "kitne saal",
        "kitne sal",
        "kitne saal ka",
        "kitne sal ka",
        "kitne years",
        "how many years",
        "years ka",
        "year ka",
        "years ki",
        "year ki",
        "saal ka",
        "saal ki",
        "sal ka",
        "sal ki",
        "kitna time",
        "kitne time",
        "course kitne saal",
        "course kitne years",
        "kitna duration",
        "course ka duration",
        "course ki duration",
        "kitne years ka course",
        "kitne saal ka course",
        "ye course kitne saal ka",
        "ye kitne saal ka hai",
    ]

    # =============================================================
    # NORMALIZATION
    # =============================================================

    @staticmethod
    def _normalize(text: str) -> str:
        """
        Normalize common speech-to-text variations.
        """

        text = str(text).lower().strip()

        # Common punctuation → spaces
        replacements = {
            "?": " ",
            "!": " ",
            ",": " ",
            ".": " ",
            ":": " ",
            ";": " ",
            "-": " ",
            "_": " ",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        # ---------------------------------------------------------
        # Common STT course spellings
        # ---------------------------------------------------------

        text = text.replace("b c a", "bca")
        text = text.replace("b c a.", "bca")
        text = text.replace("b c a ", "bca ")

        text = text.replace("b tech", "btech")
        text = text.replace("m tech", "mtech")

        # ---------------------------------------------------------
        # Common Hindi/Hinglish spelling variations
        # ---------------------------------------------------------

        replacements = {
            "kese": "kaise",
            "konse": "kaunse",
            "konsa": "kaunsa",
            "kidhar": "kahan",
            "hun": "hoon",
            "krna": "karna",
            "kr": "kar",
            "chahiye": "chahiye",
        }

        words = text.split()

        normalized_words = [
            replacements.get(word, word)
            for word in words
        ]

        text = " ".join(normalized_words)

        # ---------------------------------------------------------
        # Collapse repeated spaces
        # ---------------------------------------------------------

        return " ".join(text.split())

    # =============================================================
    # MAIN DETECTOR
    # =============================================================

    def detect(self, user_input: str) -> str:

        if not user_input or not str(user_input).strip():
            return "UNKNOWN"

        query = self._normalize(user_input)

        # ---------------------------------------------------------
        # Exact commands
        # ---------------------------------------------------------

        if query in {
            "exit",
            "quit",
            "close",
            "bye",
            "goodbye",
            "good bye",
            "stop",
        }:
            return "GOODBYE"

        # ---------------------------------------------------------
        # Greeting
        # ---------------------------------------------------------

        if self._contains_any(
            query,
            self.INTENTS["GREETING"]
        ):
            return "GREETING"

        # ---------------------------------------------------------
        # Thank You
        # ---------------------------------------------------------

        if self._contains_any(
            query,
            self.INTENTS["THANK_YOU"]
        ):
            return "THANK_YOU"

        # ---------------------------------------------------------
        # Goodbye
        # ---------------------------------------------------------

        if self._contains_any(
            query,
            self.INTENTS["GOODBYE"]
        ):
            return "GOODBYE"

        # ---------------------------------------------------------
        # Duration
        # ---------------------------------------------------------

        if self._contains_any(
            query,
            self.DURATION_WORDS
        ):
            return "COURSE_QUERY"

        # ---------------------------------------------------------
        # Specific intents first
        #
        # Important:
        # Documents / fees / eligibility etc. are checked before
        # general admission and course queries.
        # ---------------------------------------------------------

        priority = [
            "DOCUMENT_QUERY",
            "FEES_QUERY",
            "ELIGIBILITY_QUERY",
            "SCHOLARSHIP_QUERY",
            "ADMISSION_PROCESS_QUERY",
            "FAQ_QUERY",
            "COURSE_QUERY",
            "ADMISSION_QUERY",
        ]

        for intent in priority:

            if self._contains_any(
                query,
                self.INTENTS[intent]
            ):
                return intent

        return "UNKNOWN"

    # =============================================================
    # KEYWORD MATCHING
    # =============================================================

    @staticmethod
    def _contains_any(
        query: str,
        keywords: list[str]
    ) -> bool:

        words = set(query.split())

        for keyword in keywords:

            keyword = keyword.lower().strip()

            if not keyword:
                continue

            # Multi-word phrase
            if " " in keyword:

                if keyword in query:
                    return True

            # Single word
            else:

                if keyword in words:
                    return True

        return False


# ================================================================
# DIRECT TEST
# ================================================================

if __name__ == "__main__":

    router = IntentRouter()

    test_queries = [
        "hello",
        "thank you",
        "bye",

        "BCA",
        "B C A",
        "b tech",

        "fees kitni hai",
        "fee batao",
        "aur fees",

        "documents kya lagenge",
        "docs chahiye",
        "papers kya chahiye",

        "eligibility kya hai",
        "kitne percentage chahiye",

        "scholarship hai kya",
        "aur scholarship",

        "admission kaise lena hai",
        "admission process",

        "college kaha hai",
        "college kidhar hai",
        "address",
        "contact number",

        "BCA kitne saal ka hai",

        "random question",
    ]

    print("\n========================================")
    print("       MANTRA INTENT ROUTER V2")
    print("========================================\n")

    for query in test_queries:

        intent = router.detect(query)

        print(f"👤 {query}")
        print(f"🧠 {intent}")
        print("-" * 40)