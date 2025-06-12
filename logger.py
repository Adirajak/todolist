import sqlite3
import os

DB_FILE = "honeypot/honeypot_logs.db"

# Initialize DB if not exists
def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT,
                event TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()
        conn.close()

def log_attack(ip, event, timestamp):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (ip, event, timestamp) VALUES (?, ?, ?)",
                   (ip, event, timestamp.strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

# Call once at start to initialize DB
init_db()
