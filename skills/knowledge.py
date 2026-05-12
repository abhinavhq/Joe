import urllib.request
import json
from bs4 import BeautifulSoup


def search_wikipedia(query):
    try:
        # Clean query
        search = query.replace(" ", "+")

        # Search Wikipedia API
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())

        if "extract" in data:
            # Get first 3 sentences
            extract = data["extract"]
            sentences = extract.split(". ")[:3]
            result = ". ".join(sentences)
            return f"According to Wikipedia: {result}"
        return "Couldn't find that on Wikipedia!"
    except Exception as e:
        print(f"Wikipedia error: {e}")
        return search_web_info(query)


def search_web_info(query):
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        response = urllib.request.urlopen(req)
        html = response.read().decode()
        soup = BeautifulSoup(html, "html.parser")

        # Try to get featured snippet
        snippets = soup.find_all("div", class_="BNeawe")
        for snippet in snippets[:3]:
            text = snippet.get_text()
            if len(text) > 50:
                return f"Here's what I found: {text[:300]}"

        return "Couldn't find a direct answer, try searching Google!"
    except Exception as e:
        print(f"Web scrape error: {e}")
        return "Couldn't fetch that info right now!"


def get_weather_detailed(city):
    try:
        url = f"https://wttr.in/{city}?format=3"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        response = urllib.request.urlopen(req)
        return response.read().decode()
    except Exception as e:
        return f"Weather error: {e}"