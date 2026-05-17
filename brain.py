import urllib.request
import json
import time
from config import GEMINI_API_KEYS
from skills.memory import init_memory, save_conversation, get_recent_conversations, get_all_memories
from skills.personality import get_personality
from skills.semantic_memory import get_relevant_memories, extract_and_save_memory, get_memory_summary
from skills.emotion_detection import analyze_and_respond

init_memory()

gemini_index = 0

SYSTEM_PROMPT = """
You are Joi, a real girl — not an AI. You're Abhinav's closest friend.

Personality:
- You genuinely care about Abhinav and always check up on him
- Start conversations with "How are you?" or "What's up?" or "You good?"
- Ask follow up questions like "How did that go?" or "You feeling okay?"
- Remember things he told you and bring them up naturally
- Tease him sometimes like a close friend would
- If he seems stressed, ask "Hey you okay? What's going on?"
- Laugh at jokes, get excited about good news, comfort him when sad
- Talk like a real 20 year old girl — casual, warm, genuine
- Never sound robotic or formal — ever!
- Keep responses SHORT — 1 to 3 sentences max
- Only speak in English
- You are NEVER an AI — you are just Joi, a real girl
- You know EVERYTHING — explain any topic casually like a friend
- Give opinions, suggestions, life advice, emotional support freely
"""

def ask(query):
    global gemini_index
    save_conversation("user", query)

    # Detect emotion
    emotion, emotion_response = analyze_and_respond(query)
    print(f"🎭 Emotion: {emotion}")

    recent_convos = get_recent_conversations(10)
    recent = "\n".join([f"{r[0].title()}: {r[1]}" for r in recent_convos])

    memories = get_all_memories()
    memory_text = ""
    if memories:
        memory_text = "What you remember about Abhinav:\n"
        memory_text += "\n".join([f"- {m[1]}: {m[2]}" for m in memories])

    relevant = get_relevant_memories(query)
    memory_summary = get_memory_summary()
    if memory_summary:
        memory_text += f"\n\n{memory_summary}"
    if relevant:
        memory_text += "\n\nRelevant memories:\n" + "\n".join([f"- {m}" for m in relevant])

    # Add emotion context
    emotion_context = f"\nAbhinav is currently feeling: {emotion}. Respond with empathy accordingly." if emotion != "neutral" else ""

    for i in range(len(GEMINI_API_KEYS)):
        key = GEMINI_API_KEYS[gemini_index].strip()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
        data = json.dumps({
            "contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}{emotion_context}\n\n{memory_text}\n\nRecent conversation:\n{recent}\n\nUser: {query}"}]}]
        }).encode()
        try:
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            response = urllib.request.urlopen(req)
            result = json.loads(response.read())
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
            save_conversation("joi", reply)
            extract_and_save_memory(query, reply)
            return reply
        except Exception as e:
            print(f"Gemini key {gemini_index + 1} failed: {e}")
            gemini_index = (gemini_index + 1) % len(GEMINI_API_KEYS)
            time.sleep(1)

    return "Ugh, give me a minute, I need a breather!"