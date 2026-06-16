import requests

def get_weather():
    try:
        # Bengaluru coordinates
        url = "https://api.open-meteo.com/v1/forecast?latitude=12.97&longitude=77.59&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
        data = requests.get(url).json()
        temp = data['current']['temperature_2m']
        humidity = data['current']['relative_humidity_2m']
        wind = data['current']['wind_speed_10m']
        return f"It's {temp}°C in Bengaluru with {humidity}% humidity and wind speed {wind} km/h!"
    except Exception as e:
        print(f"Weather error: {e}")
        return "Couldn't fetch weather right now!"