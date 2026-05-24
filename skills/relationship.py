import time
import random

relationship = {

    # =========================
    # CORE RELATIONSHIP
    # =========================

    "trust": 10,
    "comfort": 10,
    "attachment": 10,
    "bond_level": 1,

    # =========================
    # HUMAN EMOTIONAL STATES
    # =========================

    "jealousy": 0,
    "emotional_dependence": 0,
    "emotional_safety": 20,
    "vulnerability": 5,

    # =========================
    # INTERACTION TRACKING
    # =========================

    "last_interaction": time.time(),
    "days_together": 0
}

# =========================
# GET DATA
# =========================

def get_relationship():

    return relationship

# =========================
# TRUST
# =========================

def increase_trust(amount=1):

    relationship["trust"] += amount

    relationship["trust"] = min(
        100,
        relationship["trust"]
    )

# =========================
# COMFORT
# =========================

def increase_comfort(amount=1):

    relationship["comfort"] += amount

    relationship["comfort"] = min(
        100,
        relationship["comfort"]
    )

# =========================
# ATTACHMENT
# =========================

def increase_attachment(amount=1):

    relationship["attachment"] += amount

    relationship["attachment"] = min(
        100,
        relationship["attachment"]
    )

# =========================
# EMOTIONAL SAFETY
# =========================

def increase_emotional_safety(amount=1):

    relationship["emotional_safety"] += amount

    relationship["emotional_safety"] = min(
        100,
        relationship["emotional_safety"]
    )

# =========================
# VULNERABILITY
# =========================

def increase_vulnerability(amount=1):

    relationship["vulnerability"] += amount

    relationship["vulnerability"] = min(
        100,
        relationship["vulnerability"]
    )

# =========================
# JEALOUSY
# =========================

def increase_jealousy(amount=1):

    relationship["jealousy"] += amount

    relationship["jealousy"] = min(
        100,
        relationship["jealousy"]
    )

# =========================
# DEPENDENCE
# =========================

def increase_dependence(amount=1):

    relationship["emotional_dependence"] += amount

    relationship["emotional_dependence"] = min(
        100,
        relationship["emotional_dependence"]
    )

# =========================
# UPDATE RELATIONSHIP
# =========================

def update_relationship():

    total = (
        relationship["trust"] +
        relationship["comfort"] +
        relationship["attachment"] +
        relationship["emotional_safety"]
    )

    relationship["bond_level"] = min(
        10,
        total // 40
    )

# =========================
# HUMAN-LIKE EVOLUTION
# =========================

def evolve_relationship():

    # Higher bond = more vulnerability
    if relationship["bond_level"] > 5:

        increase_vulnerability(1)

    # High attachment creates dependence
    if relationship["attachment"] > 70:

        increase_dependence(1)

    # Emotional safety boosts trust
    if relationship["emotional_safety"] > 60:

        increase_trust(1)

# =========================
# ABSENCE REACTION
# =========================

def process_absence():

    now = time.time()

    absence = now - relationship["last_interaction"]

    # Long absence increases attachment feelings
    if absence > 7200:

        increase_attachment(2)

        increase_dependence(1)

    relationship["last_interaction"] = now