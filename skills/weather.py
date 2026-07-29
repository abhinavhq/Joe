import requests

def get_current_city():
    try:
        response = requests.get("http://ip-api.com/json/", timeout=5)
        data = response.json()
        if data["status"] == "success":
            return {
                "city": data["city"],
                "lat": data["lat"],
                "lon": data["lon"]
            }
    except:
        pass
    return {"city": "Bengaluru", "lat": 12.97, "lon": 77.59}

def get_weather():
    try:
        location = get_current_city()
        lat = location["lat"]
        lon = location["lon"]
        city = location["city"]

        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,apparent_temperature"
        data = requests.get(url, timeout=10).json()

        temp = data['current']['temperature_2m']
        feels_like = data['current']['apparent_temperature']
        humidity = data['current']['relative_humidity_2m']
        wind = data['current']['wind_speed_10m']
        code = data['current']['weather_code']

        # Weather condition from code
        condition = get_weather_condition(code)

        return f"It's {temp}°C in {city} right now, feels like {feels_like}°C. {condition} with {humidity}% humidity and wind at {wind} km/h!"
    except Exception as e:
        print(f"Weather error: {e}")
        return "Couldn't fetch weather right now!"

def get_weather_condition(code):
    if code == 0:
        return "Clear sky ☀️"
    elif code in [1, 2, 3]:
        return "Partly cloudy ⛅"
    elif code in [45, 48]:
        return "Foggy 🌫️"
    elif code in [51, 53, 55]:
        return "Drizzling 🌦️"
    elif code in [61, 63, 65]:
        return "Rainy 🌧️"
    elif code in [71, 73, 75]:
        return "Snowing ❄️"
    elif code in [80, 81, 82]:
        return "Rain showers 🌧️"
    elif code in [95, 96, 99]:
        return "Thunderstorm ⛈️"
    else:
        return "Cloudy ☁️"

def get_weather_for_city(city_name):
    try:
        # Geocode the city
        from skills.maps import geocode_place
        coords = geocode_place(city_name)
        if not coords:
            return f"Couldn't find {city_name}!"

        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,apparent_temperature"
        data = requests.get(url, timeout=10).json()

        temp = data['current']['temperature_2m']
        feels_like = data['current']['apparent_temperature']
        humidity = data['current']['relative_humidity_2m']
        wind = data['current']['wind_speed_10m']
        code = data['current']['weather_code']
        condition = get_weather_condition(code)

        return f"It's {temp}°C in {city_name} right now, feels like {feels_like}°C. {condition} with {humidity}% humidity and wind at {wind} km/h!"
    except Exception as e:
        return f"Couldn't fetch weather for {city_name}!"