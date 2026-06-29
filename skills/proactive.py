import random
import time

from skills.speech_gate import can_background_speak, mark_joi_spoke, mark_user_spoke

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


def proactive_loop():
    def _loop():
        while True:
            time.sleep(60)
            try:
                if should_send_passive() and can_background_speak():
                    from llm import ask_ai_stream
                    from skills.time_awareness import get_time_of_day
                    tod = get_time_of_day()
                    prompt = get_passive_prompt()
                    full_prompt = f"""
{prompt}
It is currently {tod}.
You are Joi, talking to Abhinav.
Say something short, natural and human — 1 sentence only.
No quotes, no explanation, just say it naturally.
"""
                    message = ask_ai_stream(full_prompt)
                    if message:
                        speak(message)
                        mark_joi_spoke()
            except Exception as e:
                print(f"Proactive error: {e}")

    thread = threading.Thread(target=_loop, daemon=True)
    thread.start()
    print("✅ Proactive messages started!")

    def on_person_detected(name):
        if not can_background_speak():
            return
        if name == "Abhinav":
            speak(f"Hey {name}! I see you!")
            mark_joi_spoke()
        else:
            speak("Hey, who are you?")
            mark_joi_spoke()

            while True:
                query = listen()
                if query:
                    mark_user_spoke()  # ← add this line
                    empty_count = 0
                    ...


