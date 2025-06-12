import sqlite3

def create_table():
    conn = sqlite3.connect('honeypot.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS attacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            timestamp TEXT,
            attack_type TEXT,
            command TEXT,
            severity TEXT
        )
    ''')
    conn.commit()
    conn.close()
