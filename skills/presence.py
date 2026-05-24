import time

last_seen = time.time()

def update_presence():

    global last_seen

    last_seen = time.time()

def get_absence_time():

    return time.time() - last_seen

def get_presence_message():

    absence = get_absence_time()

    # 5 minutes
    if absence > 300 and absence < 1800:

        return "you're backkk 😭"

    # 30 minutes
    elif absence >= 1800 and absence < 7200:

        return "where did you disappear to 😒"

    # 2+ hours
    elif absence >= 7200:

        return "you were gone forever omg 😭"

    return None