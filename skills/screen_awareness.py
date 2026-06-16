import pyautogui
import base64
import urllib.request
import json
import threading
import time
import random

from config import CEREBRAS_API_KEY

screen_watching = False
last_comment_time = 0
COMMENT_INTERVAL = 300  # comment every 5 minutes

SCREEN_PROMPTS = [
    "Look at this screenshot. What is the person doing? React naturally like a girlfriend seeing her boyfriend's screen. Be casual, short, 1 sentence.",
    "Look at this screenshot. Comment on what you see like a close friend peeking at someone's screen. Be funny or caring. 1 sentence only.",
    "What do you see on this screen? React like a real girl would. Short and natural.",
]

def capture_screen_base64():
    try:
        screenshot = pyautogui.screenshot()
        import io
        from PIL import Image
        buffer = io.BytesIO()
        screenshot.save(buffer, format='JPEG', quality=50)
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode('utf-8')
    except Exception as e:
        print(f"Screen capture error: {e}")
        return None

def analyze_screen():
    try:
        image_data = capture_screen_base64()
        if not image_data:
            return None

        key =  CEREBRAS_API_KEY
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"

        prompt = random.choice(SCREEN_PROMPTS)

        data = json.dumps({
            "contents": [{
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_data
                        }
                    },
                    {"text": prompt}
                ]
            }]
        }).encode()

        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json"}
        )
        response = urllib.request.urlopen(req)
        result = json.loads(response.read())
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"Screen analysis error: {e}")
        return None

def start_screen_watching(speak_func, interval=300):
    global screen_watching
    screen_watching = True
    thread = threading.Thread(
        target=_watch_loop,
        args=(speak_func, interval),
        daemon=True
    )
    thread.start()
    print("✅ Screen watching started!")

def _watch_loop(speak_func, interval):
    global screen_watching, last_comment_time
    time.sleep(30)  # wait 30 secs before first comment

    while screen_watching:
        try:
            current_time = time.time()
            if current_time - last_comment_time >= interval:
                comment = analyze_screen()
                if comment:
                    print(f"👁️ Screen comment: {comment}")
                    speak_func(comment)
                    last_comment_time = current_time
            time.sleep(30)
        except Exception as e:
            print(f"Screen watch error: {e}")
            time.sleep(60)

def stop_screen_watching():
    global screen_watching
    screen_watching = False

def peek_at_screen():
    comment = analyze_screen()
    return comment if comment else "I can't see your screen right now!"