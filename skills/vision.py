import cv2
import base64
import urllib.request
import json

from config import CEREBRAS_API_KEY

def capture_and_analyze(prompt="What do you see in this image? Describe it casually like a friend."):
    try:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not cap.isOpened():
            return "Can't access camera!"

        ret, frame = cap.read()
        cap.release()

        if not ret:
            return "Couldn't capture image!"

        # Resize smaller to avoid 400 error
        frame = cv2.resize(frame, (320, 240))

        # Convert to base64
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        image_base64 = base64.b64encode(buffer).decode('utf-8')

        # Use Gemini Vision with correct key
        key = CEREBRAS_API_KEY
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
        return f"Vision error: {e}"

def what_is_this():
    return capture_and_analyze(
        "Look at this image and tell me ONLY what object or thing you see. "
        "Describe it in 1-2 casual sentences like a friend. "
        "Do NOT analyze emotions or feelings. Just identify the object!"
    )

def describe_scene():
    return capture_and_analyze(
        "Describe what you see in this scene casually in 2-3 sentences. "
        "Focus on objects, people, and environment only. "
        "Do NOT analyze emotions!"
    )

def read_text_from_camera():
    return capture_and_analyze(
        "Read any text you can see in this image. "
        "Just read the text, nothing else."
    )

def identify_person():
    return capture_and_analyze(
        "Describe the person you see. "
        "What are they wearing? How do they look? "
        "Be casual and friendly."
    )