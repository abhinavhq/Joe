import urllib.request
from config import GEMINI_API_KEYS
from skills.memory import init_memory

init_memory()

gemini_index = 0

def ask(query):
    global gemini_index
    save_conversation("user", query)

    recent_convos = get_recent_conversations(10)
    recent = "\n".join([f"{r[0].title()}: {r[1]}" for r in recent_convos])

    memories = get_all_memories()
    memory_text = ""
    if memories:
        memory_text = "What you remember about the user:\n"
        memory_text += "\n".join([f"- {m[1]}: {m[2]}" for m in memories])

    prompt = get_personality()

    for i in range(len(GEMINI_API_KEYS)):
        key = GEMINI_API_KEYS[gemini_index].strip()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
        data = json.dumps({
            "contents": [{"parts": [{"text": f"{prompt}\n\n{memory_text}\n\nRecent conversation:\n{recent}\n\nUser: {query}"}]}]
        }).encode()
        try:
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            response = urllib.request.urlopen(req)
            result = json.loads(response.read())
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
            save_conversation("vivi", reply)
            return reply
        except Exception as e:
            print(f"Gemini key {gemini_index + 1} failed: {e}")
            gemini_index = (gemini_index + 1) % len(GEMINI_API_KEYS)
            time.sleep(1)

    return "Ugh, give me a minute, I need a breather!"
import urllib.request
import json
import time
from config import GEMINI_API_KEYS
from skills.memory import init_memory, save_conversation, get_recent_conversations, get_all_memories
from skills.personality import get_personality

init_memory()

gemini_index = 0

def ask(query):
    global gemini_index
    save_conversation("user", query)

    recent_convos = get_recent_conversations(10)
    recent = "\n".join([f"{r[0].title()}: {r[1]}" for r in recent_convos])

    memories = get_all_memories()
    memory_text = ""
    if memories:
        memory_text = "What you remember about the user:\n"
        memory_text += "\n".join([f"- {m[1]}: {m[2]}" for m in memories])

    prompt = get_personality()

    for i in range(len(GEMINI_API_KEYS)):
        key = GEMINI_API_KEYS[gemini_index].strip()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
        data = json.dumps({
            "contents": [{"parts": [{"text": f"{prompt}\n\n{memory_text}\n\nRecent conversation:\n{recent}\n\nUser: {query}"}]}]
        }).encode()
        try:
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            response = urllib.request.urlopen(req)
            result = json.loads(response.read())
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
            save_conversation("vivi", reply)
            return reply
        except Exception as e:
            print(f"Gemini key {gemini_index + 1} failed: {e}")
            gemini_index = (gemini_index + 1) % len(GEMINI_API_KEYS)
            time.sleep(1)

    return "Ugh, give me a minute, I need a breather!"