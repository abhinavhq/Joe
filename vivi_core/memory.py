import json
import math
import re
from pathlib import Path
from typing import Any


class MemoryStore:
    def __init__(self, db_path: str = "data/memory.json") -> None:
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"history": [], "preferences": {}, "profile": {}}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return {"history": [], "preferences": {}, "profile": {}}

    def _save(self) -> None:
        self.path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")

    def add_turn(self, user_text: str, assistant_text: str, emotion: str) -> None:
        item = {
            "user": user_text,
            "assistant": assistant_text,
            "emotion": emotion,
            "vector": self._vectorize(user_text),
        }
        self.data["history"].append(item)
        self.data["history"] = self.data["history"][-200:]
        self._save()

    def set_preference(self, key: str, value: str) -> None:
        self.data["preferences"][key] = value
        self._save()

    def set_profile(self, key: str, value: str) -> None:
        self.data["profile"][key] = value
        self._save()

    def context_block(self, query: str, max_items: int = 3) -> str:
        history = self.data.get("history", [])
        if not history:
            return ""
        query_vec = self._vectorize(query)
        scored: list[tuple[float, dict[str, Any]]] = []
        for item in history:
            score = self._cosine(query_vec, item.get("vector", []))
            scored.append((score, item))
        best = [x[1] for x in sorted(scored, key=lambda s: s[0], reverse=True)[:max_items] if x[0] > 0]
        if not best:
            return ""
        lines = []
        for item in best:
            lines.append(f'User said: "{item["user"]}" -> You answered: "{item["assistant"]}"')
        return "\n".join(lines)

    def _vectorize(self, text: str, size: int = 128) -> list[float]:
        vec = [0.0] * size
        tokens = re.findall(r"[a-z0-9']+", text.lower())
        if not tokens:
            return vec
        for token in tokens:
            vec[hash(token) % size] += 1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    @staticmethod
    def _cosine(a: list[float], b: list[float]) -> float:
        if not a or not b or len(a) != len(b):
            return 0.0
        return sum(x * y for x, y in zip(a, b))
