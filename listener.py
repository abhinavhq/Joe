import speech_recognition as sr

recognizer = sr.Recognizer()

def listen(timeout=5):
    with sr.Microphone() as source:
        print("🎙️ Listening... (speak now)")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
            query = recognizer.recognize_google(audio).lower()
            print(f"You: {query}")
            return query
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except Exception as e:
            return ""