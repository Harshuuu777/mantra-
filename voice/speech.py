"""
MANTRA - Voice System v6

Handles:
1. Microphone input
2. Speech-to-text
3. Text-to-speech
4. Windows SAPI5 voice
5. pyttsx3 + Windows SAPI fallback
6. Better speech recognition reliability
"""

import re
import subprocess

import speech_recognition as sr
import pyttsx3


# ============================================================
# SPEECH RECOGNIZER
# ============================================================

recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True

recognizer.pause_threshold = 0.8
recognizer.phrase_threshold = 0.25
recognizer.non_speaking_duration = 0.5


# ============================================================
# TEXT CLEANER
# ============================================================

def clean_for_speech(text):
    """
    Clean MANTRA response before sending it to TTS.
    """

    if not text:
        return ""

    text = str(text)

    # Remove emojis and unsupported Unicode
    text = re.sub(
        r"[^\x00-\x7F]+",
        " ",
        text
    )

    # Remove excessive spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


# ============================================================
# PYTTSX3 ENGINE
# ============================================================

def create_engine():

    engine = pyttsx3.init(
        driverName="sapi5"
    )

    voices = engine.getProperty(
        "voices"
    )

    selected_voice = None

    # Prefer Microsoft David
    for voice in voices:

        voice_name = str(
            voice.name
        ).lower()

        if "david" in voice_name:

            selected_voice = voice
            break

    # Fallback to first voice
    if selected_voice is None and voices:

        selected_voice = voices[0]

    if selected_voice:

        engine.setProperty(
            "voice",
            selected_voice.id
        )

        print(
            f"🔊 TTS Voice: {selected_voice.name}"
        )

    engine.setProperty(
        "rate",
        150
    )

    engine.setProperty(
        "volume",
        1.0
    )

    return engine


# ============================================================
# WINDOWS SAPI FALLBACK
# ============================================================

def windows_sapi_speak(text):
    """
    Direct Windows SAPI5 speech.

    This bypasses pyttsx3 completely.
    """

    if not text:
        return False

    # Escape PowerShell-sensitive characters
    safe_text = (
        text
        .replace("'", "''")
    )

    powershell_script = (
        "Add-Type -AssemblyName System.Speech; "
        "$speaker = New-Object "
        "System.Speech.Synthesis.SpeechSynthesizer; "
        "$speaker.Volume = 100; "
        "$speaker.Rate = 0; "
        f"$speaker.Speak('{safe_text}'); "
        "$speaker.Dispose();"
    )

    try:

        subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                powershell_script,
            ],
            check=True,
            creationflags=(
                subprocess.CREATE_NO_WINDOW
            ),
        )

        return True

    except Exception as error:

        print(
            f"❌ Windows SAPI error: {error}"
        )

        return False


# ============================================================
# TEXT TO SPEECH
# ============================================================

def speak(text):
    """
    MANTRA text-to-speech.

    First tries pyttsx3.
    If that fails, uses Windows SAPI directly.
    """

    if not text:
        return

    speech_text = clean_for_speech(
        text
    )

    if not speech_text:
        return

    print(
        f"🔊 MANTRA is speaking..."
    )

    # --------------------------------------------------------
    # METHOD 1 - PYTTSX3
    # --------------------------------------------------------

    try:

        engine = create_engine()

        engine.say(
            speech_text
        )

        engine.runAndWait()

        engine.stop()

        del engine

        return

    except Exception as error:

        print(
            f"⚠️ pyttsx3 failed: {error}"
        )

    # --------------------------------------------------------
    # METHOD 2 - WINDOWS SAPI
    # --------------------------------------------------------

    print(
        "🔄 Switching to Windows SAPI..."
    )

    success = windows_sapi_speak(
        speech_text
    )

    if success:

        print(
            "✅ Windows SAPI speech completed."
        )

    else:

        print(
            "❌ MANTRA could not produce audio."
        )


# ============================================================
# MICROPHONE CALIBRATION
# ============================================================

def calibrate_microphone():

    print(
        "🎤 Calibrating microphone..."
    )

    try:

        with sr.Microphone() as source:

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.8
            )

        print(
            "🎤 Voice system ready. "
            f"Energy threshold: "
            f"{recognizer.energy_threshold:.0f}"
        )

    except Exception as error:

        print(
            f"❌ Microphone calibration error: {error}"
        )


# ============================================================
# SPEECH RECOGNITION
# ============================================================

def recognize_audio(audio):
    """
    English India first.
    Hindi India second.
    """

    # --------------------------------------------------------
    # English
    # --------------------------------------------------------

    try:

        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        if text:

            return text.strip()

    except sr.UnknownValueError:

        pass

    except sr.RequestError as error:

        print(
            f"❌ Speech recognition service error: {error}"
        )

        return ""

    except Exception as error:

        print(
            f"❌ English recognition error: {error}"
        )


    # --------------------------------------------------------
    # Hindi
    # --------------------------------------------------------

    try:

        text = recognizer.recognize_google(
            audio,
            language="hi-IN"
        )

        if text:

            return text.strip()

    except sr.UnknownValueError:

        pass

    except sr.RequestError as error:

        print(
            f"❌ Speech recognition service error: {error}"
        )

        return ""

    except Exception as error:

        print(
            f"❌ Hindi recognition error: {error}"
        )


    return ""


# ============================================================
# LISTEN
# ============================================================

def listen():

    max_attempts = 2

    for attempt in range(
        max_attempts
    ):

        try:

            with sr.Microphone() as source:

                if attempt == 0:

                    print(
                        "\n🎤 Listening..."
                    )

                else:

                    print(
                        "\n🔄 Listening again..."
                    )

                audio = recognizer.listen(
                    source,
                    timeout=6,
                    phrase_time_limit=10
                )

        except sr.WaitTimeoutError:

            print(
                "⚠️ No speech detected."
            )

            continue

        except Exception as error:

            print(
                f"❌ Microphone error: {error}"
            )

            return ""

        print(
            "🧠 Understanding..."
        )

        text = recognize_audio(
            audio
        )

        if text:

            print(
                f"👤 You said: {text}"
            )

            return text

        if attempt == 0:

            print(
                "⚠️ I couldn't understand that."
            )

            print(
                "🎤 Please say that again..."
            )

        else:

            print(
                "⚠️ I still couldn't understand that."
            )


    return ""


# ============================================================
# VOICE SYSTEM TEST
# ============================================================

def test_speech():

    print()
    print(
        "================================"
    )
    print(
        "       MANTRA VOICE TEST"
    )
    print(
        "================================"
    )

    # --------------------------------------------------------
    # TTS
    # --------------------------------------------------------

    print()
    print(
        "🔊 Testing MANTRA voice..."
    )

    speak(
        "Hello Harshal. "
        "I am MANTRA. "
        "Your college admission assistant. "
        "My voice system is working."
    )

    # --------------------------------------------------------
    # Microphone
    # --------------------------------------------------------

    calibrate_microphone()

    text = listen()

    if text:

        speak(
            f"You said {text}"
        )

    print()
    print(
        "🎤 VOICE SYSTEM: ONLINE"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    test_speech()