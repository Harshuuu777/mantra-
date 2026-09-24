"""
MANTRA - Voice Assistant

Connects:
    Microphone
        ↓
    Speech-to-Text
        ↓
    MANTRA Response Engine
        ↓
    Text-to-Speech
"""

from voice.speech import listen, speak
from brain.response_engine import ResponseEngine


def run_voice_assistant():
    """Start MANTRA voice conversation."""

    print("\n================================")
    print("        MANTRA VOICE ASSISTANT")
    print("================================")
    print("Speak naturally. Say 'exit' to stop.\n")

    # ---------------------------------------------------------
    # Initialize MANTRA Brain
    # ---------------------------------------------------------

    brain = ResponseEngine()

    # ---------------------------------------------------------
    # Startup greeting
    # ---------------------------------------------------------

    greeting = (
        "Hello! I am MANTRA, your college admission assistant. "
        "How can I help you?"
    )

    print(f"🤖 MANTRA: {greeting}")
    speak(greeting)

    # ---------------------------------------------------------
    # Main voice loop
    # ---------------------------------------------------------

    while True:

        # Listen to student
        user_input = listen()

        # -----------------------------------------------------
        # Microphone returned nothing
        # -----------------------------------------------------

        if not user_input:
            print("⚠️ I didn't hear anything.")
            continue

        print(f"👤 You: {user_input}")

        # -----------------------------------------------------
        # Exit commands
        # -----------------------------------------------------

        exit_words = {
            "exit",
            "quit",
            "bye",
            "goodbye",
            "close",
            "stop",
        }

        if user_input.lower().strip() in exit_words:

            response = brain.respond(user_input)

            print(f"🤖 MANTRA: {response}")
            speak(response)

            break

        # -----------------------------------------------------
        # Send student's question to MANTRA Brain
        # -----------------------------------------------------

        response = brain.respond(user_input)

        # -----------------------------------------------------
        # Display response
        # -----------------------------------------------------

        print(f"🤖 MANTRA: {response}")

        # -----------------------------------------------------
        # Speak response
        # -----------------------------------------------------

        speak(response)

    print("\n================================")
    print("      MANTRA VOICE OFFLINE")
    print("================================")


# =============================================================
# PROGRAM START
# =============================================================

if __name__ == "__main__":
    run_voice_assistant()