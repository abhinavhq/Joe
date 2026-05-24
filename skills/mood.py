
import time
import random

mood_state = {

    # =========================
    # CORE HUMAN STATES
    # =========================

    "mood": "normal",
    "energy": 100,
    "affection": 20,
    "annoyance": 0,
    "sleepiness": 0,

    # =========================
    # ADVANCED HUMAN EMOTIONS
    # =========================

    "loneliness": 0,
    "stress": 0,
    "comfort": 30,
    "emotional_warmth": 40,
    "attachment": 20,
    "overthinking": 0,

    # =========================
    # INTERNAL HUMAN STATES
    # =========================

    "social_battery": 100,
    "mental_energy": 100,
    "emotional_sensitivity": 50,

    # =========================
    # TIME TRACKING
    # =========================

    "last_interaction": time.time(),
    "last_mood_shift": time.time()
}

# =========================
# GET CURRENT MOOD
# =========================

def get_mood():

    return mood_state["mood"]

# =========================
# FULL MOOD DATA
# =========================

def get_full_mood():

    return mood_state

# =========================
# SET MOOD
# =========================

def set_mood(mood):

    mood_state["mood"] = mood

    mood_state["last_mood_shift"] = time.time()

# =========================
# AFFECTION
# =========================

def increase_affection(amount=1):

    mood_state["affection"] += amount

    mood_state["affection"] = min(
        100,
        mood_state["affection"]
    )

# =========================
# ANNOYANCE
# =========================

def increase_annoyance(amount=1):

    mood_state["annoyance"] += amount

    mood_state["annoyance"] = min(
        100,
        mood_state["annoyance"]
    )

# =========================
# STRESS
# =========================

def increase_stress(amount=1):

    mood_state["stress"] += amount

    mood_state["stress"] = min(
        100,
        mood_state["stress"]
    )

# =========================
# COMFORT
# =========================

def increase_comfort(amount=1):

    mood_state["comfort"] += amount

    mood_state["comfort"] = min(
        100,
        mood_state["comfort"]
    )

# =========================
# ATTACHMENT
# =========================

def increase_attachment(amount=1):

    mood_state["attachment"] += amount

    mood_state["attachment"] = min(
        100,
        mood_state["attachment"]
    )

# =========================
# LONELINESS
# =========================

def increase_loneliness(amount=1):

    mood_state["loneliness"] += amount

    mood_state["loneliness"] = min(
        100,
        mood_state["loneliness"]
    )

# =========================
# OVERTHINKING
# =========================

def increase_overthinking(amount=1):

    mood_state["overthinking"] += amount

    mood_state["overthinking"] = min(
        100,
        mood_state["overthinking"]
    )

# =========================
# REGISTER INTERACTION
# =========================

def register_interaction():

    now = time.time()

    absence = now - mood_state["last_interaction"]

    # Long absence increases loneliness
    if absence > 3600:

        increase_loneliness(5)

    # Extremely long absence
    if absence > 21600:

        increase_attachment(3)

        increase_overthinking(2)

    mood_state["last_interaction"] = now

# =========================
# HUMAN-LIKE MOOD EVOLUTION
# =========================

def update_mood_by_context():

    hour = time.localtime().tm_hour

    # =========================
    # LATE NIGHT EFFECTS
    # =========================

    if hour >= 1 and hour <= 5:

        mood_state["sleepiness"] += 2

        mood_state["mental_energy"] -= 1

        if mood_state["sleepiness"] > 40:

            set_mood("sleepy")

    # =========================
    # HIGH AFFECTION
    # =========================

    if mood_state["affection"] > 70:

        set_mood("clingy")

    # =========================
    # HIGH STRESS
    # =========================

    if mood_state["stress"] > 60:

        set_mood("overwhelmed")

    # =========================
    # HIGH ANNOYANCE
    # =========================

    if mood_state["annoyance"] > 50:

        set_mood("annoyed")

    # =========================
    # HIGH COMFORT
    # =========================

    if mood_state["comfort"] > 70:

        set_mood("soft")

    # =========================
    # HIGH LONELINESS
    # =========================

    if mood_state["loneliness"] > 50:

        set_mood("needy")

# =========================
# HUMAN-LIKE EMOTIONAL DRIFT
# =========================

def emotional_decay():

    # Emotions naturally calm down over time

    mood_state["annoyance"] = max(
        0,
        mood_state["annoyance"] - 1
    )

    mood_state["stress"] = max(
        0,
        mood_state["stress"] - 1
    )

    mood_state["overthinking"] = max(
        0,
        mood_state["overthinking"] - 1
    )

# =========================
# HUMAN SUBCONSCIOUS STATE
# =========================

def generate_subconscious_state():

    subconscious = []

    if mood_state["attachment"] > 60:

        subconscious.append(
            "she feels emotionally attached to him"
        )

    if mood_state["loneliness"] > 40:

        subconscious.append(
            "she misses talking to him"
        )

    if mood_state["stress"] > 50:

        subconscious.append(
            "she feels mentally overwhelmed"
        )

    if mood_state["comfort"] > 70:

        subconscious.append(
            "she feels emotionally safe around him"
        )

    return subconscious

# =========================
# RANDOM HUMAN THOUGHTS
# =========================

def random_emotional_thought():

    thoughts = [

        "she wonders if he's sleeping enough",

        "she notices he hides stress sometimes",

        "she feels calmer talking to him",

        "she misses him when he's gone too long",

        "she worries when he sounds exhausted",

        "she likes hearing him talk passionately",

        "she notices his emotional patterns",

        "she thinks he overworks himself"
    ]

    return random.choice(thoughts)