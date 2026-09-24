"""
MANTRA - STEP 35
Eligibility Data Updater

Adds verified eligibility information to existing
course records without deleting or replacing the
rest of college_data.json.
"""

import json
from pathlib import Path


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "data" / "college_data.json"


# =========================================================
# VERIFIED ELIGIBILITY
# =========================================================

BCA_ELIGIBILITY = (
    "Candidate must have passed HSC or equivalent examination "
    "and must have obtained a non-zero positive score in "
    "MAH BCA CET or another applicable equivalent entrance "
    "examination."
)


BTECH_ELIGIBILITY = (
    "For Maharashtra State candidates, the candidate must have "
    "passed HSC with Physics and Mathematics and any one of "
    "Chemistry, Biology, Biotechnology, Technical or Vocational "
    "subjects, with at least 50% marks (45% for reserved "
    "categories), and must have a valid MHT-CET or non-zero "
    "positive JEE Main score. A Diploma in Engineering with "
    "45% marks (40% for reserved categories) is also an "
    "acceptable route."
)


# =========================================================
# LOAD DATA
# =========================================================

def load_data():

    if not DATA_FILE.exists():

        raise FileNotFoundError(
            f"College data file not found:\n{DATA_FILE}"
        )

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# =========================================================
# UPDATE ELIGIBILITY
# =========================================================

def update_eligibility(data):

    courses = data.get("courses", [])

    if not courses:

        raise ValueError(
            "No courses found in college_data.json."
        )

    updated_courses = 0

    for course in courses:

        name = str(
            course.get("name", "")
        ).strip().lower()

        # -------------------------------------------------
        # BCA
        # -------------------------------------------------

        if name == "bca":

            course["eligibility"] = BCA_ELIGIBILITY

            updated_courses += 1

        # -------------------------------------------------
        # B.TECH COURSES
        # -------------------------------------------------

        elif name.startswith("b.tech"):

            course["eligibility"] = BTECH_ELIGIBILITY

            updated_courses += 1

    return updated_courses


# =========================================================
# SAVE DATA
# =========================================================

def save_data(data):

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

        file.write("\n")


# =========================================================
# VERIFY
# =========================================================

def verify_data(data):

    print()
    print("================================")
    print(" MANTRA ELIGIBILITY VERIFICATION")
    print("================================")
    print()

    for course in data.get("courses", []):

        name = course.get("name", "")
        eligibility = course.get(
            "eligibility",
            ""
        )

        if eligibility:

            print(f"✅ {name}")
            print(f"   {eligibility}")
            print()

        else:

            print(f"⚠️ {name}")
            print("   Eligibility not available.")
            print()


# =========================================================
# MAIN
# =========================================================

def main():

    print()
    print("================================")
    print(" MANTRA STEP 35")
    print(" ELIGIBILITY DATA UPDATE")
    print("================================")
    print()

    print(f"Data file:")
    print(DATA_FILE)
    print()

    try:

        data = load_data()

        updated_count = update_eligibility(
            data
        )

        save_data(data)

        print(
            f"✅ Eligibility updated for "
            f"{updated_count} course records."
        )

        verify_data(data)

        print()
        print(
            "✅ STEP 35A: ELIGIBILITY DATA UPDATED"
        )
        print()

    except Exception as error:

        print()
        print(
            "❌ ELIGIBILITY UPDATE FAILED"
        )

        print(
            f"Error: {error}"
        )

        print()


if __name__ == "__main__":
    main()