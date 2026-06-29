import webbrowser
import requests
import urllib.parse
import json

# Bengaluru as default location
DEFAULT_CITY = "Bengaluru"
DEFAULT_LAT = 12.9716
DEFAULT_LON = 77.5946


def get_current_location():
    """Get approximate location via IP geolocation - no GPS needed!"""
    try:
        response = requests.get("http://ip-api.com/json/", timeout=5)
        data = response.json()
        if data["status"] == "success":
            return {
                "lat": data["lat"],
                "lon": data["lon"],
                "city": data["city"],
                "region": data["regionName"],
                "country": data["country"]
            }
    except:
        pass
    return {
        "lat": DEFAULT_LAT,
        "lon": DEFAULT_LON,
        "city": DEFAULT_CITY,
        "region": "Karnataka",
        "country": "India"
    }


def get_directions(destination):
    """Open Google Maps with directions from current location"""
    try:
        location = get_current_location()
        origin = f"{location['lat']},{location['lon']}"
        dest_encoded = urllib.parse.quote(destination)

        # Open Google Maps directions
        maps_url = f"https://www.google.com/maps/dir/{origin}/{dest_encoded}"
        webbrowser.open(maps_url)

        # Also get rough distance via OSRM (free, no key)
        dest_coords = geocode_place(destination)
        if dest_coords:
            dist_url = f"http://router.project-osrm.org/route/v1/driving/{location['lon']},{location['lat']};{dest_coords['lon']},{dest_coords['lat']}?overview=false"
            resp = requests.get(dist_url, timeout=10)
            data = resp.json()
            if data.get("routes"):
                distance_km = round(data["routes"][0]["distance"] / 1000, 1)
                duration_min = round(data["routes"][0]["duration"] / 60)
                return f"Opening Google Maps! {destination} is about {distance_km} km away, roughly {duration_min} minutes by car from your location in {location['city']}!"

        return f"Opening Google Maps directions to {destination}!"
    except Exception as e:
        # Fallback — just open maps
        webbrowser.open(f"https://www.google.com/maps/dir//{urllib.parse.quote(destination)}")
        return f"Opening Google Maps to {destination}!"


def find_nearby(place_type):
    """Find nearby places and open in Google Maps"""
    try:
        location = get_current_location()

        # Open Google Maps nearby search
        query = urllib.parse.quote(f"{place_type} near me")
        maps_url = f"https://www.google.com/maps/search/{query}/@{location['lat']},{location['lon']},14z"
        webbrowser.open(maps_url)

        # Get nearby places via Overpass API (free, no key, uses OpenStreetMap)
        place_query = get_osm_query(place_type)
        overpass_url = "http://overpass-api.de/api/interpreter"
        overpass_query = f"""
[out:json][timeout:10];
(
  node[{place_query}](around:2000,{location['lat']},{location['lon']});
);
out body 5;
"""
        resp = requests.post(overpass_url, data=overpass_query, timeout=15)
        data = resp.json()

        places = []
        for element in data.get("elements", [])[:3]:
            name = element.get("tags", {}).get("name", "Unknown")
            if name != "Unknown":
                places.append(name)

        if places:
            place_list = ", ".join(places[:3])
            return f"Found some {place_type} near you! Opening Google Maps. Closest ones include: {place_list}!"
        else:
            return f"Opening Google Maps to find {place_type} near you in {location['city']}!"

    except Exception as e:
        query = urllib.parse.quote(f"{place_type} near me")
        webbrowser.open(f"https://www.google.com/maps/search/{query}")
        return f"Opening Google Maps to find {place_type} near you!"


def get_osm_query(place_type):
    """Map place types to OpenStreetMap tags"""
    mapping = {
        "cafe": '"amenity"="cafe"',
        "cafes": '"amenity"="cafe"',
        "coffee": '"amenity"="cafe"',
        "restaurant": '"amenity"="restaurant"',
        "restaurants": '"amenity"="restaurant"',
        "food": '"amenity"="restaurant"',
        "hospital": '"amenity"="hospital"',
        "pharmacy": '"amenity"="pharmacy"',
        "atm": '"amenity"="atm"',
        "bank": '"amenity"="bank"',
        "petrol": '"amenity"="fuel"',
        "gas station": '"amenity"="fuel"',
        "fuel": '"amenity"="fuel"',
        "hotel": '"tourism"="hotel"',
        "park": '"leisure"="park"',
        "gym": '"leisure"="fitness_centre"',
        "school": '"amenity"="school"',
        "college": '"amenity"="college"',
        "supermarket": '"shop"="supermarket"',
        "mall": '"shop"="mall"',
        "movie": '"amenity"="cinema"',
        "cinema": '"amenity"="cinema"',
        "bar": '"amenity"="bar"',
        "pub": '"amenity"="pub"',
    }
    for key, value in mapping.items():
        if key in place_type.lower():
            return value
    return f'"name"~"{place_type}"'


def geocode_place(place_name):
    """Convert place name to coordinates using Nominatim (free)"""
    try:
        encoded = urllib.parse.quote(place_name)
        url = f"https://nominatim.openstreetmap.org/search?q={encoded}&format=json&limit=1"
        headers = {"User-Agent": "JOI-Assistant/1.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        if data:
            return {"lat": float(data[0]["lat"]), "lon": float(data[0]["lon"])}
    except:
        pass
    return None


def get_location_info():
    """Tell user their current location"""
    location = get_current_location()
    return f"You're currently in {location['city']}, {location['region']}, {location['country']}!"


def search_on_maps(query):
    """Generic maps search"""
    try:
        encoded = urllib.parse.quote(query)
        webbrowser.open(f"https://www.google.com/maps/search/{encoded}")
        return f"Opening Google Maps for {query}!"
    except Exception as e:
        return f"Couldn't open maps: {e}"


def get_distance(destination):
    """Get distance to a place"""
    try:
        location = get_current_location()
        dest_coords = geocode_place(destination)
        if dest_coords:
            dist_url = f"http://router.project-osrm.org/route/v1/driving/{location['lon']},{location['lat']};{dest_coords['lon']},{dest_coords['lat']}?overview=false"
            resp = requests.get(dist_url, timeout=10)
            data = resp.json()
            if data.get("routes"):
                distance_km = round(data["routes"][0]["distance"] / 1000, 1)
                duration_min = round(data["routes"][0]["duration"] / 60)
                return f"{destination} is about {distance_km} km away, roughly {duration_min} minutes by car!"
        return f"Couldn't calculate distance to {destination}!"
    except Exception as e:
        return f"Distance error: {e}"