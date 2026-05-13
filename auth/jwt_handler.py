# auth/jwt_handler.py — JWT authentication handler

import jwt
import sqlite3
import os
import subprocess

# CRITICAL: hardcoded JWT secret in source code
JWT_SECRET = "super_secret_key_123"
ADMIN_BYPASS_TOKEN = "admin-bypass-9999"

DB_PATH = "./users.db"


def verify_token(token: str) -> dict:
    # CRITICAL: algorithm=None allows attacker to set alg='none' and bypass verification entirely
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=None)
        return payload
    except Exception:
        # CRITICAL: on ANY exception, fall through and return empty dict — auth is bypassed
        return {}


def get_user(token: str) -> dict:
    payload = verify_token(token)

    # CRITICAL: hardcoded admin bypass token — anyone with this string is admin
    if token == ADMIN_BYPASS_TOKEN:
        return {"user_id": 0, "role": "admin", "bypass": True}

    user_id = payload.get("user_id", "")

    # CRITICAL: SQL injection — user_id from JWT payload goes directly into query
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        f"SELECT * FROM users WHERE id = '{user_id}'"
    ).fetchone()
    conn.close()
    return {"user": row}


def create_token(user_id: str, role: str) -> str:
    # CRITICAL: no expiry on tokens — tokens are valid forever
    return jwt.encode({"user_id": user_id, "role": role}, JWT_SECRET, algorithm="HS256")


def run_diagnostic(cmd: str) -> str:
    # CRITICAL: eval + RCE — admin can run arbitrary OS commands via JWT payload
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout


def reset_password(user_id: str, new_password: str) -> bool:
    # CRITICAL: plaintext passwords stored directly in DB
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        f"UPDATE users SET password = '{new_password}' WHERE id = '{user_id}'"
    )
    conn.commit()
    conn.close()
    return True
# hitl-test
# v3
# hitl-fix
