import webbrowser
import urllib.request

last_results = []

def play_music(query, result_number=1):
    global last_results

    song = query.replace("play", "").replace("music", "").replace("song", "").replace("video", "").replace("on spotify", "").replace("on youtube", "").strip()

    if any(w in query for w in ["first", "1st", "one"]):
        result_number = 1
    elif any(w in query for w in ["second", "2nd", "two"]):
        result_number = 2
    elif any(w in query for w in ["third", "3rd", "three"]):
        result_number = 3
    elif any(w in query for w in ["fourth", "4th", "four"]):
        result_number = 4

    if not song:
        song = "top hits"

    if "spotify" in query:
        webbrowser.open(f"spotify:search:{song}")
        return f"Playing {song} on Spotify!"

    try:
        search = song.replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={search}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        response = urllib.request.urlopen(req)
        html = response.read().decode()

        last_results = []
        pos = 0
        for _ in range(5):
            start = html.find('"videoId":"', pos) + 11
            if start == 10:
                break
            video_id = html[start:start+11]
            if video_id not in last_results:
                last_results.append(video_id)
            pos = start + 11

        if last_results:
            idx = min(result_number - 1, len(last_results) - 1)
            webbrowser.open(f"https://www.youtube.com/watch?v={last_results[idx]}")
            return f"Playing result {result_number} for {song} on YouTube!"
        else:
            webbrowser.open(url)
            return f"Searching {song} on YouTube!"
    except Exception as e:
        print(f"Music error: {e}")
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
        return f"Searching {song} on YouTube!"