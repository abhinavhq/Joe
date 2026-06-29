import time

last_user_interaction = time.time()
last_speak_time = time.time()

MIN_GAP_AFTER_USER = 30  # seconds after user speaks
MIN_GAP_BETWEEN_SPEAKS = 60  # min gap between background speaks

def mark_user_spoke():
    global last_user_interaction
    last_user_interaction = time.time()

def mark_joi_spoke():
    global last_speak_time
    last_speak_time = time.time()

def can_background_speak():
    now = time.time()
    if now - last_user_interaction < MIN_GAP_AFTER_USER:
        return False
    if now - last_speak_time < MIN_GAP_BETWEEN_SPEAKS:
        return False
    return True