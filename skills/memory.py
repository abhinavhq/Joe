import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'vivi_memory.db')

def init_memory():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memories
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  category TEXT,
                  key TEXT,
                  value TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS conversations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  role TEXT,
                  message TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def save_memory(category, key, value):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM memories WHERE category=? AND key=?", (category, key))
    c.execute("INSERT INTO memories (category, key, value) VALUES (?,?,?)", (category, key, value))
    conn.commit()
    conn.close()

def get_memory(category, key):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT value FROM memories WHERE category=? AND key=?", (category, key))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_all_memories():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT category, key, value FROM memories ORDER BY timestamp DESC LIMIT 20")
    results = c.fetchall()
    conn.close()
    return results

def save_conversation(role, message):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO conversations (role, message) VALUES (?,?)", (role, message))
    conn.commit()
    conn.close()

def get_recent_conversations(limit=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role, message FROM conversations ORDER BY timestamp DESC LIMIT ?", (limit,))
    results = c.fetchall()
    conn.close()
    return list(reversed(results))