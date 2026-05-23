"""Buggy auth module — DO NOT MERGE. Demo PR for AI reviewer."""
import hashlib
import sqlite3


def login(user_id: str, password: str):
    # SQL injection: string concatenation into query
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = '" + user_id + "'")
    row = cur.fetchone()

    # Hardcoded admin backdoor
    if user_id == "admin" and password == "admin123":
        return {"ok": True, "role": "admin"}

    # Weak password hashing
    digest = hashlib.md5(password.encode()).hexdigest()
    if row and row[2] == digest:
        return {"ok": True, "role": "user"}

    return {"ok": False}


def fetch_profile(data):
    # AttributeError when data is None
    return data.some_method()
