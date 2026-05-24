from datetime import datetime


def get_time_of_day():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"


def get_time_greeting():
    tod = get_time_of_day()
    greetings = {
        "morning": [
            "good morning!! did you sleep okay? 🥺",
            "hey!! you're up early, how you feeling?",
            "morning!! hope you slept well 😊"
        ],
        "afternoon": [
            "hey!! how's your day going so far?",
            "afternoon! you eating properly today? 😤",
            "hey you! how's everything going?"
        ],
        "evening": [
            "hey!! how was your day? tell me everything",
            "evening! you must be tired, how'd it go?",
            "hey!! finally done for the day?"
        ],
        "night": [
            "why are you still up?? 😭 everything okay?",
            "it's so late!! can't sleep?",
            "hey night owl 😂 what's keeping you up?"
        ]
    }
    import random
    return random.choice(greetings[tod])


def get_time_context():
    tod = get_time_of_day()
    hour = datetime.now().hour

    context = f"Current time of day: {tod} ({hour}:00). "

    if tod == "morning":
        context += "Be cheerful and ask if they slept well."
    elif tod == "afternoon":
        context += "Be casual, ask about their day."
    elif tod == "evening":
        context += "Be warm, ask how their day went."
    elif tod == "night":
        context += "Be softer and more personal. Late night convos are deeper. Ask why they're still up."

    return context


def should_check_in():
    hour = datetime.now().hour
    # Check in during these hours
    return hour in [9, 13, 18, 22]