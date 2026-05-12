import pyautogui
import pytesseract
from PIL import Image
import os
import datetime

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def take_screenshot():
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # Fixed path
        desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
        if not os.path.exists(desktop):
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        if not os.path.exists(desktop):
            desktop = r"C:\Users\abhinav yadav\Desktop"

        path = os.path.join(desktop, f"screenshot_{timestamp}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        return f"Screenshot saved to Desktop!"
    except Exception as e:
        return f"Screenshot error: {e}"


def read_screen():
    try:
        screenshot = pyautogui.screenshot()
        text = pytesseract.image_to_string(screenshot)
        if text.strip():
            return f"I can see this on your screen: {text[:200]}"
        return "I couldn't read any text on screen!"
    except Exception as e:
        return f"OCR error: {e}"