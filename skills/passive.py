import random
import time

last_passive = time.time()

human_thoughts = [

    "say something soft and natural",

    "say something playful like a real close friend",

    "randomly check on him naturally",

    "say something cute and casual",

    "react like you've been thinking about him",

    "say something late-night vibe if it's night",

    "tease him naturally",

    "say something emotionally warm",

    "act slightly clingy in a cute way",

    "say something human and spontaneous"
]

def should_send_passive():

    global last_passive

    now = time.time()

    # every 10 minutes
    if now - last_passive > 600:

        last_passive = now

        return True

    return False

def get_passive_prompt():

    return random.choice(human_thoughts)