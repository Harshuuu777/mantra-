"""
MANTRA - Voice System v3

Handles:
1. Microphone input
2. Speech-to-text
3. Text-to-speech
"""

import re
import speech_recognition as sr
import pyttsx3


# ============================================================
# SPEECH RECOGNIZER
# ============================================================

recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.7
recognizer.phrase_threshold = 0.2
recognizer.non_speaking_duration = 0.4


# ============================================================
# TEXT CLEANER
# ============================================================

def clean_for_speech(text):
    """
    Remove emojis and unsupported characters before
    sending text to Windows TTS.
    """

    if not text:
        return ""

    text = str(text)

    # Keep normal ASCII characters
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ============================================================
# CREATE TTS ENGINE
# ============================================================

def create_engine():
    """
    Create a fresh pyttsx3 engine.

    Creating a fresh engine for every response makes
    Windows TTS more reliable during long conversations.
    """

    engine = pyttsx3.init()

    engine.setProperty("rate", 165)
    engine.setProperty("volume", 1.0)

    return engine


# ============================================================
# TEXT TO SPEECH
# ============================================================

def speak(text):
    """
    Convert MANTRA response into speech.
    """

    if not text:
        return

    speech_text = clean_for_speech(text)

    if not speech_text:
        return

    try:

        print("🔊 MANTRA is speaking...")

        engine = create_engine()

        engine.say(speech_text)
        engine.runAndWait()

        engine.stop()

        del engine

    except Exception as error:

        print(f"❌ Text-to-speech error: {error}")

        # Retry once
        try:

            print("🔄 Retrying voice...")

            engine = create_engine()

            engine.say(speech_text)
            engine.runAndWait()

            engine.stop()

            del engine

        except Exception as retry_error:

            print(f"❌ TTS retry failed: {retry_error}")


# ============================================================
# MICROPHONE CALIBRATION
# ============================================================

def calibrate_microphone():
    """
    Calibrate microphone for background noise.
    """

    print("🎤 Calibrating microphone...")

    try:

        with sr.Microphone() as source:

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.8
            )

        print("🎤 Voice system ready.")

    except Exception as error:

        print(f"❌ Microphone error: {error}")


# ============================================================
# SPEECH TO TEXT
# ============================================================

def listen():
    """
    Listen to the microphone and convert speech to text.
    """

    try:

        with sr.Microphone() as source:

            print("\n🎤 Listening...")

            try:

                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10
                )

            except sr.WaitTimeoutError:

                print("⚠️ No speech detected.")

                return ""

    except Exception as error:

        print(f"❌ Microphone error: {error}")

        return ""

    print("🧠 Understanding...")

    try:

        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        text = text.strip()

        if text:

            print(f"👤 You said: {text}")

        return text

    except sr.UnknownValueError:

        print("⚠️ I couldn't understand that.")

        return ""

    except sr.RequestError as error:

        print(f"❌ Speech recognition service error: {error}")

        return ""

    except Exception as error:

        print(f"❌ Recognition error: {error}")

        return ""


# ============================================================
# VOICE SYSTEM TEST
# ============================================================

def test_speech():

    print("\n================================")
    print("       MANTRA VOICE TEST")
    print("================================")

    calibrate_microphone()

    speak(
        "Hello! I am MANTRA, "
        "your college admission assistant."
    )

    text = listen()

    if text:

        speak(
            f"You said {text}"
        )

    print("\n🎤 VOICE SYSTEM: ONLINE")


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    test_speech()