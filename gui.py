import customtkinter as ctk
import threading
from speaker import speak
from listener import listen
from brain import ask
from skills.web_search import web_search
from skills.open_apps import open_app
from skills.weather import get_weather
from skills.jokes import get_joke
from skills.music import play_music
from skills.reminders import set_reminder
from skills.system_controls import volume_up, volume_down, mute, media_pause, media_next, media_prev
from skills.wake_word import listen_for_wake_word
from skills.memory import save_memory, get_memory
from skills.personality import set_personality
from skills.datetime_skill import get_time, get_date
from skills.news import get_news
import re

# Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ViviGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("VIVI - AI Assistant")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.is_listening = False
        self.setup_ui()

    def setup_ui(self):
        # Title
        self.title_label = ctk.CTkLabel(
            self.root,
            text="✨ VIVI",
            font=ctk.CTkFont(size=40, weight="bold"),
            text_color="#FF69B4"
        )
        self.title_label.pack(pady=20)

        # Status
        self.status_label = ctk.CTkLabel(
            self.root,
            text="Say 'Hey Vivi' to wake me up!",
            font=ctk.CTkFont(size=16),
            text_color="#888888"
        )
        self.status_label.pack(pady=5)

        # Chat box
        self.chat_box = ctk.CTkTextbox(
            self.root,
            width=740,
            height=300,
            font=ctk.CTkFont(size=14),
            corner_radius=15
        )
        self.chat_box.pack(pady=15, padx=20)
        self.chat_box.configure(state="disabled")

        # Input frame
        self.input_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.input_frame.pack(pady=10, padx=20, fill="x")

        # Text input
        self.text_input = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Type a message or use voice...",
            font=ctk.CTkFont(size=14),
            height=45,
            corner_radius=10,
            width=550
        )
        self.text_input.pack(side="left", padx=5)
        self.text_input.bind("<Return>", self.send_text)

        # Send button
        self.send_btn = ctk.CTkButton(
            self.input_frame,
            text="Send",
            command=self.send_text,
            width=80,
            height=45,
            corner_radius=10,
            fg_color="#FF69B4",
            hover_color="#FF1493"
        )
        self.send_btn.pack(side="left", padx=5)

        # Voice button
        self.voice_btn = ctk.CTkButton(
            self.input_frame,
            text="🎙️ Voice",
            command=self.toggle_voice,
            width=100,
            height=45,
            corner_radius=10,
            fg_color="#9B59B6",
            hover_color="#8E44AD"
        )
        self.voice_btn.pack(side="left", padx=5)

        # Mode buttons
        self.mode_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.mode_frame.pack(pady=10)

        modes = [
            ("📚 Study", "study"),
            ("🔥 Hype", "hype"),
            ("😎 Chill", "chill"),
            ("💀 Roast", "roast"),
            ("😊 Normal", "normal"),
        ]

        for label, mode in modes:
            btn = ctk.CTkButton(
                self.mode_frame,
                text=label,
                command=lambda m=mode: self.switch_mode(m),
                width=100,
                height=35,
                corner_radius=10,
            )
            btn.pack(side="left", padx=5)

    def add_message(self, sender, message):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"{sender}: {message}\n\n")
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")

    def update_status(self, text):
        self.status_label.configure(text=text)

    def handle(self, query):
        if not query:
            return
        self.add_message("You", query)

        if any(w in query for w in ["search", "google", "look up"]):
            reply = web_search(query)
        elif any(w in query for w in ["open", "launch", "start"]):
            reply = open_app(query)
        elif any(w in query for w in ["weather", "temperature", "forecast"]):
            reply = get_weather()
        elif any(w in query for w in ["joke", "funny", "laugh"]):
            reply = get_joke()
        elif any(w in query for w in ["what time", "current time", "time now"]):
            reply = get_time()
        elif any(w in query for w in ["what date", "today's date", "what day"]):
            reply = get_date()
        elif any(w in query for w in ["news", "headlines", "what's happening"]):
            reply = get_news()
        elif any(w in query for w in ["volume up", "louder", "turn up"]):
            reply = volume_up()
        elif any(w in query for w in ["volume down", "quieter", "turn down"]):
            reply = volume_down()
        elif any(w in query for w in ["mute", "silence"]):
            reply = mute()
        elif any(w in query for w in ["pause", "resume"]):
            reply = media_pause()
        elif any(w in query for w in ["next song", "skip"]):
            reply = media_next()
        elif any(w in query for w in ["previous song", "go back"]):
            reply = media_prev()
        elif any(w in query for w in ["play", "music", "song"]):
            reply = play_music(query)
        elif "remind" in query:
            match = re.search(r"remind me to (.+) in (\d+)", query)
            if match:
                task, mins = match.group(1), int(match.group(2))
                reply = set_reminder(task, mins)
            else:
                reply = "Please say: remind me to [task] in [X] minutes"
        elif "my name is" in query:
            name = query.replace("my name is", "").strip()
            save_memory("user", "name", name)
            reply = f"Got it! I'll remember your name is {name}!"
        else:
            reply = ask(query)

        self.add_message("VIVI 💜", reply)
        threading.Thread(target=speak, args=(reply,), daemon=True).start()
        self.update_status("Listening...")

    def send_text(self, event=None):
        query = self.text_input.get().strip().lower()
        if query:
            self.text_input.delete(0, "end")
            threading.Thread(target=self.handle, args=(query,), daemon=True).start()

    def toggle_voice(self):
        if not self.is_listening:
            self.is_listening = True
            self.voice_btn.configure(text="🔴 Stop", fg_color="#E74C3C")
            self.update_status("🎙️ Listening...")
            threading.Thread(target=self.voice_listen, daemon=True).start()
        else:
            self.is_listening = False
            self.voice_btn.configure(text="🎙️ Voice", fg_color="#9B59B6")
            self.update_status("Stopped listening")

    def voice_listen(self):
        query = listen()
        if query:
            self.handle(query)
        self.is_listening = False
        self.voice_btn.configure(text="🎙️ Voice", fg_color="#9B59B6")

    def switch_mode(self, mode):
        result = set_personality(mode)
        self.add_message("VIVI 💜", f"Switched to {mode} mode!")
        self.update_status(f"{mode.title()} mode active")

    def run(self):
        name = get_memory("user", "name")
        greeting = f"Hey {name}! I'm back!" if name else "Hey! I'm Vivi!"
        self.add_message("VIVI 💜", greeting)
        self.root.mainloop()


if __name__ == "__main__":
    app = ViviGUI()
    app.run()