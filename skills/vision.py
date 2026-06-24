import cv2
import base64
import urllib.request
import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma3:4b"

def capture_frame():
    try:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            return None
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return None
        frame = cv2.resize(frame, (640, 480))
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        return base64.b64encode(buffer).decode('utf-8')
    except Exception as e:
        print(f"Camera error: {e}")
        return None

def ask_ollama_vision(prompt, image_base64=None):
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
        if image_base64:
            payload["images"] = [image_base64]

        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        result = response.json()
        return result.get("response", "Couldn't analyze that!")
    except Exception as e:
        return f"Vision error: {e}"

def what_is_this():
    image = capture_frame()
    if not image:
        return "Can't access camera!"
    return ask_ollama_vision(
        "Look at this image and tell me what object or thing you see. "
        "Describe it in 1-2 casual sentences like a friend. "
        "Be direct and natural, no bullet points.",
        image
    )

def describe_scene():
    image = capture_frame()
    if not image:
        return "Can't access camera!"
    return ask_ollama_vision(
        "Describe what you see in this scene casually in 2 sentences. "
        "Focus on objects, people, and environment. Be natural.",
        image
    )

def read_text_from_camera():
    image = capture_frame()
    if not image:
        return "Can't access camera!"
    return ask_ollama_vision(
        "Read any text visible in this image. "
        "Just read what you see, nothing else.",
        image
    )

def identify_person():
    image = capture_frame()
    if not image:
        return "Can't access camera!"
    return ask_ollama_vision(
        "Describe the person you see. "
        "What are they wearing? How do they look? "
        "Be casual and friendly.",
        image
    )