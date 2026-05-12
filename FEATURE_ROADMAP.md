# VIVI Advanced Feature Roadmap

This project now has a modular base in `vivi_core/` to support scaling toward a full personal AI assistant.

## Already Added in Code

- Long-term memory foundation (`vivi_core/memory.py`) with:
  - Conversation history
  - Preference storage
  - Lightweight vector-style semantic recall
- Context awareness (multi-turn + retrieved memory context)
- Emotion-aware style adaptation (`vivi_core/emotion.py`)
- Natural TTS fallback chain remains in `speaker.py` (`edge-tts` -> `pyttsx3`)
- Multi-step execution and basic autonomous planning for `and/then` commands (`vivi_core/tools.py`)
- Tool calling router (web/apps/weather/media/music/jokes/system controls)
- Custom modes:
  - `set mode <name>`
  - `set personality <name>`
  - `set language <name>`
- Personalization commands:
  - `remember that key = value`
- Clean architecture split with central orchestrator (`vivi_core/agent.py`)

## Next Steps (high-impact)

1. Wake word + interrupt handling
2. Offline STT/TTS + local LLM fallback
3. OCR + screen understanding + vision pipeline
4. Plugin/skill loader from `plugins/` directory
5. Dashboard UI (Streamlit/PySide) with real-time logs
6. Auth/permissions layer for system actions
7. Cloud sync and multi-device state sync
8. Analytics + robust error fallback policy engine
