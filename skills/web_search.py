import webbrowser

def web_search(query):
    query = query.replace("search", "").replace("google", "").strip()
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Searching Google for {query}"