# JOI — Personal AI Voice Assistant 🤖

> *"She's not an AI. She's Joi."*

JOI is a fully local, human-like AI voice assistant built in Python. She talks, listens, remembers, feels emotions, watches your screen, recognizes your face, plays music, controls your PC, tracks crypto/stocks, and genuinely feels like a real companion — not a generic chatbot.

---

## ✨ Features

### 🧠 AI & Personality
- Powered by **Cerebras** (ultra-fast LLM inference) with `gpt-oss-120b`
- Human-like personality — casual, flirty, caring, emotionally reactive
- Mood system with real emotional states (playful, soft, tired, clingy, annoyed)
- Relationship progression — gets closer to you over time
- Dynamic personality that shifts based on time of day and your mood

### 🎙️ Voice
- **Cartesia TTS** (`sonic-2`) for ultra-realistic voice with emotion control
- Edge TTS fallback (free, unlimited)
- Voice emotion system — speaks faster when excited, softer when sad
- Interruption handling — stops talking when you speak
- Filler words ("umm", "okay so", "ngl") for natural feel
- Laugh/giggle reactions

### 👂 Listening
- Wake word detection — *"Hey Joi"*
- Google Speech Recognition for voice input
- Proactive messages — she texts you first every 10 minutes

### 🧠 Memory
- Long-term memory via SQLite
- Semantic memory — learns your preferences, habits, and patterns
- Remembers your name, likes, dislikes, and past conversations forever

### 😊 Emotion Detection
- Detects emotions from text (happy, sad, angry, anxious, tired, lonely)
- TextBlob sentiment analysis as fallback
- Adjusts her voice and response style based on your detected emotion

### 👁️ Vision (Local, No API)
- **Ollama + gemma3:4b** running 100% offline
- Object identification from camera
- Anime character recognition
- Scene description
- Text reading (OCR from camera)
- Food identification
- Document reading
- Screen content reading

### 🖥️ Screen Awareness
- Watches your screen every 5 minutes
- Comments naturally on what you're doing
- *"omg are you still coding?? take a break!"*

### 👤 Face Recognition
- OpenCV LBPH face recognizer (no dlib needed)
- Registers and recognizes your face
- Presence detection — greets you when you sit down

### 🎮 Gaming Companion
- Detects running games (Roblox, Minecraft, Valorant, GTA, Steam, etc.)
- Reacts when you start/stop playing
- Sends periodic comments while you game

### 💰 Finance & Crypto
- Live crypto prices via CoinGecko (free, no key)
- Live stock prices via Alpha Vantage
- RSI + trend analysis
- AI-generated bullish/bearish outlook
- Market overview (BTC dominance, total market cap)

### 🗺️ Maps & GPS
- Auto-detects your current city via IP
- Voice-controlled Google Maps directions
- Find nearby places (cafes, restaurants, hospitals, ATMs)
- Distance and travel time calculation
- All free, no API key needed

### 🌤️ Weather
- Auto-detects your location
- Real-time weather via Open-Meteo (free, no key)
- Feels-like temperature, humidity, wind, conditions
- Ask about any city — *"weather in Mumbai"*

### 💻 System Control (30+ commands)
- Volume up/down/mute/unmute
- Brightness up/down
- Shutdown/restart/sleep/hibernate/lock
- Media controls (pause, next, previous)
- Open task manager, file explorer, settings
- Toggle WiFi, empty recycle bin, quick screenshot
- Show desktop, minimize all windows

### 📱 App Control (30+ apps)
- Spotify, Discord, WhatsApp, Telegram
- Steam, Roblox, Minecraft, Epic Games
- Chrome, Brave, Edge, PyCharm, VSCode, Cursor
- VTube Studio, Desktop Mate, Ollama, VirtualBox
- Notepad, Calculator, Paint, VLC, Anki, Postman

### 🎵 Music
- Play any song on YouTube by voice
- Spotify search via URI
- Pause, next, previous track controls

### 🌐 Browser Control
- Open any website
- Scroll up/down/top/bottom
- New tab, close tab, switch tabs
- Go back/forward, refresh
- Zoom in/out/reset
- Find text on page

### 📰 Info & Search
- Google News headlines
- Wikipedia search
- Web scraping fallback
- Joke generator

### 💬 WhatsApp
- Send messages to contacts by voice

### ⏰ Reminders
- Voice-set reminders with scheduled alerts

## 🤖 Desktop Avatar
- Mate Engine integration (Live2D-style avatar)
- Auto starts/stops with JOI

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM | Cerebras API (`gpt-oss-120b`) |
| TTS | Cartesia (`sonic-2`) + Edge TTS fallback |
| STT | Google Speech Recognition |
| Vision | Ollama + gemma3:4b (local, offline) |
| Face Recognition | OpenCV LBPH |
| Emotion Detection | TextBlob + keyword matching |
| Memory | SQLite |
| Crypto Data | CoinGecko API (free) |
| Stock Data | Alpha Vantage API (free) |
| Weather | Open-Meteo API (free) |
| Maps | OpenStreetMap + OSRM + Nominatim (free) |
| Avatar | Mate Engine |
| Language | Python 3.11 |

---

## 📁 Project Structure

```
Joe/
├── main.py                 # Entry point, command handler
├── brain.py                # AI prompt builder, memory + emotion fusion
├── llm.py                  # Cerebras API client
├── speaker.py              # TTS (Cartesia + Edge TTS), voice emotion
├── listener.py             # Speech recognition
├── config.py               # API keys and settings
├── skills/
│   ├── web_search.py       # Google search
│   ├── open_apps.py        # App launcher (30+ apps)
│   ├── weather.py          # Auto-location weather
│   ├── jokes.py            # Joke generator
│   ├── music.py            # YouTube + Spotify music
│   ├── reminders.py        # Voice reminders
│   ├── system_controls.py  # PC controls (volume, power, etc.)
│   ├── wake_word.py        # Wake word detection
│   ├── memory.py           # SQLite conversation memory
│   ├── semantic_memory.py  # Long-term semantic memory
│   ├── personality.py      # Personality modes + dynamic style
│   ├── datetime_skill.py   # Time and date
│   ├── news.py             # Google News RSS
│   ├── browser.py          # Selenium browser control
│   ├── system_info.py      # CPU, RAM, disk, battery
│   ├── screenshot_ocr.py   # Screenshot + OCR
│   ├── whatsapp.py         # WhatsApp messaging
│   ├── knowledge.py        # Wikipedia + web scraping
│   ├── vision.py           # Local Ollama vision (camera)
│   ├── screen_awareness.py # Screen watching + comments
│   ├── face_recognition.py # OpenCV face recognition
│   ├── gaming.py           # Game detection + companion
│   ├── emotion_detection.py# Text emotion detection
│   ├── mood.py             # JOI's mood state system
│   ├── relationship.py     # Relationship progression
│   ├── habits.py           # Habit learning
│   ├── time_awareness.py   # Time-of-day context
│   ├── proactive.py        # Proactive message system
│   ├── speech_gate.py      # Background speech controller
│   ├── sounds.py           # Laugh/giggle sounds
│   ├── filler_words.py     # Natural filler words
│   ├── finance.py          # Crypto + stock prices
│   ├── maps.py             # GPS + Google Maps
│   └── mate_engine.py      # Desktop avatar control
├── known_faces/            # Stored face data
├── sounds/                 # Sound files
└── requirements.txt        # Python dependencies
```

---

## 🚀 Setup

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/JOI.git
cd JOI
```

### 2. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Ollama (for local vision)
Download from [ollama.com](https://ollama.com/download) and pull the vision model:
```bash
ollama pull gemma3:4b
```

### 5. Configure API keys
Create/edit `config.py`:
```python
CEREBRAS_API_KEY = "your-cerebras-key"
CARTESIA_API_KEY = "your-cartesia-key"      # optional, Edge TTS works without it
ALPHA_VANTAGE_API_KEY = "your-av-key"       # optional, for stock prices
ASSISTANT_NAME = "JOI"
CITY = "Bengaluru"                           # your city
CONTACTS = {
    "mom": "+91XXXXXXXXXX",
    "dad": "+91XXXXXXXXXX",
}
```

### 6. Run JOI
```bash
python main.py
```

Say **"Hey Joi"** to wake her up!

---

## 🗣️ Voice Commands (100+)

### Basic
| Say | Action |
|---|---|
| *"Hey Joi"* | Wake word |
| *"what time is it"* | Current time |
| *"what's the date"* | Current date |
| *"tell me a joke"* | Random joke |
| *"bye"* | Exit |

### AI Chat
| Say | Action |
|---|---|
| *"how are you"* | She responds naturally |
| *"I'm feeling sad"* | Emotional support |
| *"I'm bored"* | She suggests things |
| *"roast me"* | Gets savage 😂 |

### Vision
| Say | Action |
|---|---|
| *"what is this"* | Identifies object via camera |
| *"which character is this"* | Identifies anime character |
| *"read this"* | Reads text from camera |
| *"describe the scene"* | Describes surroundings |
| *"who is this"* | Describes person |

### Finance
| Say | Action |
|---|---|
| *"bitcoin price"* | Live BTC price + analysis |
| *"ethereum price"* | Live ETH data |
| *"apple stock"* | AAPL price + RSI |
| *"tesla stock"* | TSLA analysis |
| *"crypto market"* | Market overview |

### Maps
| Say | Action |
|---|---|
| *"where am I"* | Current location |
| *"directions to Forum Mall"* | Opens Google Maps |
| *"find cafes near me"* | Nearby cafes |
| *"how far is MG Road"* | Distance + travel time |

### System
| Say | Action |
|---|---|
| *"volume up/down"* | Adjust volume |
| *"brightness up/down"* | Adjust brightness |
| *"shutdown"* | Shutdown PC |
| *"lock"* | Lock screen |
| *"show desktop"* | Minimize all windows |

---

## ⚙️ Requirements

```
cerebras-openai
cartesia
edge-tts
pygame
SpeechRecognition
pyaudio
opencv-python
numpy
requests
pyautogui
pillow
textblob
psutil
pygetwindow
pycaw
comtypes
selenium
webdriver-manager
pywhatkit
wikipedia
beautifulsoup4
screen-brightness-control
```

---

## 🔑 Free APIs Used

| Service | Purpose | Cost |
|---|---|---|
| CoinGecko | Crypto prices | Free, no key |
| Open-Meteo | Weather | Free, no key |
| OpenStreetMap/OSRM | Maps/routing | Free, no key |
| ip-api.com | Location detection | Free, no key |
| Google News RSS | Headlines | Free, no key |
| Overpass API | Nearby places | Free, no key |
| Alpha Vantage | Stock prices | Free tier (25 req/day) |
| Cerebras | LLM inference | Free tier available |

---

## 🤝 Contributing

Pull requests welcome! Some ideas for contributions:
- Hindi language support
- More game detections in `gaming.py`
- Additional app support in `open_apps.py`
- Better anime character recognition prompts
- GPU-accelerated vision support

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 👤 Author

Built by **Abhinav** — CS student from Bengaluru 🇮🇳

> *Inspired by the movie Her and the concept of a truly personal AI companion.*

---

⭐ *Star this repo if JOI helped you!*
