import edge_tts
import asyncio
import pygame as pg
import os
import tempfile
import threading
import re
import time

VOICE = "en-US-AriaNeural"

# Voice profiles based on emotion
VOICE_PROFILES = {
    "normal":  {"rate": "+0%",  "pitch": "+0Hz",  "volume": "+0%"},
    "happy":   {"rate": "+15%", "pitch": "+5Hz",  "volume": "+10%"},
    "excited": {"rate": "+25%", "pitch": "+8Hz",  "volume": "+15%"},
    "sad":     {"rate": "-20%", "pitch": "-5Hz",  "volume": "-10%"},
    "soft":    {"rate": "-10%", "pitch": "-2Hz",  "volume": "-15%"},
    "angry":   {"rate": "+10%", "pitch": "+3Hz",  "volume": "+20%"},
    "flirty":  {"rate": "-5%",  "pitch": "+3Hz",  "volume": "-5%"},
    "tired":   {"rate": "-25%", "pitch": "-8Hz",  "volume": "-20%"},
    "playful": {"rate": "+20%", "pitch": "+6Hz",  "volume": "+10%"},
    "anxious": {"rate": "+15%", "pitch": "+2Hz",  "volume": "+5%"},
    "caring":  {"rate": "-10%", "pitch": "+1Hz",  "volume": "-5%"},
    "clingy":  {"rate": "-5%",  "pitch": "+4Hz",  "volume": "-5%"},
}

current_emotion = "normal"
_mixer_init = False
is_speaking = False

def set_voice_emotion(emotion):
    global current_emotion
    if emotion in VOICE_PROFILES:
        current_emotion = emotion
        print(f"🎙️ Voice emotion: {emotion}")

def get_voice_profile():
    return VOICE_PROFILES.get(current_emotion, VOICE_PROFILES["normal"])

def stop_speaking():
    global is_speaking
    is_speaking = False
    try:
        pg.mixer.music.stop()
    except:
        pass

async def _speak_async(text):
    global _mixer_init, is_speaking

    profile = get_voice_profile()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tmp_path = f.name

    try:
        communicate = edge_tts.Communicate(
            text,
            VOICE,
            rate=profile["rate"],
            pitch=profile["pitch"],
            volume=profile["volume"]
        )
        await communicate.save(tmp_path)

        if not _mixer_init:
            pg.mixer.init()
            _mixer_init = True

        pg.mixer.music.load(tmp_path)
        is_speaking = True
        pg.mixer.music.play()

        while pg.mixer.music.get_busy():
            if not is_speaking:
                pg.mixer.music.stop()
                break
            pg.time.wait(100)

        pg.mixer.music.unload()

    finally:
        is_speaking = False
        try:
            os.remove(tmp_path)
        except:
            pass

def speak(text):
    global is_speaking
    print(f"JOI: {text}")
    try:
        asyncio.run(_speak_async(text))
    except Exception as e:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.setProperty('rate', 175)
        engine.say(text)
        engine.runAndWait()

def speak_stream(text):
    parts = re.split(r'(?<=[.!?]) +', text)
    for part in parts:
        if not part.strip():
            continue
        speak(part)
        time.sleep(0.2)