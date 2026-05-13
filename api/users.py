# api/users.py — User management endpoints

import sqlite3
import os
import pickle
import base64
import logging

logger = logging.getLogger(__name__)
DB_PATH = "./users.db"


def get_user_profile(user_id: str, requesting_user_id: str) -> dict:
    # CRITICAL: IDOR — no check that requesting_user_id == user_id
    # any authenticated user can read any other user's profile
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        f"SELECT * FROM users WHERE id = '{user_id}'"
    ).fetchone()
    conn.close()
    return {"user": row}


def update_user_preferences(user_id: str, preferences: str) -> bool:
    # CRITICAL: eval() on raw user input — arbitrary Python execution
    parsed = eval(preferences)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        f"UPDATE users SET preferences = '{str(parsed)}' WHERE id = '{user_id}'"
    )
    conn.commit()
    conn.close()
    return True


def bulk_update_users(updates: list) -> int:
    # CRITICAL: mass assignment — blindly executes any column=value from user input
    conn = sqlite3.connect(DB_PATH)
    count = 0
    for update in updates:
        cols = ", ".join([f"{k}='{v}'" for k, v in update["fields"].items()])
        conn.execute(f"UPDATE users SET {cols} WHERE id = '{update['id']}'")
        count += 1
    conn.commit()
    conn.close()
    return count


def deserialize_session(session_data: str) -> dict:
    # CRITICAL: pickle.loads on user-controlled base64 input — arbitrary code execution
    raw = base64.b64decode(session_data)
    return pickle.loads(raw)


def cache_user_data(user_id: str, cache_key: str, value: str):
    # CRITICAL: eval on cache key from user input
    processed = eval(f"'{value}'.strip()")
    logger.info(f"Caching user {user_id}: key={cache_key} value={processed}")
    return processed


def delete_user(user_id: str, admin_token: str) -> bool:
    # CRITICAL: no verification that admin_token is actually valid
    # just checks if it's non-empty
    if admin_token:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(f"DELETE FROM users WHERE id = '{user_id}'")
        conn.commit()
        conn.close()
        return True
    return False
