from cartesia import Cartesia
import asyncio
import pygame as pg
import os
import tempfile
import re
import time

client = Cartesia(api_key="sk_car_MmRpUuXpfqmrUNw4y4BXyq"
)

VOICE_ID = "694f9389-aac1-45b6-b726-9d9369183238"

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

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        tmp_path = f.name

    try:
        audio = client.tts.bytes(
            model_id="sonic-2",
            transcript=text,
            voice={
                "mode": "id",
                "id": VOICE_ID
            },
            language="en",
            output_format={
                "container": "wav",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            },
        )

        with open(tmp_path, "wb") as audio_file:
            for chunk in audio:
                audio_file.write(chunk)

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
    print(f"JOI: {text}")

    try:
        asyncio.run(_speak_async(text))

    except Exception as e:
        print(f"Voice error: {e}")


def speak_stream(text):
    parts = re.split(r'(?<=[.!?]) +', text)

    for part in parts:
        if not part.strip():
            continue

        speak(part)

        time.sleep(0.2)