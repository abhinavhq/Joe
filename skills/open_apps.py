import subprocess
import os
import webbrowser

APPS = {
    # Browsers
    "brave":        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    "edge":         r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",

    # Communication
    "discord":      r"C:\Users\abhinav yadav\AppData\Local\Discord\app-1.0.9233\Discord.exe",
    "whatsapp":     r"C:\Users\abhinav yadav\AppData\Roaming\WhatsApp\WhatsApp.exe",
    "telegram":     r"C:\Users\abhinav yadav\AppData\Roaming\Telegram Desktop\Telegram.exe",

    # Web
    "youtube":      "https://www.youtube.com",
    "chrome":       r"C:\Program Files\Google\Chrome\Application\chrome.exe",

    # Music
    "spotify":      r"C:\Users\abhinav yadav\AppData\Roaming\Spotify\Spotify.exe",
    "vlc":          r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",

    # Development
    "pycharm":      r"C:\Program Files\JetBrains\PyCharm 2025.1.1.1\bin\pycharm64.exe",
    "vscode":       r"C:\Users\abhinav yadav\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "cursor":       r"C:\Users\abhinav yadav\AppData\Local\Programs\cursor\Cursor.exe",
    "sublime":      r"C:\Program Files\Sublime Text\sublime_text.exe",
    "github":       r"C:\Users\abhinav yadav\AppData\Local\GitHubDesktop\GitHubDesktop.exe",
    "postman":      r"C:\Users\abhinav yadav\AppData\Local\Postman\Postman.exe",
    "replit":       r"C:\Users\abhinav yadav\AppData\Local\replit\Replit.exe",

    # Games
    "steam":        r"C:\Program Files (x86)\Steam\steam.exe",
    "epic":         r"C:\Program Files\Epic Games\Launcher\Portal\Binaries\Win64\EpicGamesLauncher.exe",
    "roblox":       r"C:\Users\abhinav yadav\AppData\Local\Roblox\Versions\version-80c7b8e578f241ff\RobloxPlayerBeta.exe",
    "minecraft":    r"C:\Users\abhinav yadav\AppData\Roaming\Minecraft\LL.exe",
    "hoyo":         r"C:\Program Files\HoYoPlay\launcher.exe",
    "vtube":        r"C:\Program Files (x86)\Steam\steamapps\common\VTube Studio\VTube Studio.exe",
    "desktop mate": r"C:\Program Files (x86)\Steam\steamapps\common\Desktop Mate\DesktopMate.exe",

    # Tools
    "notepad":      "notepad.exe",
    "calculator":   "calc.exe",
    "paint":        "mspaint.exe",
    "ollama":       r"C:\Users\abhinav yadav\AppData\Local\Programs\Ollama\ollama app.exe",
    "virtualbox":   r"C:\Program Files\Oracle\VirtualBox\VirtualBox.exe",
    "anki":         r"C:\Users\abhinav yadav\AppData\Local\Programs\Anki\anki.exe",
    "snipping":     r"C:\Users\abhinav yadav\AppData\Local\Microsoft\WindowsApps\SnippingTool.exe",
}

def open_app(query):
    for app, path in APPS.items():
        if app in query:
            try:
                if path.startswith("http"):
                    webbrowser.open(path)
                    return f"Opening {app}!"
                else:
                    os.startfile(os.path.expandvars(path))
                    return f"Opening {app}!"
            except:
                try:
                    subprocess.Popen(path, shell=True)
                    return f"Opening {app}!"
                except:
                    return f"Couldn't open {app}!"
    return "I couldn't find that app. Try saying the exact name!"