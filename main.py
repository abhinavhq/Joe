from speaker import speak
from listener import listen
from brain import ask
from config import ASSISTANT_NAME
from skills.web_search import web_search
from skills.open_apps import open_app
from skills.weather import get_weather
from skills.jokes import get_joke
from skills.music import play_music
from skills.reminders import set_reminder
from skills.wake_word import listen_for_wake_word
from skills.memory import save_memory, get_memory
from skills.datetime_skill import get_time, get_date
from skills.news import get_news
from skills.browser import (open_website, scroll_down, scroll_up, close_browser)
from skills.system_info import get_system_info, get_battery, get_cpu, get_ram, get_disk
from skills.screenshot_ocr import take_screenshot, read_screen
from skills.whatsapp import send_whatsapp_now
from config import CONTACTS
from skills.system_controls import (
    volume_up, volume_down, mute,
    media_pause, media_next, media_prev
)
from skills.knowledge import search_wikipedia, search_web_info
from skills.mate_engine import start_mate_engine

import re

def handle(query):
    if not query:
        return

    # Web search
    if any(w in query for w in ["search", "google", "look up"]):
        speak(web_search(query))

    # Open apps
    elif any(w in query for w in ["open", "launch", "start"]):
        speak(open_app(query))

    # Weather
    elif any(w in query for w in ["weather", "temperature", "forecast"]):
        speak(get_weather())

    # Jokes
    elif any(w in query for w in ["joke", "funny", "laugh"]):
        speak(get_joke())

     # Time
    elif any(w in query for w in ["what time", "current time", "time now"]):
        speak(get_time())

    # Date
    elif any(w in query for w in ["what date", "today's date", "what day"]):
        speak(get_date())

    # News
    elif any(w in query for w in ["news", "headlines", "what's happening"]):
        speak(get_news())

    # System info
    elif any(w in query for w in ["system info", "pc status", "computer status"]):
        speak(get_system_info())

    elif any(w in query for w in ["battery", "charge"]):
        speak(get_battery())

    elif any(w in query for w in ["cpu", "processor"]):
        speak(get_cpu())

    elif any(w in query for w in ["ram", "memory"]):
        speak(get_ram())

    elif any(w in query for w in ["disk", "storage", "space"]):
        speak(get_disk())


      # Screensho
    elif any(w in query for w in ["take screenshot", "screenshot"]):
        speak(take_screenshot())

    elif any(w in query for w in ["read screen", "what's on screen", "read my screen"]):
        speak(read_screen())

     # Browser automation
    elif "browse" in query or "go to" in query:
        site = query.replace("browse", "").replace("go to", "").strip()
        speak(open_website(site))

    elif "scroll down" in query:
        speak(scroll_down())

    elif "scroll up" in query:
        speak(scroll_up())

    elif "close browser" in query:
        speak(close_browser())

     # WhatsApp
    elif "whatsapp" in query or "send message" in query or "text" in query:
        speak("Who do you want to message?")
        contact_name = listen()
        if contact_name and contact_name in CONTACTS:
            speak("What's the message?")
            message = listen()
            if message:
                speak(send_whatsapp_now(CONTACTS[contact_name], message))
        else:
            speak(f"I don't have {contact_name} in your contacts!")

    # Wikipedia
    elif any(w in query for w in ["wikipedia", "wiki", "who is", "what is", "tell me about", "explain"]):
        speak("Let me look that up!")
        result = search_wikipedia(
            query.replace("wikipedia", "").replace("wiki", "").replace("who is", "").replace("what is", "").replace(
                "tell me about", "").replace("explain", "").strip())
        speak(result)

    # Web info
    elif any(w in query for w in ["search info", "find info", "look up info", "get info"]):
        speak("Searching the web!")
        result = search_web_info(
            query.replace("search info", "").replace("find info", "").replace("look up info", "").replace("get info",
                                                                                                          "").strip())
        speak(result)



    # Volume controls
    elif any(w in query for w in ["volume up", "increase volume", "louder", "turn up"]):
        speak(volume_up())

    elif any(w in query for w in ["volume down", "decrease volume", "quieter", "turn down"]):
        speak(volume_down())

    elif any(w in query for w in ["mute", "silence"]):
        speak(mute())

    # Media controls
    elif any(w in query for w in ["pause", "resume", "play pause"]):
        speak(media_pause())

    elif any(w in query for w in ["next song", "next track", "skip"]):
        speak(media_next())

    elif any(w in query for w in ["previous song", "prev track", "go back"]):
        speak(media_prev())

    # Music
    elif any(w in query for w in ["play", "music", "song"]):
        speak(play_music(query))

    # Reminders
    elif "remind" in query:
        match = re.search(r"remind me to (.+) in (\d+)", query)
        if match:
            task, mins = match.group(1), int(match.group(2))
            speak(set_reminder(task, mins))
        else:
            speak("Please say: remind me to [task] in [X] minutes")

    # Remember name
    elif "my name is" in query:
        name = query.replace("my name is", "").strip()
        save_memory("user", "name", name)
        speak(f"Got it! I'll remember that your name is {name}!")

    # Remember preferences
    elif any(w in query for w in ["i like", "i love", "i hate", "i enjoy"]):
        save_memory("preferences", query[:50], query)
        speak(ask(query))

    # Remember user info
    elif any(w in query for w in ["i am", "i'm", "i work", "i study"]):
        save_memory("user_info", query[:50], query)
        speak(ask(query))

    # Exit
    elif any(w in query for w in ["bye", "exit", "quit", "stop"]):
        speak("Goodbye! Have a great day!")
        exit()

    # AI chat
    else:
        speak(ask(query))


# if __name__ == "__main__":
#     start_avatar()

if __name__ == "__main__":
    start_mate_engine()  # Start Mate Engine with JOI!

    name = get_memory("user", "name")
    if name:
        speak(f"Hey {name}! I'm back, say Hey Joi to wake me up!")
    else:
        speak("Hey! I'm Joi, say Hey Joi to wake me up!")

    while True:
        listen_for_wake_word()
        speak("Yeah? What's up!")

        # Keep listening until silence or bye
        while True:
            query = listen()
            if query:
                if any(w in query for w in ["bye", "exit", "quit", "stop"]):
                    speak("Goodbye! Have a great day!")
                    exit()
                handle(query)
            else:
                # Only go back to sleep after 3 empty listens
                empty_count = 0
                empty_count += 1
                if empty_count >= 3:
                    print("👂 Going back to sleep...")
                    break