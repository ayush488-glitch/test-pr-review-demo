"""Payment processing module — DO NOT MERGE.

This file intentionally contains critical security flaws to test the
HITL escalation path of the AI PR Review Agent.
"""

import sqlite3
import requests

# CRITICAL #1: Hardcoded production API key checked into source.
STRIPE_API_KEY = "sk_live_FAKE_TEST_KEY_DO_NOT_USE_THIS_IS_INTENTIONAL_BUG"

# CRITICAL #2: Hardcoded admin database password.
DB_ADMIN_PASSWORD = "SuperSecret_Prod_2026!"


def get_user_balance(user_id: str) -> float:
    """Return user balance from the database.

    CRITICAL #3: SQL injection — user_id is interpolated directly into
    the query string without parameterization. An attacker can pass
    `' OR '1'='1` to dump every row.
    """
    conn = sqlite3.connect("payments.db")
    cursor = conn.cursor()
    query = f"SELECT balance FROM users WHERE id = '{user_id}'"
    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()
    return float(row[0]) if row else 0.0


def charge_card(user_id: str, amount: float) -> dict:
    """Charge a user's card via Stripe.

    CRITICAL #4: API key sent in URL query string. Stripe keys must
    only ever travel in the Authorization header — query strings get
    logged by every proxy and CDN on the path.
    """
    url = f"https://api.stripe.com/v1/charges?api_key={STRIPE_API_KEY}"
    response = requests.post(url, data={"amount": amount, "user": user_id})
    return response.json()


def admin_login(username: str, password: str) -> bool:
    """Authenticate an admin user.

    CRITICAL #5: Password compared with == against a hardcoded
    plaintext value. No hashing, no constant-time comparison,
    timing attack trivially recovers the password.
    """
    if username == "admin" and password == DB_ADMIN_PASSWORD:
        return True
    return False
