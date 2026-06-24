from speaker import speak
from listener import listen
from brain import ask
from config import ASSISTANT_NAME, CONTACTS
from skills.web_search import web_search
from skills.open_apps import open_app
from skills.weather import get_weather
from skills.jokes import get_joke
from skills.music import play_music
from skills.reminders import set_reminder
from skills.wake_word import listen_for_wake_word
from skills.memory import save_memory, get_memory
from skills.personality import set_personality
from skills.datetime_skill import get_time, get_date
from skills.news import get_news
from skills.browser import (
    google_search, open_website, youtube_search_play,
    scroll_down, scroll_up, scroll_to_top, scroll_to_bottom,
    close_browser, go_back, go_forward, refresh_page,
    new_tab, close_tab, next_tab, zoom_in, zoom_out,
    zoom_reset, find_on_page, get_page_title, type_in_browser
)
from skills.system_info import get_system_info, get_battery, get_cpu, get_ram, get_disk
from skills.screenshot_ocr import take_screenshot, read_screen
from skills.whatsapp import send_whatsapp_now
from skills.system_controls import (
    volume_up, volume_down, mute,
    media_pause, media_next, media_prev,
    shutdown, restart, sleep,
    cancel_shutdown, lock_pc
)
from skills.knowledge import search_wikipedia, search_web_info
from skills.mate_engine import start_mate_engine, stop_mate_engine
from skills.vision import what_is_this, describe_scene, read_text_from_camera
import atexit
from skills.face_recognition import register_face, recognize_face, start_presence_detection



from skills.emotion_detection import detect_emotion_from_text

from speaker import stop_speaking, is_speaking
from speaker import speak, speak_stream

from skills.presence import (
    update_presence,
    get_presence_message)

from skills.passive import (
    should_send_passive,
    get_passive_prompt
)

from skills.sounds import download_all_sounds


from skills.filler_words import get_thinking_filler


from skills.screen_awareness import start_screen_watching, stop_screen_watching, peek_at_screen


from skills.gaming import start_gaming_companion, stop_gaming_companion, is_gaming, get_current_game

from skills.proactive import should_send_passive, get_passive_prompt
import threading
import time

from skills.system_controls import (
    volume_up, volume_down, mute, unmute, get_volume_level, set_volume,
    media_pause, media_next, media_prev, media_stop,
    get_brightness, set_brightness, brightness_up, brightness_down,
    shutdown, restart, sleep, hibernate, log_off,
    cancel_shutdown, lock_pc, unlock_pc,
    open_task_manager, empty_recycle_bin, take_screenshot_quick,
    open_control_panel, open_settings, toggle_wifi,
    open_file_explorer, minimize_all_windows
)


from skills.finance import format_crypto_report, format_stock_report, get_market_overview
from brain import get_financial_analysis

import re

def on_person_detected(name):
    if name == "Abhinav":
        speak(f"Hey {name}! I see you!")
    else:
        speak("Hey, who are you?")

atexit.register(stop_mate_engine)


def proactive_loop():  # ← ADD HERE
    def _loop():
        while True:
            time.sleep(60)
            try:
                if should_send_passive():
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
            except Exception as e:
                print(f"Proactive error: {e}")

    thread = threading.Thread(target=_loop, daemon=True)
    thread.start()
    print("✅ Proactive messages started!")

def handle(query):
    if not query:
        return
    ...

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

    # Screenshot
    elif any(w in query for w in ["take screenshot", "screenshot"]):
        speak(take_screenshot())

    elif any(w in query for w in ["read screen", "what's on screen", "read my screen"]):
        speak(read_screen())

    # Vision — make sure these are HIGH UP in handle()!
    elif any(w in query for w in
                 ["what is this", "what do you see", "look at this", "look at my hand", "what am i holding",
                  "what's in my hand"]):
        speak("Let me look!")
        speak(what_is_this())

    elif any(w in query for w in ["look around", "describe what you see", "what's around"]):
        speak("Looking around!")
        speak(describe_scene())

    elif any(w in query for w in ["read this", "what does it say", "read the text"]):
        speak("Let me read that!")
        speak(read_text_from_camera())
    # Browser
    elif "go to" in query or "browse" in query:
        site = query.replace("go to", "").replace("browse", "").strip()
        speak(open_website(site))

    elif "scroll to top" in query or "top of page" in query:
        speak(scroll_to_top())

    elif "scroll to bottom" in query or "bottom of page" in query:
        speak(scroll_to_bottom())

    elif "scroll down" in query:
        speak(scroll_down())

    elif "scroll up" in query:
        speak(scroll_up())

    elif "go back" in query or "previous page" in query:
        speak(go_back())

    elif "go forward" in query or "next page" in query:
        speak(go_forward())

    elif "refresh" in query or "reload" in query:
        speak(refresh_page())

    elif "new tab" in query:
        speak(new_tab())

    elif "close tab" in query:
        speak(close_tab())

    elif "next tab" in query or "switch tab" in query:
        speak(next_tab())

    elif "zoom in" in query:
        speak(zoom_in())

    elif "zoom out" in query:
        speak(zoom_out())

    elif "zoom reset" in query or "reset zoom" in query:
        speak(zoom_reset())

    elif "what page" in query or "current page" in query:
        speak(get_page_title())

    elif "find" in query and "page" in query:
        term = query.replace("find", "").replace("on page", "").replace("page", "").strip()
        speak(find_on_page(term))

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
            speak("I don't have that contact!")

    # Wikipedia
    elif any(w in query for w in ["wikipedia", "wiki"]) or query.startswith("who is ") or query.startswith( "what is ") and len(query) > 10:
        speak("Let me look that up!")
        result = search_wikipedia(query.replace("wikipedia", "").replace("wiki", "").replace("who is", "").replace("what is", "").replace("tell me about", "").replace("explain", "").strip())
        speak(result)

    # Web info
    elif any(w in query for w in ["search info", "find info", "look up info", "get info"]):
        speak("Searching the web!")
        result = search_web_info(query.replace("search info", "").replace("find info", "").replace("look up info", "").replace("get info", "").strip())
        speak(result)

     # Volume
    elif any(w in query for w in
                 ["volume up", "increase volume", "louder", "turn up", "increase the volume", "turn the volume up"]):
        speak(volume_up())

    elif any(w in query for w in
             ["volume down", "decrease volume", "quieter", "turn down", "decrease the volume", "turn the volume down"]):
        speak(volume_down())

    elif "unmute" in query:
        speak(unmute())

    elif "mute" in query:
        speak(mute())

    elif "what's my volume" in query or "current volume" in query or "volume level" in query:
        speak(get_volume_level())

    # Brightness
    elif "brightness up" in query or "increase brightness" in query:
        speak(brightness_up())

    elif "brightness down" in query or "decrease brightness" in query:
        speak(brightness_down())

    elif "what's my brightness" in query or "current brightness" in query:
        speak(get_brightness())

    # Media
    elif any(w in query for w in ["pause", "resume", "play pause"]):
        speak(media_pause())

    elif any(w in query for w in ["next song", "next track", "skip"]):
        speak(media_next())

    elif any(w in query for w in ["previous song", "prev track"]):
        speak(media_prev())

    elif "stop music" in query or "stop media" in query:
        speak(media_stop())

    # Power
    elif "unlock" in query:
        speak(unlock_pc())

    elif "lock" in query or "lock pc" in query:
        speak(lock_pc())

    elif "shutdown" in query or "turn off pc" in query:
        speak(shutdown())

    elif "restart" in query or "reboot" in query:
        speak(restart())

    elif "hibernate" in query:
        speak(hibernate())

    elif "sleep" in query:
        speak(sleep())

    elif "log off" in query or "log out" in query:
        speak(log_off())

    elif "cancel shutdown" in query:
        speak(cancel_shutdown())

    # Utility
    elif "task manager" in query:
        speak(open_task_manager())

    elif "empty recycle bin" in query or "clear recycle bin" in query:
        speak(empty_recycle_bin())

    elif "take a screenshot" in query or "quick screenshot" in query:
        speak(take_screenshot_quick())

    elif "control panel" in query:
        speak(open_control_panel())

    elif "open settings" in query:
        speak(open_settings())

    elif "turn on wifi" in query or "enable wifi" in query:
        speak(toggle_wifi("on"))

    elif "turn off wifi" in query or "disable wifi" in query:
        speak(toggle_wifi("off"))

    elif "file explorer" in query or "open explorer" in query:
        speak(open_file_explorer())

    elif "minimize everything" in query or "minimize all" in query or "show desktop" in query:
        speak(minimize_all_windows())
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
        speak(f"Got it! I'll remember your name is {name}!")

    # Remember preferences
    elif any(w in query for w in ["i like", "i love", "i hate", "i enjoy"]):
        save_memory("preferences", query[:50], query)
        speak(ask(query))

    # Remember user info
    elif any(w in query for w in ["i am", "i'm", "i work", "i study"]):
        save_memory("user_info", query[:50], query)
        speak(ask(query))

    # Personality modes
    elif "study mode" in query or "focus mode" in query:
        speak(set_personality("study"))
        speak("Okay I'm in study mode, let's get it!")

    elif "hype mode" in query or "motivate me" in query:
        speak(set_personality("hype"))
        speak("LET'S GOOO! I'm hyped up and ready!")

    elif "chill mode" in query or "relax mode" in query:
        speak(set_personality("chill"))
        speak("Yo we vibing now, chill mode activated")

    elif "roast mode" in query or "roast me" in query:
        speak(set_personality("roast"))
        speak("Oh you want to get roasted? Say less!")

    elif "normal mode" in query or "default mode" in query:
        speak(set_personality("normal"))
        speak("Back to normal, what's up!")

    # PC controls
    elif "shutdown" in query or "turn off pc" in query:
        speak(shutdown())

    elif "restart" in query or "reboot" in query:
        speak(restart())

    elif "sleep" in query or "hibernate" in query:
        speak(sleep())

    elif "cancel shutdown" in query:
        speak(cancel_shutdown())

    elif "lock" in query or "lock pc" in query:
        speak(lock_pc())

    # Face recognition

    elif "register my face" in query or "remember my face" in query:
        speak("Look at the camera!")
        result = register_face("Abhinav")
        speak(result)

    elif "who am i" in query or "recognize me" in query:
        speak("Let me look!")
        name = recognize_face()
        speak(f"I see {name}!")
    elif any(w in query for w in ["what am i doing", "look at my screen", "what's on my screen"]):
        speak("Let me peek!")
        speak(peek_at_screen())

    elif "start watching" in query or "watch my screen" in query:
        start_screen_watching(speak)
        speak("Okay I'll keep an eye on your screen!")

    elif "stop watching" in query:
        stop_screen_watching()
        speak("Okay I'll stop peeking!")

        # Gaming
    elif any(w in query for w in ["am i gaming", "what game", "gaming mode"]):
        game = get_current_game()
        if game:
            speak(f"You're playing {game}! How's it going? 🎮")
        else:
            speak("You're not gaming right now!")

        # Screen awareness
    elif any(w in query for w in ["what am i doing", "look at my screen", "what's on my screen"]):
        speak("Let me peek!")
        speak(peek_at_screen())

    elif "start watching" in query or "watch my screen" in query:
        start_screen_watching(speak)
        speak("Okay I'll keep an eye on your screen!")

    elif "stop watching" in query:
        stop_screen_watching()
        speak("Okay I'll stop peeking!")

        # Crypto & Stocks
    elif "market overview" in query or "crypto market" in query:
        speak("Let me check the market!")
        speak(get_market_overview())

    elif any(w in query for w in ["price", "stock", "crypto", "bitcoin", "worth"]) and not any(
            w in query for w in ["go to", "browse"]):
        speak("Let me check that for you!")

        from skills.finance import COIN_IDS, STOCK_SYMBOLS

        found_asset = None
        asset_type = None

        for name in COIN_IDS:
            if name in query:
                found_asset = name
                asset_type = "crypto"
                break

        if not found_asset:
            for name in STOCK_SYMBOLS:
                if name in query:
                    found_asset = name
                    asset_type = "stock"
                    break

        if found_asset:
            if asset_type == "crypto":
                report = format_crypto_report(found_asset)
            else:
                report = format_stock_report(found_asset)

            speak(report)

            analysis = get_financial_analysis(asset_type, found_asset, report)
            if analysis:
                speak(analysis)
        else:
            speak("Which coin or stock do you want to check? Try saying the name clearly!")

        # AI chat
    else:
        import threading
        stop_event = threading.Event()

        def say_filler():
            import time
            time.sleep(0.8)
            if not stop_event.is_set():
                speak(get_thinking_filler())

        filler_thread = threading.Thread(target=say_filler, daemon=True)
        filler_thread.start()

        response = ask(query)
        stop_event.set()
        speak_stream(response)

if __name__ == "__main__":

    download_all_sounds()

    start_mate_engine()

    start_presence_detection(callback=on_person_detected)

    start_screen_watching(speak)

    start_gaming_companion(speak)

    proactive_loop()

    name = get_memory("user", "name")

    if name:

        speak(f"Hey {name}! I'm back, say Hey Joi to wake me up!")

    else:

        speak("Hey! I'm Joi, say Hey Joi to wake me up!")

    while True:

        # =========================
        # HUMAN-LIKE PASSIVE THOUGHTS
        # =========================

        if should_send_passive():

            passive_prompt = get_passive_prompt()

            response = ask(passive_prompt)

            speak_stream(response)

        # =========================
        # WAKE WORD
        # =========================

        listen_for_wake_word()

        # =========================
        # PRESENCE AWARENESS
        # =========================

        presence_msg = get_presence_message()

        update_presence()

        if presence_msg:

            speak(presence_msg)

        else:

            speak("Yeah? What's up!")

        empty_count = 0

        while True:

            # =========================
            # INTERRUPT IF USER TALKS
            # =========================

            if is_speaking:

                stop_speaking()

            query = listen()

            if query:

                empty_count = 0

                if any(w in query for w in ["bye", "exit", "quit", "stop"]):

                    speak("Goodbye! Have a great day!")

                    stop_mate_engine()

                    exit()

                handle(query)

            else:

                empty_count += 1

                if empty_count >= 5:

                    speak("I'll be here if you need me!")

                    print("👂 Going back to sleep...")

                    break