import schedule, time, threading
from speaker import speak

reminders = []

def set_reminder(task, minutes):
    def remind():
        speak(f"Reminder: {task}")
    schedule.every(minutes).minutes.do(remind).tag(task)
    reminders.append(task)
    return f"Reminder set for {task} in {minutes} minutes."

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Run in background
thread = threading.Thread(target=run_scheduler, daemon=True)
thread.start()