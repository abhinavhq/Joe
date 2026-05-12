def detect_emotion(text: str) -> str:
    q = text.lower()
    if any(w in q for w in ["sad", "down", "upset", "depressed", "cry"]):
        return "sad"
    if any(w in q for w in ["angry", "mad", "annoyed", "furious"]):
        return "angry"
    if any(w in q for w in ["happy", "excited", "great", "awesome", "love"]):
        return "happy"
    if any(w in q for w in ["afraid", "nervous", "anxious", "scared"]):
        return "anxious"
    return "neutral"


def emotion_style_prompt(emotion: str) -> str:
    mapping = {
        "sad": "Be warm, gentle, and comforting.",
        "angry": "Stay calm, grounded, and solution-oriented.",
        "happy": "Match the excitement and energy.",
        "anxious": "Use reassuring and practical language.",
        "neutral": "Be natural and conversational.",
    }
    return mapping.get(emotion, mapping["neutral"])
