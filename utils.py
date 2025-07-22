import sqlite3
from datetime import datetime

def get_user(username, password):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return cur.fetchone()

def get_qr_data(code):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM qr_pages WHERE code=?", (code,))
    return cur.fetchone()

def log_access(username, code,timestamp=None):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("INSERT INTO access_logs (username, Loc, timestamp) VALUES (?, ?, ?)",
                (username, code, timestamp))
    con.commit()
    con.close()

def create_feedback(username,rating_event,rating_portal,comments):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute("""
        INSERT INTO feedback (username, rating_event, rating_portal, comments)
        VALUES (?, ?, ?, ?, ?)
    """, (username, rating_event, rating_portal, comments))
    con.commit()
    con.close()

def get_feedbacks():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute("SELECT username, rating_event, rating_portal, comments FROM feedback")
    feedbacks = cur.fetchall()
    con.close()
    return feedbacks

def get_access_logs():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute("SELECT username, Loc, timestamp FROM access_logs ORDER BY timestamp DESC")
    logs = cur.fetchall()
    con.close()
    return logs