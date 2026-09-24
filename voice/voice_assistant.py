"""
MANTRA - Wake Word Voice Assistant

Flow:

Standby
   ↓
Wake Word: "Mantra"
   ↓
MANTRA activates
   ↓
User speaks
   ↓
Response Engine
   ↓
MANTRA speaks
   ↓
Back to standby
"""

from voice.speech import listen, speak
from voice.wake_word import wait_for_wake_word
from brain.response_engine import ResponseEngine


def run_voice_assistant():
    print("\n================================")
    print("   MANTRA WAKE-WORD ASSISTANT")
    print("================================")
    print("Say 'Mantra' to activate MANTRA.")
    print("Say 'bye' or 'exit' during conversation to stop.\n")

    # Create ONE brain instance.
    # This keeps name and conversation context alive.
    brain = ResponseEngine()

    while True:

        # -----------------------------
        # STANDBY MODE
        # -----------------------------
        try:
            wait_for_wake_word()
        except KeyboardInterrupt:
            print("\n\n🛑 MANTRA stopped by user.")
            break
        except Exception as error:
            print(f"❌ Wake word error: {error}")
            continue

        # -----------------------------
        # ACTIVE MODE
        # -----------------------------
        print("\n✨ MANTRA ACTIVATED!")

        activation_message = (
            "Yes! 👋 I am listening. "
            "How can I help you with admission?"
        )

        print(f"🤖 MANTRA: {activation_message}")
        speak(activation_message)

        # -----------------------------
        # CONVERSATION LOOP
        # -----------------------------
        while True:

            try:
                user_input = listen()
            except KeyboardInterrupt:
                print("\n\n🛑 MANTRA stopped by user.")
                return
            except Exception as error:
                print(f"❌ Listening error: {error}")
                continue

            if not user_input:
                print("⚠️ I didn't hear anything.")
                continue

            print(f"👤 You: {user_input}")

            # -----------------------------
            # EXIT CHECK
            # -----------------------------
            exit_words = {
                "exit",
                "quit",
                "bye",
                "goodbye",
                "close",
                "stop",
            }

            normalized_input = user_input.lower().strip()

            if normalized_input in exit_words:

                response = brain.respond(user_input)

                print(f"🤖 MANTRA: {response}")
                speak(response)

                print("\n💤 Returning to standby...")
                break

            # -----------------------------
            # MANTRA BRAIN
            # -----------------------------
            response = brain.respond(user_input)

            print(f"🤖 MANTRA: {response}")
            speak(response)

        # After conversation ends,
        # MANTRA goes back to standby.


if __name__ == "__main__":
    run_voice_assistant()