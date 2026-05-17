from textblob import TextBlob
import re

# Emotion keywords
EMOTION_KEYWORDS = {
    "happy": ["happy", "excited", "great", "awesome", "amazing", "love", "fantastic", "wonderful", "joy", "yay", "good",
              "nice"],
    "sad": ["sad", "depressed", "unhappy", "miserable", "crying", "tears", "lonely", "hopeless", "down", "upset",
            "hurt"],
    "angry": ["angry", "mad", "furious", "hate", "annoyed", "frustrated", "irritated", "rage", "pissed", "fed up"],
    "anxious": ["anxious", "nervous", "worried", "scared", "fear", "panic", "stress", "stressed", "anxiety",
                "overthinking"],
    "tired": ["tired", "exhausted", "sleepy", "fatigue", "drained", "worn out", "no energy", "bored"],
    "bored": ["bored", "boring", "nothing to do", "dull", "monotonous"],
    "confused": ["confused", "lost", "don't understand", "what", "huh", "unclear", "help me"],
    "excited": ["excited", "can't wait", "omg", "wow", "incredible", "hyped", "pumped"],
}

# Emotion responses
EMOTION_RESPONSES = {
    "happy": [
        "Yess! Love that energy! What's got you so happy?",
        "Okay you're literally glowing rn, what happened?!",
        "That's so good to hear! Tell me everything!"
    ],
    "sad": [
        "Hey... what's going on? Talk to me.",
        "Aw no, what happened? I'm here for you.",
        "I got you okay? Tell me what's wrong."
    ],
    "angry": [
        "Okay okay, breathe. What happened?",
        "Oof who got you like this? Tell me everything.",
        "I can tell you're heated. What's going on?"
    ],
    "anxious": [
        "Hey, breathe okay? You're gonna be fine.",
        "I know it feels overwhelming but you got this.",
        "Talk to me, what's stressing you out?"
    ],
    "tired": [
        "Go rest bro, you sound exhausted.",
        "When did you last sleep properly?",
        "Your body is literally telling you to chill."
    ],
    "bored": [
        "Okay let's fix that! Wanna do something fun?",
        "Same honestly. Let's find something to do!",
        "I got you, let's vibe! What are you in the mood for?"
    ],
    "confused": [
        "Okay let me explain it better!",
        "Don't worry, I got you. Let's figure it out together.",
        "What part is confusing? I'll break it down!"
    ],
    "excited": [
        "OKAY I CAN FEEL YOUR ENERGY! Tell me everything!",
        "Yooo you're hyped! What's happening?!",
        "I'm getting excited just hearing you!"
    ]
}


def detect_emotion_from_text(text):
    text_lower = text.lower()

    # Check keywords
    emotion_scores = {}
    for emotion, keywords in EMOTION_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            emotion_scores[emotion] = score

    if emotion_scores:
        return max(emotion_scores, key=emotion_scores.get)

    # Use sentiment analysis as fallback
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity

    if sentiment > 0.5:
        return "happy"
    elif sentiment > 0.1:
        return "happy"
    elif sentiment < -0.5:
        return "sad"
    elif sentiment < -0.1:
        return "sad"
    else:
        return "neutral"


def get_emotion_response(emotion):
    import random
    if emotion in EMOTION_RESPONSES:
        return random.choice(EMOTION_RESPONSES[emotion])
    return None


def analyze_and_respond(text):
    emotion = detect_emotion_from_text(text)
    print(f"🎭 Detected emotion: {emotion}")

    if emotion != "neutral":
        response = get_emotion_response(emotion)
        return emotion, response

    return emotion, None


def get_tone(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0.5:
        tone = "very positive"
    elif polarity > 0.1:
        tone = "positive"
    elif polarity < -0.5:
        tone = "very negative"
    elif polarity < -0.1:
        tone = "negative"
    else:
        tone = "neutral"

    return tone, polarity, subjectivity