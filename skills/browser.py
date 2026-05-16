from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = None

def get_driver():
    global driver
    if driver is None:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
    return driver

def open_website(url):
    try:
        d = get_driver()
        if not url.startswith("http"):
            url = "https://" + url
        d.get(url)
        return f"Opened {url}!"
    except Exception as e:
        return f"Browser error: {e}"

def google_search(query):
    try:
        d = get_driver()
        d.get(f"https://www.google.com/search?q={query}")
        return f"Searched for {query}!"
    except Exception as e:
        return f"Browser error: {e}"

def youtube_search_play(song):
    try:
        d = get_driver()
        d.get(f"https://www.youtube.com/results?search_query={song}")
        time.sleep(2)
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
        return f"Error: {e}"

def scroll_up():
    try:
        d = get_driver()
        d.execute_script("window.scrollBy(0, -500)")
        return "Scrolled up!"
    except Exception as e:
        return f"Error: {e}"

def scroll_to_top():
    try:
        d = get_driver()
        d.execute_script("window.scrollTo(0, 0)")
        return "Scrolled to top!"
    except Exception as e:
        return f"Error: {e}"

def scroll_to_bottom():
    try:
        d = get_driver()
        d.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        return "Scrolled to bottom!"
    except Exception as e:
        return f"Error: {e}"

def go_back():
    try:
        d = get_driver()
        d.back()
        return "Went back!"
    except Exception as e:
        return f"Error: {e}"

def go_forward():
    try:
        d = get_driver()
        d.forward()
        return "Went forward!"
    except Exception as e:
        return f"Error: {e}"

def refresh_page():
    try:
        d = get_driver()
        d.refresh()
        return "Page refreshed!"
    except Exception as e:
        return f"Error: {e}"

def new_tab(url="https://www.google.com"):
    try:
        d = get_driver()
        d.execute_script(f"window.open('{url}', '_blank')")
        d.switch_to.window(d.window_handles[-1])
        return "Opened new tab!"
    except Exception as e:
        return f"Error: {e}"

def close_tab():
    try:
        d = get_driver()
        d.close()
        if d.window_handles:
            d.switch_to.window(d.window_handles[-1])
        return "Tab closed!"
    except Exception as e:
        return f"Error: {e}"

def next_tab():
    try:
        d = get_driver()
        handles = d.window_handles
        current = handles.index(d.current_window_handle)
        next_idx = (current + 1) % len(handles)
        d.switch_to.window(handles[next_idx])
        return "Switched to next tab!"
    except Exception as e:
        return f"Error: {e}"

def zoom_in():
    try:
        d = get_driver()
        d.execute_script("document.body.style.zoom='125%'")
        return "Zoomed in!"
    except Exception as e:
        return f"Error: {e}"

def zoom_out():
    try:
        d = get_driver()
        d.execute_script("document.body.style.zoom='75%'")
        return "Zoomed out!"
    except Exception as e:
        return f"Error: {e}"

def zoom_reset():
    try:
        d = get_driver()
        d.execute_script("document.body.style.zoom='100%'")
        return "Zoom reset!"
    except Exception as e:
        return f"Error: {e}"

def find_on_page(text):
    try:
        d = get_driver()
        element = d.find_element(By.XPATH, f"//*[contains(text(), '{text}')]")
        d.execute_script("arguments[0].scrollIntoView();", element)
        return f"Found '{text}' on page!"
    except Exception as e:
        return f"Couldn't find '{text}' on page!"

def get_page_title():
    try:
        d = get_driver()
        return f"Current page: {d.title}"
    except Exception as e:
        return f"Error: {e}"

def type_in_browser(text):
    try:
        d = get_driver()
        active = d.switch_to.active_element
        active.send_keys(text)
        return f"Typed: {text}"
    except Exception as e:
        return f"Error: {e}"

def close_browser():
    global driver
    try:
        if driver:
            driver.quit()
            driver = None
        return "Browser closed!"
    except Exception as e:
        return f"Error: {e}"