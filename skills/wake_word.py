import speech_recognition as sr


def listen_for_wake_word():
    recognizer = sr.Recognizer()
    print("👂 Waiting for wake word...")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                text = recognizer.recognize_google(audio).lower()
                print(f"Heard: {text}")

                wake_words = [
                    "hey joi",
                    "hey joy",
                    "hey joe",
                    "joi",
                    "joy",
                    "hey baby",
                    "baby",
                    "hey bb",
                ]
                if any(phrase in text for phrase in wake_words):
                    print("✅ Wake word detected!")
                    return True

        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except Exception as e:
            print(f"Wake word error: {e}")