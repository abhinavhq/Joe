import subprocess
import os

MATE_ENGINE_PATH = r"D:\mate engine\MateEngineX.exe"
mate_process = None

def start_mate_engine():
    global mate_process
    try:
        mate_process = subprocess.Popen(MATE_ENGINE_PATH)
        print("✅ Mate Engine started!")
        return True
    except Exception as e:
        print(f"❌ Mate Engine error: {e}")
        return False

def stop_mate_engine():
    global mate_process
    try:
        if mate_process:
            mate_process.terminate()
            print("✅ Mate Engine closed!")
    except Exception as e:
        print(f"❌ Error closing Mate Engine: {e}")

def trigger_emotion(emotion):
    import pyautogui
    emotions = {
        "happy": "h",
        "sad": "s",
        "angry": "a",
        "surprised": "u",
    }
    if emotion in emotions:
        pyautogui.press(emotions[emotion])