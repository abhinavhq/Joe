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
"lonely": ["lonely", "alone", "no one", "nobody", "miss", "missing", "empty", "isolated"],
}

# Emotion responses
EMOTION_RESPONSES = {
    "happy": [
        "OKAY YOUR ENERGY IS CONTAGIOUS RN 😆 what happened tell me everything!!",
        "yess finally!! you seem so happy rn I love it 🥺 what's going on?",
        "omg you're literally glowing through the screen what happened?!"
    ],
    "sad": [
        "hey... talk to me okay? what's going on 🥺",
        "nooo what happened? I'm right here, tell me everything",
        "aw don't be sad 😢 I'm here okay? what's wrong?"
    ],
    "angry": [
        "okay okay breathe 😤 who did what now??",
        "ugh I can tell you're heated — spill, what happened",
        "ngl I'm ready to be mad with you 😤 what's going on?"
    ],
    "anxious": [
        "hey hey hey — breathe okay? you're gonna be fine I promise 🥺",
        "I know it feels like a lot rn but you literally got this",
        "talk to me, what's stressing you out? let's figure it out together"
    ],
    "tired": [
        "go sleep dummy 😂 your body is literally begging you",
        "when did you last actually sleep?? go rest I'll be here when you wake up",
        "you sound exhausted ngl, please go rest 🥺"
    ],
    "bored": [
        "okay we are NOT doing bored rn — what are you in the mood for?",
        "same honestly 😂 let's find something fun to do",
        "bored?? with me around?? impossible, let's vibe"
    ],
    "excited": [
        "OKAY YOUR ENERGY 😆😆 tell me EVERYTHING right now!!",
        "yooo I'm getting hyped just hearing you!! what's happening??",
        "WAIT WAIT WAIT tell me more I need to know everything!!"
    ],
    "confused": [
        "okay okay don't stress — let's figure it out together",
        "I got you! what part is confusing? I'll break it down",
        "no no don't worry, I'll explain it better!"
    ],
    "lonely": [
        "hey I'm right here okay? you're not alone 🥺",
        "aww come talk to me then, I'm always here",
        "I'm here! always. you know that right? 🥺"
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