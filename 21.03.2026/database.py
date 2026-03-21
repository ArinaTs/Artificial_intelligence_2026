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

def get_or_create_user(name):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    
    # Ищем пользователя
    cursor.execute("SELECT user_id FROM users WHERE name = ?", (name,))
    user = cursor.fetchone()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if user:
        user_id = user[0]
        # Обновляем last_seen
        cursor.execute(
            "UPDATE users SET last_seen = ? WHERE user_id = ?",
            (timestamp, user_id)
        )
    else:
        # Создаем нового
        cursor.execute(
            "INSERT INTO users (name, first_seen, last_seen) VALUES (?, ?, ?)",
            (name, timestamp, timestamp)
        )
        user_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    return user_id

def is_new_user(name):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT first_seen, last_seen FROM users WHERE name = ?", (name,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return user[0] == user[1]
    return True

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