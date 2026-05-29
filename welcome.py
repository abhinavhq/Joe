import time
import pyttsx3

time.sleep(5)

engine = pyttsx3.init()

voices = engine.getProperty('voices')

# Mature cute female voice
for voice in voices:
    if "zira" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# Better natural pacing
engine.setProperty('rate', 165)

# Slightly softer volume
engine.setProperty('volume', 0.9)

engine.say("Master Abhinav... welcome back.")
engine.runAndWait()