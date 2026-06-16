import psutil
import threading
import time
import random
import subprocess

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

def get_running_games():
    running = []
    for process in psutil.process_iter(['name']):
        try:
            pname = process.info['name'].lower()
            for game, exe in GAMES.items():
                if exe.lower() in pname:
                    running.append(game)
        except:
            pass
    return running

def detect_game():
    games = get_running_games()
    return games[0] if games else None

def get_game_reaction(game):
    if game in GAME_REACTIONS:
        return random.choice(GAME_REACTIONS[game])
    return random.choice(GAME_REACTIONS["default"])

def get_gaming_comment():
    return random.choice(GAMING_COMMENTS)

def start_gaming_companion(speak_func):
    global gaming_active
    gaming_active = True
    thread = threading.Thread(
        target=_gaming_loop,
        args=(speak_func,),
        daemon=True
    )
    thread.start()
    print("✅ Gaming companion started!")

def _gaming_loop(speak_func):
    global gaming_active, current_game
    last_comment = time.time()
    last_game = None

    while gaming_active:
        try:
            game = detect_game()

            # New game detected!
            if game and game != last_game:
                current_game = game
                last_game = game
                reaction = get_game_reaction(game)
                print(f"🎮 Game detected: {game}")
                speak_func(reaction)
                last_comment = time.time()

            # Game closed
            elif not game and last_game:
                last_game = None
                current_game = None
                speak_func("aw you stopped playing! how was it? 🎮")

            # Random comment while gaming
            elif game and (time.time() - last_comment) > 600:
                comment = get_gaming_comment()
                speak_func(comment)
                last_comment = time.time()

            time.sleep(10)

        except Exception as e:
            print(f"Gaming error: {e}")
            time.sleep(30)

def stop_gaming_companion():
    global gaming_active
    gaming_active = False

def is_gaming():
    return current_game is not None

def get_current_game():
    return current_game