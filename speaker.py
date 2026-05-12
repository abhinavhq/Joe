import edge_tts
import asyncio
import pygame as pg
import os
import tempfile

VOICE = "en-US-AriaNeural"

_mixer_init = False

async def _speak_async(text):
    global _mixer_init
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tmp_path = f.name
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(tmp_path)
        if not _mixer_init:
            pg.mixer.init()
            _mixer_init = True
        pg.mixer.music.load(tmp_path)
        pg.mixer.music.play()
        while pg.mixer.music.get_busy():
            pg.time.wait(100)
        pg.mixer.music.unload()
    finally:
        try:
            os.remove(tmp_path)
        except:
            pass

def speak(text):
    print(f"VIVI: {text}")
    try:
        # Animate mouth
        try:
            from skills.avatar import set_speaking
            set_speaking(True)
        except:
            pass
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
    finally:
        try:
            from skills.avatar import set_speaking
            set_speaking(False)
        except:
            pass