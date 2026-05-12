import requests
from config import WEATHER_API_KEY, CITY

def get_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
        data = requests.get(url).json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        humidity = data['main']['humidity']
        return f"It's {temp}°C in {CITY} with {desc}. Humidity is {humidity}%."
    except:
        return "Couldn't fetch weather right now."