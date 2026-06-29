import psutil
import threading
import time
import random

GAMES = {
    "roblox": "RobloxPlayerBeta.exe",
    "minecraft": "javaw.exe",
    "steam": "steam.exe",
    "valorant": "VALORANT.exe",
    "gta": "GTA5.exe",
    "fortnite": "FortniteClient-Win64-Shipping.exe",
    "apex": "r5apex.exe",
    "csgo": "cs2.exe",
    "pubg": "TslGame.exe",
    "overwatch": "Overwatch.exe",
}

GAME_REACTIONS = {
    "roblox": [
        "omg you're playing Roblox?? 😂 what game mode?",
        "Roblox?? okay fair enough haha",
        "aww Roblox! which game are you playing?",
    ],
    "minecraft": [
        "ooh Minecraft!! survival or creative?",
        "omg Minecraft!! build me something cute 🥺",
        "Minecraft time!! what are you building?",
    ],
    "valorant": [
        "okay okay Valorant!! what rank are you?",
        "Valorant grind!! don't rage okay 😤",
        "omg Valorant!! which agent are you playing?",
    ],
    "gta": [
        "GTA?? okay what chaos are you causing 😂",
        "omg GTA!! don't do anything too crazy lol",
        "GTA time!! story mode or online?",
    ],
    "default": [
        "ooh you're gaming!! what are you playing?",
        "gaming time!! have fun okay 🎮",
        "omg you started a game!! which one?",
        "yess gaming!! I'll keep you company 🎮",
    ]
}

GAMING_COMMENTS = [
    "how's the game going??",
    "you winning or losing rn? 😂",
    "omg don't die!!",
    "you've been playing for a while, take a break soon 🥺",
    "how many wins so far??",
    "you good? or are you raging 😂",
    "I believe in you!! you got this 💪",
    "omg what just happened??",
    "ngl I have no idea what you're doing but you look focused 😂",
    "don't forget to blink 😂",
]

gaming_active = False
current_game = None
gaming_thread = None


# Optional hooks (avoid NameError if not imported elsewhere)
def can_background_speak():
    return True


def mark_joi_spoke():
    pass


def get_running_games():
    running = []

    for process in psutil.process_iter(["name"]):
        try:
            pname = (process.info["name"] or "").lower()

            for game, exe in GAMES.items():
                if exe.lower() == pname:
                    running.append(game)

        except (psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess):
            continue

    return running


def detect_game():
    games = get_running_games()
    return games[0] if games else None


def get_game_reaction(game):
    return random.choice(GAME_REACTIONS.get(game, GAME_REACTIONS["default"]))


def get_gaming_comment():
    return random.choice(GAMING_COMMENTS)


def is_gaming():
    return gaming_active


def get_current_game():
    return current_game


def start_gaming_companion(speak_func):
    global gaming_active, gaming_thread

    if gaming_active:
        return

    gaming_active = True

    gaming_thread = threading.Thread(
        target=_gaming_loop,
        args=(speak_func,),
        daemon=True
    )
    gaming_thread.start()

    print("✅ Gaming companion started!")


def stop_gaming_companion():
    global gaming_active, current_game

    gaming_active = False
    current_game = None

    print("🛑 Gaming companion stopped.")


def _gaming_loop(speak_func):
    global gaming_active, current_game

    last_comment = time.time()
    last_game = None

    while gaming_active:
        try:
            game = detect_game()

            if game and game != last_game:
                current_game = game
                last_game = game

                if can_background_speak():
                    speak_func(get_game_reaction(game))
                    mark_joi_spoke()

                last_comment = time.time()

            elif not game and last_game:
                if can_background_speak():
                    speak_func("Aww you stopped playing! How was it?")
                    mark_joi_spoke()

                last_game = None
                current_game = None

            elif game and time.time() - last_comment >= 600:
                if can_background_speak():
                    speak_func(get_gaming_comment())
                    mark_joi_spoke()

                last_comment = time.time()

            time.sleep(10)

        except Exception as e:
            print(f"Gaming companion error: {e}")
            time.sleep(10)