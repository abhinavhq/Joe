from skills.jokes import get_joke
from skills.music import play_music
from skills.open_apps import open_app
from skills.system_controls import media_next, media_pause, media_prev, mute, volume_down, volume_up
from skills.weather import get_weather
from skills.web_search import web_search


class ToolRouter:
    def execute(self, query: str) -> str | None:
        q = query.lower()
        if any(w in q for w in ["search", "google", "look up", "browse"]):
            return web_search(query)
        if any(w in q for w in ["open", "launch", "start"]):
            return open_app(query)
        if any(w in q for w in ["weather", "temperature", "forecast"]):
            return get_weather()
        if any(w in q for w in ["joke", "funny", "laugh"]):
            return get_joke()
        if any(w in q for w in ["volume up", "increase volume", "louder", "turn up"]):
            return volume_up()
        if any(w in q for w in ["volume down", "decrease volume", "quieter", "turn down"]):
            return volume_down()
        if any(w in q for w in ["mute", "silence"]):
            return mute()
        if any(w in q for w in ["pause", "resume", "play pause"]):
            return media_pause()
        if any(w in q for w in ["next song", "next track", "skip"]):
            return media_next()
        if any(w in q for w in ["previous song", "prev track", "go back"]):
            return media_prev()
        if any(w in q for w in ["play", "music", "song"]):
            return play_music(query)
        return None

    def needs_planning(self, query: str) -> bool:
        q = query.lower()
        return " and " in q or " then " in q

    def run_plan(self, query: str) -> str | None:
        parts = [p.strip() for p in query.replace(" then ", " and ").split(" and ") if p.strip()]
        if len(parts) < 2:
            return None
        outputs = []
        for part in parts:
            out = self.execute(part)
            if out:
                outputs.append(out)
        if not outputs:
            return None
        return " | ".join(outputs)
