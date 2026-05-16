import json
import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'joi_semantic.db')


def init_semantic_memory():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS semantic_memories
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  memory TEXT,
                  category TEXT,
                  importance INTEGER DEFAULT 1,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                  access_count INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()


def save_semantic_memory(memory, category="general", importance=1):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Check if similar memory exists
    c.execute("SELECT id, memory FROM semantic_memories WHERE category=?", (category,))
    existing = c.fetchall()

    for row in existing:
        if similar(row[1], memory):
            # Update existing
            c.execute("UPDATE semantic_memories SET access_count = access_count + 1 WHERE id=?", (row[0],))
            conn.commit()
            conn.close()
            return

    c.execute("INSERT INTO semantic_memories (memory, category, importance) VALUES (?,?,?)",
              (memory, category, importance))
    conn.commit()
    conn.close()


def similar(text1, text2, threshold=0.8):
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    if not words1 or not words2:
        return False
    intersection = words1.intersection(words2)
    return len(intersection) / max(len(words1), len(words2)) > threshold


def get_relevant_memories(query, limit=5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""SELECT memory, category, importance 
                 FROM semantic_memories 
                 ORDER BY importance DESC, access_count DESC 
                 LIMIT ?""", (limit,))
    results = c.fetchall()
    conn.close()

    # Filter relevant ones
    relevant = []
    query_words = set(query.lower().split())
    for row in results:
        memory_words = set(row[0].lower().split())
        if query_words.intersection(memory_words):
            relevant.append(row[0])

    return relevant if relevant else [r[0] for r in results[:3]]


def extract_and_save_memory(query, response):
    query_lower = query.lower()

    # Extract important info from conversation
    if any(w in query_lower for w in ["my name is", "i am", "i'm"]):
        save_semantic_memory(f"User said: {query}", "identity", importance=5)

    elif any(w in query_lower for w in ["i like", "i love", "i enjoy", "favorite"]):
        save_semantic_memory(f"User preference: {query}", "preferences", importance=4)

    elif any(w in query_lower for w in ["i hate", "i don't like", "i dislike"]):
        save_semantic_memory(f"User dislikes: {query}", "preferences", importance=4)

    elif any(w in query_lower for w in ["i work", "i study", "i go to", "i live"]):
        save_semantic_memory(f"User lifestyle: {query}", "lifestyle", importance=4)

    elif any(w in query_lower for w in ["i feel", "i'm feeling", "i am feeling"]):
        save_semantic_memory(f"User emotion: {query}", "emotions", importance=3)

    elif any(w in query_lower for w in ["yesterday", "last week", "today i"]):
        save_semantic_memory(f"User event: {query}", "events", importance=3)

    else:
        save_semantic_memory(f"Conversation: {query}", "general", importance=1)


def get_memory_summary():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""SELECT memory FROM semantic_memories 
                 WHERE importance >= 3 
                 ORDER BY importance DESC, access_count DESC 
                 LIMIT 10""")
    results = c.fetchall()
    conn.close()

    if results:
        return "Important things I remember:\n" + "\n".join([f"- {r[0]}" for r in results])
    return ""


init_semantic_memory()