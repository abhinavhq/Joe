class ModeManager:
    def __init__(self) -> None:
        self.mode = "default"
        self.personality = "friendly"
        self.language = "English"

    def set_mode(self, mode_name: str) -> str:
        self.mode = mode_name.lower().strip() or "default"
        return f"Switched to {self.mode} mode."

    def set_personality(self, name: str) -> str:
        self.personality = name.lower().strip() or "friendly"
        return f"Personality changed to {self.personality}."

    def set_language(self, language: str) -> str:
        self.language = language.strip() or "English"
        return f"Language set to {self.language}."

    def instruction_block(self) -> str:
        return (
            f"Current mode: {self.mode}. "
            f"Personality style: {self.personality}. "
            f"Respond in {self.language} unless user asks otherwise."
        )
