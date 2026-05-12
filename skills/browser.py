from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = None

def get_driver():
    global driver
    if driver is None:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
    return driver

def google_search(query):
    try:
        d = get_driver()
        d.get("https://www.google.com")
        search = d.find_element(By.NAME, "q")
        search.send_keys(query)
        search.send_keys(Keys.RETURN)
        time.sleep(2)
        return f"Searched Google for {query}!"
    except Exception as e:
        return f"Browser error: {e}"

def open_website(url):
    try:
        d = get_driver()
        if not url.startswith("http"):
            url = "https://" + url
        d.get(url)
        return f"Opened {url}!"
    except Exception as e:
        return f"Browser error: {e}"

def youtube_search_play(song):
    try:
        d = get_driver()
        d.get(f"https://www.youtube.com/results?search_query={song}")
        time.sleep(2)
        # Click first video
        video = d.find_element(By.CSS_SELECTOR, "ytd-video-renderer a#thumbnail")
        video.click()
        return f"Playing {song} on YouTube!"
    except Exception as e:
        return f"Browser error: {e}"

def scroll_down():
    try:
        d = get_driver()
        d.execute_script("window.scrollBy(0, 500)")
        return "Scrolled down!"
    except Exception as e:
        return f"Browser error: {e}"

def scroll_up():
    try:
        d = get_driver()
        d.execute_script("window.scrollBy(0, -500)")
        return "Scrolled up!"
    except Exception as e:
        return f"Browser error: {e}"

def close_browser():
    global driver
    try:
        if driver:
            driver.quit()
            driver = None
        return "Browser closed!"
    except Exception as e:
        return f"Browser error: {e}"

def go_back():
    try:
        d = get_driver()
        d.back()
        return "Went back!"
    except Exception as e:
        return f"Browser error: {e}"