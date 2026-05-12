import pywhatkit as kit
import datetime


def send_whatsapp(contact, message):
    try:
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute + 2  # Send 2 minutes from now

        if minute >= 60:
            minute -= 60
            hour += 1

        kit.sendwhatmsg(contact, message, hour, minute)
        return f"WhatsApp message sent to {contact}!"
    except Exception as e:
        return f"WhatsApp error: {e}"


def send_whatsapp_now(contact, message):
    try:
        kit.sendwhatmsg_instantly(contact, message)
        return f"WhatsApp message sent!"
    except Exception as e:
        return f"WhatsApp error: {e}"