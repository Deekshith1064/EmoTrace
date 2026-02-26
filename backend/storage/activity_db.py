import sqlite3

# Create / connect to database
conn = sqlite3.connect("activity_logs.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    duration INTEGER,
    timestamp TEXT
)
""")

conn.commit()

# Create emotion logs table
cursor.execute("""
CREATE TABLE IF NOT EXISTS emotion_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emotion TEXT,
    score REAL,
    timestamp TEXT
)
""")

conn.commit()


def insert_log(url, duration, timestamp):
    cursor.execute(
        "INSERT INTO activity_logs (url, duration, timestamp) VALUES (?, ?, ?)",
        (url, duration, timestamp)
    )
    conn.commit()

def fetch_all_logs():
    cursor.execute("SELECT * FROM activity_logs")
    return cursor.fetchall()

def fetch_all_emotions():
    cursor.execute("SELECT * FROM emotion_logs")
    return cursor.fetchall()

def get_all_logs():
    conn = sqlite3.connect("activity_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT url, duration, timestamp FROM activity_logs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    return [
        {"url": row[0], "duration": row[1], "timestamp": row[2]}
        for row in rows
    ]

def insert_emotion(emotion, score, timestamp):
    cursor.execute(
        "INSERT INTO emotion_logs (emotion, score, timestamp) VALUES (?, ?, ?)",
        (emotion, score, timestamp)
    )
    conn.commit()


if __name__ == "__main__":
    print("Database ready.")
