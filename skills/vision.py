import cv2
import base64
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma3:4b"

VISION_SYSTEM = """You are a precise visual analyst with expert knowledge in:
- Anime/manga characters (by hair color, clothing, weapons, art style)
- Products and brands (by logos, text, packaging)
- People (by appearance, clothing, expressions)
- Documents and text (read exactly as written)
- Food and objects (by color, texture, shape)

Rules:
1. ALWAYS describe physical details first (colors, shapes, textures)
2. THEN identify based on those details
3. Never guess blindly — base identification on what you actually see
4. Be specific and accurate, not vague
5. Keep responses casual and short (2 sentences max)
6. If unsure, say what you DO see clearly instead of wrong guessing"""

def capture_frame(width=640, height=480, quality=85):
    try:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            return None
        # Warm up camera
        for _ in range(3):
            cap.read()
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return None
        frame = cv2.resize(frame, (width, height))
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
        return base64.b64encode(buffer).decode('utf-8')
    except Exception as e:
        print(f"Camera error: {e}")
        return None

def ask_ollama_vision(prompt, image_base64=None, timeout=120):
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": f"{VISION_SYSTEM}\n\nTask: {prompt}",
            "stream": False,
            "options": {
                "temperature": 0.1,  # low temp = more accurate, less creative
                "top_p": 0.9,
            }
        }
        if image_base64:
            payload["images"] = [image_base64]

        print("👁️ Analyzing...")
        response = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
        result = response.json()
        text = result.get("response", "Couldn't analyze that!")

        # Clean garbage/hallucinated output
        if len(text) > 600:
            text = text[:600] + "..."
        if len(set(text[:30])) < 4:
            return "I can see something but can't make it out clearly!"

        return text.strip()
    except requests.exceptions.Timeout:
        return "Taking too long to analyze — try again!"
    except Exception as e:
        return f"Vision error: {e}"

def what_is_this():
    image = capture_frame()
    if not image:
        return "Can't access camera!"
    return ask_ollama_vision(
        "Carefully examine this image. "
        "First describe: main colors, shape, size, any text/logos visible, distinctive features. "
        "Then identify: what exactly is this object/character/item? "
        "For anime figures: hair color → clothing color → weapons → then name the character. "
        "For products: read any visible brand/text first. "
        "Be accurate. 2 sentences max.",
        image
    )

def describe_scene():
    image = capture_frame()
    if not image:
        return "Can't access camera!"
    return ask_ollama_vision(
        "Describe this entire scene: "
        "What's in the foreground? Background? "
        "Any people, objects, furniture, nature? "
        "What's the setting/environment? "
        "Colors and lighting? Be specific and natural. 2-3 sentences.",
        image
    )

def read_text_from_camera():
    image = capture_frame(quality=95)  # higher quality for text
    if not image:
        return "Can't access camera!"
    return ask_ollama_vision(
        "Read ALL text visible in this image exactly as written. "
        "Include every word you can see — signs, labels, screens, "
        "handwriting, printed text, anything. "
        "Output ONLY the text you read, word for word.",
        image
    )

def identify_person():
    image = capture_frame()
    if not image:
        return "Can't access camera!"
    return ask_ollama_vision(
        "Describe this person accurately: "
        "1) Hair: color and style "
        "2) Face: any notable features, expression "
        "3) Clothing: colors, style, what they're wearing "
        "4) What are they doing? "
        "Be specific and casual. 2 sentences.",
        image
    )

def identify_food():
    image = capture_frame()
    if not image:
        return "Can't access camera!"
    return ask_ollama_vision(
        "What food or drink is in this image? "
        "Describe: color, texture, presentation, ingredients you can see. "
        "Then identify the dish/food item. "
        "If packaged food, read the label. "
        "2 sentences max.",
        image
    )

def read_document():
    image = capture_frame(quality=95)
    if not image:
        return "Can't access camera!"
    return ask_ollama_vision(
        "This is a document or paper. "
        "Read the title/heading first, then key content. "
        "Summarize the main points in 2-3 sentences. "
        "Include any important numbers, dates, or names you see.",
        image
    )

def read_screen_content():
    image = capture_frame(quality=95)
    if not image:
        return "Can't access camera!"
    return ask_ollama_vision(
        "What's on this screen/display? "
        "What app, website, or program is open? "
        "What content is showing? Read any visible text. "
        "Be specific about what you see. 2 sentences.",
        image
    )

def identify_anime_character():
    image = capture_frame()
    if not image:
        return "Can't access camera!"
    return ask_ollama_vision(
        "This appears to be an anime/manga character or figure. "
        "Carefully examine: "
        "Hair color and style, eye color, "
        "clothing colors and distinctive features, "
        "any weapons or accessories, "
        "art style clues. "
        "Based on these physical details, identify the character and which anime/manga they're from. "
        "Be confident only if details clearly match. 2 sentences.",
        image
    )

def check_surroundings():
    image = capture_frame(width=1280, height=720)  # higher res for surroundings
    if not image:
        return "Can't access camera!"
    return ask_ollama_vision(
        "Give a detailed description of this entire environment: "
        "room type, furniture, objects present, lighting, "
        "colors, any screens or displays visible, "
        "overall atmosphere. "
        "What kind of space is this? 3 sentences.",
        image
    )