import requests

def get_joke():
    try:
        res = requests.get("https://official-joke-api.appspot.com/random_joke").json()
        return f"{res['setup']} ... {res['punchline']}"
    except:
        return "Why do programmers prefer dark mode? Because light attracts bugs!"