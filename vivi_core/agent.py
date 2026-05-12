from brain import ask
from vivi_core.emotion import detect_emotion, emotion_style_prompt
from vivi_core.memory import MemoryStore
from vivi_core.modes import ModeManager
from vivi_core.tools import ToolRouter


class ViviAgent:
    def __init__(self) -> None:
        self.memory = MemoryStore()
        self.modes = ModeManager()
        self.tools = ToolRouter()

    def respond(self, query: str) -> str:
        q = query.strip()
        if not q:
            return ""

        mode_reply = self._handle_mode_commands(q)
        if mode_reply:
            return mode_reply

        if self.tools.needs_planning(q):
            planned = self.tools.run_plan(q)
            if planned:
                return planned

        tool_result = self.tools.execute(q)
        if tool_result:
            self.memory.add_turn(q, tool_result, "neutral")
            return tool_result

        emotion = detect_emotion(q)
        memory_context = self.memory.context_block(q)
        injected = (
            f"{q}\n\n"
            f"[assistant_style]: {emotion_style_prompt(emotion)}\n"
            f"[mode]: {self.modes.instruction_block()}\n"
            f"[memory_context]:\n{memory_context}"
        )
        answer = ask(injected)
        self.memory.add_turn(q, answer, emotion)
        return answer

    def _handle_mode_commands(self, query: str) -> str | None:
        q = query.lower()
        if q.startswith("set mode "):
            return self.modes.set_mode(query[9:])
        if q.startswith("set personality "):
            return self.modes.set_personality(query[16:])
        if q.startswith("set language "):
            return self.modes.set_language(query[13:])
        if q.startswith("remember that "):
            payload = query[14:]
            if "=" in payload:
                key, value = [x.strip() for x in payload.split("=", 1)]
                self.memory.set_preference(key, value)
                return f"I'll remember that {key} is {value}."
            return "Say it like: remember that favorite_music = lo-fi"
        return None
