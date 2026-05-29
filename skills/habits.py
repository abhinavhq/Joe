import time
from collections import defaultdict

habit_memory = {
    "active_hours": defaultdict(int),
    "topics": defaultdict(int),
    "emotions": defaultdict(int),
    "patterns": []
}

def learn_habits(query, emotion):

    hour = time.localtime().tm_hour

    # =========================
    # ACTIVE HOURS
    # =========================

    habit_memory["active_hours"][hour] += 1

    # =========================
    # EMOTIONAL PATTERNS
    # =========================

    habit_memory["emotions"][emotion] += 1

    # =========================
    # TOPIC DETECTION
    # =========================

    topics = [
        "anime",
        "gaming",
        "coding",
        "japan",
        "music",
        "sleep",
        "stress",
        "genshin",
        "k-pop",
        "movies"
        "guitar"
        "life"
        "k-pop",
        "k-drama",
        "figurines",
        "daily conversations"
        "life"
    ]

    query_lower = query.lower()

    for topic in topics:

        if topic in query_lower:

            habit_memory["topics"][topic] += 1

def generate_habit_observation():

    observations = []

    # =========================
    # NIGHT OWL DETECTION
    # =========================

    late_night_activity = sum(
        count
        for hour, count in habit_memory["active_hours"].items()
        if hour >= 1 and hour <= 5
    )

    if late_night_activity > 5:

        observations.append(
            "he stays awake really late a lot"
        )

    # =========================
    # CODING HABIT
    # =========================

    if habit_memory["topics"]["coding"] > 5:

        observations.append(
            "he spends a lot of time coding"
        )

    # =========================
    # STRESS PATTERN
    # =========================

    if habit_memory["emotions"]["sad"] > 5:

        observations.append(
            "he hides stress sometimes"
        )

    return observations



