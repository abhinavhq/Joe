from datetime import datetime

def get_time():
    now = datetime.now()
    hour = now.strftime("%I")
    minute = now.strftime("%M")
    period = now.strftime("%p")
    return f"It's {hour}:{minute} {period}"

def get_date():
    now = datetime.now()
    day = now.strftime("%A")
    date = now.strftime("%d")
    month = now.strftime("%B")
    year = now.strftime("%Y")
    return f"Today is {day}, {date} {month} {year}"

def get_datetime():
    return f"{get_time()} and {get_date()}"