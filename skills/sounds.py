import pygame
import os
import threading
import random

SOUNDS_DIR = os.path.join(os.path.dirname(__file__), '..', 'sounds')
os.makedirs(SOUNDS_DIR, exist_ok=True)

_mixer_init = False

def init_sounds():
    global _mixer_init
    try:
        if not _mixer_init:
            pygame.mixer.init()
            _mixer_init = True
    except:
        pass

def laugh():
    from speaker import speak
    options = [
        "hahaha oh my god!",
        "lmaoo okay that's actually funny",
        "hahaha stop it!",
        "omg hahaha!",
        "okay that got me haha!",
        "hehehe 💀",
    ]
    threading.Thread(
        target=speak,
        args=(random.choice(options),),
        daemon=True
    ).start()

def giggle():
    from speaker import speak
    options = [
        "hehe",
        "hehehe",
        "teehee",
        "hehe stop!",
    ]
    threading.Thread(
        target=speak,
        args=(random.choice(options),),
        daemon=True
    ).start()

def hmm_sound():
    from speaker import speak
    options = [
        "hmm",
        "hmm let me think",
        "umm",
    ]
    threading.Thread(
        target=speak,
        args=(random.choice(options),),
        daemon=True
    ).start()

def download_all_sounds():
    print("✅ Sound system ready!")