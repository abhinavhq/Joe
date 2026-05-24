import cv2
import base64
import urllib.request
import json
from config import CEREBRAS_API_KEY


def capture_and_analyze(prompt="What do you see in this image? Describe it casually like a friend."):
    # Open camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return "Can't access camera!"

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return "Couldn't capture image!"

    # Show what was captured briefly
    cv2.imshow("JOI's Vision", frame)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()

    # Convert to base64
    _, buffer = cv2.imencode('.jpg', frame)
    image_base64 = base64.b64encode(buffer).decode('utf-8')

    # Send to Gemini Vision
    key = GEMINI_API_KEYS[0]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"

    data = json.dumps({
        "contents": [{
            "parts": [
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": image_base64
                    }
                },
                {
                    "text": prompt
                }
            ]
        }]
    }).encode()

    try:
        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json"}
        )
        response = urllib.request.urlopen(req)
        result = json.loads(response.read())
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Vision error: {e}"


def what_is_this():
    return capture_and_analyze(
        "Look at this image and tell me ONLY what object or thing you see. "
        "Describe it in 1-2 casual sentences like a friend. "
        "Do NOT analyze emotions or feelings. Just identify the object!"
    )


def read_text_from_camera():
    return capture_and_analyze("Read any text you can see in this image.")

def describe_scene():
    return capture_and_analyze(
        "Describe what you see in this scene casually in 2-3 sentences. "
        "Focus on objects, people, and environment only. "
        "Do NOT analyze emotions!"
    )
def identify_person():
    return capture_and_analyze("Describe the person you see. What are they wearing? How do they look?")