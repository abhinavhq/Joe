import random
import threading
import time

THINKING_FILLERS = [
    "umm...",
    "hmm let me think...",
    "okay so...",
    "wait...",
    "like...",
    "ugh okay so...",
    "ngl...",
    "okay okay...",
    "so basically...",
    "honestly...",
]

RESPONSE_STARTERS = [
    "okay so ",
    "ngl ",
    "like ",
    "honestly ",
    "fr tho ",
    "lowkey ",
    "wait so ",
    "omg okay ",
    "ugh okay ",
    "so basically ",
]

THINKING_SOUNDS = [
    "hmm",
    "umm",
    "uh",
    "let me think",
    "wait",
]

filler_active = False


def add_filler_starter(text):
    # 40% chance to add a casual starter
    if random.random() < 0.4:
        starter = random.choice(RESPONSE_STARTERS)
        return starter + text
    return text


def get_thinking_filler():
    return random.choice(THINKING_FILLERS)


def get_thinking_sound():
    return random.choice(THINKING_SOUNDS)


def speak_filler_while_thinking(speak_func, stop_event):
    # Wait a bit before saying filler
    time.sleep(0.8)
    if not stop_event.is_set():
        filler = get_thinking_filler()
        print(f"💭 Filler: {filler}")
        speak_func(filler)


def wrap_with_filler(speak_func, ai_func, query):
    stop_event = threading.Event()

    # Start filler in background
    filler_thread = threading.Thread(
        target=speak_filler_while_thinking,
        args=(speak_func, stop_event),
        daemon=True
    )
    filler_thread.start()

    # Get AI response
    reply = ai_func(query)

    # Stop filler
    stop_event.set()
    filler_thread.join(timeout=1)

    # Add casual starter to reply
    reply = add_filler_starter(reply)

    return reply


def clean_response_for_speech(text):
    # Remove markdown
    import re
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'#{1,6}\s', '', text)
    text = re.sub(r'`(.*?)`', r'\1', text)

    # Remove emojis for cleaner speech
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F9FF"
                               u"\U00002600-\U000027BF"
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub('', text)

    return text.strip()