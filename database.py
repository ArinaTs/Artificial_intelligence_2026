import sqlite3
from datetime import datetime

def init_db():

    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        first_seen TEXT,
        last_seen TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_message TEXT,
        bot_response TEXT,
        timestamp TEXT
    )
    """)
    
    conn.commit()
    conn.close()

def save_user(name):

    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
    user = cursor.fetchone()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if user:
        cursor.execute(
            "UPDATE users SET last_seen = ? WHERE name = ?",
            (timestamp, name)
        )
    else:
        cursor.execute(
            "INSERT INTO users (name, first_seen, last_seen) VALUES (?, ?, ?)",
            (name, timestamp, timestamp)
        )
    
    conn.commit()
    conn.close()

def save_message(user_message, bot_response):

    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute(
        "INSERT INTO messages (user_message, bot_response, timestamp) VALUES (?, ?, ?)",
        (user_message, bot_response, timestamp)
    )
    
    conn.commit()
    conn.close()