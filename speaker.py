import os
import tempfile
import threading
import re
import time
import speech_recognition as sr
import pygame as pg

try:
    import cartesia
    CARTESIA_AVAILABLE = True
except:
    CARTESIA_AVAILABLE = False
    print("⚠️ Cartesia not available, using Edge TTS")

VOICE_PROFILES = {
    "normal":   {"speed": "normal", "emotion": []},
    "happy":    {"speed": "fast",   "emotion": [{"name": "positivity", "level": "high"}]},
    "excited":  {"speed": "fastest","emotion": [{"name": "positivity", "level": "highest"}]},
    "sad":      {"speed": "slow",   "emotion": [{"name": "sadness", "level": "medium"}]},
    "soft":     {"speed": "slow",   "emotion": [{"name": "sadness", "level": "low"}]},
    "angry":    {"speed": "fast",   "emotion": [{"name": "anger", "level": "medium"}]},
    "flirty":   {"speed": "normal", "emotion": [{"name": "positivity", "level": "medium"}]},
    "tired":    {"speed": "slowest","emotion": [{"name": "sadness", "level": "low"}]},
    "playful":  {"speed": "fast",   "emotion": [{"name": "positivity", "level": "high"}]},
    "anxious":  {"speed": "fast",   "emotion": [{"name": "anger", "level": "low"}]},
    "caring":   {"speed": "slow",   "emotion": [{"name": "positivity", "level": "medium"}]},
    "clingy":   {"speed": "normal", "emotion": [{"name": "positivity", "level": "medium"}]},
}

current_emotion = "normal"
_mixer_init = False
is_speaking = False
interrupt_flag = False

CARTESIA_VOICE_ID = "eef47c0d-cb49-4160-a4a0-6b97ed4c81e6"

def set_voice_emotion(emotion):
    global current_emotion
    if emotion in VOICE_PROFILES:
        current_emotion = emotion
        print(f"🎙️ Voice emotion: {emotion}")

def get_voice_profile():
    return VOICE_PROFILES.get(current_emotion, VOICE_PROFILES["normal"])

def stop_speaking():
    global is_speaking, interrupt_flag
    is_speaking = False
    interrupt_flag = True
    try:
        pg.mixer.music.stop()
    except:
        pass

def _listen_for_interrupt():
    global interrupt_flag
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            while is_speaking:
                try:
                    audio = recognizer.listen(source, timeout=0.5, phrase_time_limit=2)
                    text = recognizer.recognize_google(audio).lower()
                    if text and len(text) > 2:
                        print(f"🛑 Interrupted: {text}")
                        stop_speaking()
                        break
                except:
                    pass
    except:
        pass

def _speak_cartesia(text):
    global _mixer_init, is_speaking, interrupt_flag
    try:
        from config import CARTESIA_API_KEY
        client = cartesia.Cartesia(api_key=CARTESIA_API_KEY)
        profile = get_voice_profile()

        audio_chunks = client.tts.bytes(
            model_id="sonic-2",
            transcript=text,
            voice={
                "id": CARTESIA_VOICE_ID,
                "experimental_controls": {
                    "speed": profile["speed"],
                    "emotion": profile["emotion"]
                }
            },
            output_format={
                "container": "mp3",
                "encoding": "mp3",
                "sample_rate": 44100,
            }
        )

        audio_data = b"".join(audio_chunks)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tmp_path = f.name
            f.write(audio_data)

        if not _mixer_init:
            pg.mixer.init()
            _mixer_init = True

        interrupt_flag = False
        pg.mixer.music.load(tmp_path)
        is_speaking = True
        pg.mixer.music.play()

        interrupt_thread = threading.Thread(
            target=_listen_for_interrupt,
            daemon=True
        )
        interrupt_thread.start()

        while pg.mixer.music.get_busy():
            if interrupt_flag:
                pg.mixer.music.stop()
                break
            pg.time.wait(100)

        pg.mixer.music.unload()
        try:
            os.remove(tmp_path)
        except:
            pass

    except Exception as e:
        print(f"Cartesia error: {e}")
        _speak_edge_tts(text)
    finally:
        is_speaking = False

def _speak_edge_tts(text):
    global _mixer_init, is_speaking, interrupt_flag
    import asyncio
    import edge_tts

    VOICE = "en-US-AriaNeural"

    async def _async():
        global _mixer_init, is_speaking, interrupt_flag
        interrupt_flag = False
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tmp_path = f.name
        try:
            communicate = edge_tts.Communicate(text, VOICE)
            await communicate.save(tmp_path)
            if not _mixer_init:
                pg.mixer.init()
                _mixer_init = True
            pg.mixer.music.load(tmp_path)
            is_speaking = True
            pg.mixer.music.play()
            interrupt_thread = threading.Thread(
                target=_listen_for_interrupt, daemon=True)
            interrupt_thread.start()
            while pg.mixer.music.get_busy():
                if interrupt_flag:
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

    asyncio.run(_async())

def speak(text):
    global is_speaking
    print(f"JOI: {text}")
    try:
        if CARTESIA_AVAILABLE:
            _speak_cartesia(text)
        else:
            _speak_edge_tts(text)
    except Exception as e:
        print(f"Speak error: {e}")
        try:
            _speak_edge_tts(text)
        except:
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
        time.sleep(0.1)