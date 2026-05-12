import subprocess
import os

MATE_ENGINE_PATH = r"C:\path\to\MateEngineX.exe"

def start_mate_engine():
    try:
        subprocess.Popen(MATE_ENGINE_PATH)
        return True
    except Exception as e:
        print(f"Mate Engine error: {e}")
        return False

def trigger_emotion(emotion):
    # Mate Engine listens for hotkeys
    import pyautogui
    emotions = {
        "happy": "h",
        "sad": "s",
        "angry": "a",
        "surprised": "u",
    }
    if emotion in emotions:
        pyautogui.press(emotions[emotion])