from speaker import speak
from skills.system_controls import volume_up, volume_down, media_pause, media_next


def handle_gesture(gesture):
    print(f"Handling gesture: {gesture}")

    if gesture == "fist":
        speak("Got it, pausing!")
        media_pause()

    elif gesture == "open_hand":
        speak("Okay!")

    elif gesture == "peace":
        speak("Peace! What's up?")

    elif gesture == "point":
        speak("Yeah? What do you need?")

    elif gesture == "rock":
        speak("Rock on!")

    elif gesture == "5_fingers" or gesture == "open_hand":
        speak("Volume up!")
        volume_up()

    elif gesture == "fist":
        speak("Volume down!")
        volume_down()

    elif gesture == "2_fingers":
        speak("Next track!")
        media_next()