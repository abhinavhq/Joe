import urllib.request


def get_news():
    try:
        url = "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-IN&gl=IN&ceid=IN:en"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        response = urllib.request.urlopen(req)
        content = response.read().decode()

        titles = []
        pos = 0
        for _ in range(10):
            start = content.find("<title>", pos) + 7
            end = content.find("</title>", start)
            if start == 6 or end == -1:
                break
            title = content[start:end].strip()
            if title and "Google News" not in title:
                titles.append(title)
            pos = end

        if titles:
            result = "Here are today's top headlines! "
            for i, t in enumerate(titles[:3], 1):
                result += f"Number {i}: {t}. "
            return result
        return "Couldn't fetch news right now!"
    except Exception as e:
        print(f"News error: {e}")
        return "Couldn't fetch news right now!"