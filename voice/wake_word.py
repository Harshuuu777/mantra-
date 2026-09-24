"""
MANTRA - Wake Word System

Listens for the wake word:
    "Mantra"

Uses the existing speech recognition system.
"""

from voice.speech import listen


WAKE_WORDS = {
    "mantra",
    "hey mantra",
    "hello mantra",
}


def is_wake_word(text):
    """Check whether the recognized text contains a MANTRA wake word."""

    if not text:
        return False

    text = text.lower().strip()

    return any(
        wake_word == text or wake_word in text
        for wake_word in WAKE_WORDS
    )


def wait_for_wake_word():
    """Keep listening until MANTRA is detected."""

    print("\n💤 MANTRA is on standby...")
    print("🎤 Say 'Mantra' to wake me.")

    while True:
        text = listen()

        if not text:
            continue

        if is_wake_word(text):
            print("✨ WAKE WORD DETECTED!")
            return True


if __name__ == "__main__":
    wait_for_wake_word()