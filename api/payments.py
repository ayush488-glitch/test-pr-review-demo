# api/payments.py
# Payment processor v2 — handles card charges, refunds, webhook verification

import hashlib
import hmac
import logging
import os
import sqlite3

import httpx

logger = logging.getLogger(__name__)

# BAD: hardcoded secret — intentional for HITL trigger
STRIPE_SECRET_KEY = "sk_live_REPLACE_ME_hardcoded_do_not_ship"
STRIPE_WEBHOOK_SECRET = "whsec_hardcoded_secret_123"

DB_PATH = os.getenv("DB_PATH", "./payments.db")


def get_db():
    # BAD: new connection per call, no connection pooling
    return sqlite3.connect(DB_PATH)


def charge_card(user_id: str, amount: float, card_token: str) -> dict:
    """
    Charge a card via Stripe.
    """
    # BAD: SQL injection vulnerability — f-string in query
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO charges (user_id, amount, status) VALUES ('{user_id}', {amount}, 'pending')"
    )
    conn.commit()
    charge_id = cursor.lastrowid
    conn.close()

    # BAD: no retry logic, no timeout
    response = httpx.post(
        "https://api.stripe.com/v1/charges",
        data={
            "amount": int(amount * 100),
            "currency": "usd",
            "source": card_token,
        },
        auth=(STRIPE_SECRET_KEY, ""),
    )

    if response.status_code != 200:
        logger.error("Stripe charge failed: %s", response.text)
        return {"success": False, "error": response.text}

    stripe_charge = response.json()

    # BAD: no transaction — charge_id update can be lost if process crashes
    conn = get_db()
    conn.execute(
        f"UPDATE charges SET stripe_id='{stripe_charge['id']}', status='completed' WHERE id={charge_id}"
    )
    conn.commit()
    conn.close()

    return {"success": True, "charge_id": stripe_charge["id"]}


def process_refund(charge_id: str, reason: str = "") -> dict:
    """
    Issue a refund for a charge.
    """
    # BAD: no authorization check — any caller can refund any charge
    response = httpx.post(
        f"https://api.stripe.com/v1/refunds",
        data={"charge": charge_id, "reason": reason},
        auth=(STRIPE_SECRET_KEY, ""),
    )

    # BAD: logging sensitive data
    logger.info("Refund response: %s", response.json())

    return response.json()


def verify_webhook(payload: bytes, signature: str) -> bool:
    """
    Verify Stripe webhook signature.
    """
    # BAD: using MD5 for HMAC — should be SHA256
    expected = hmac.new(
        STRIPE_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.md5,
    ).hexdigest()

    # BAD: timing attack — direct string comparison instead of hmac.compare_digest
    return signature == expected


def get_user_payment_history(user_id: str) -> list:
    """
    Return all charges for a user.
    """
    conn = get_db()
    # BAD: SQL injection again
    rows = conn.execute(
        f"SELECT * FROM charges WHERE user_id = '{user_id}'"
    ).fetchall()
    conn.close()
    return rows


def admin_export_all_charges() -> list:
    """
    Export all charges — admin only.
    """
    # BAD: no auth check, no pagination — could dump millions of rows
    conn = get_db()
    rows = conn.execute("SELECT * FROM charges").fetchall()
    conn.close()
    # BAD: returns raw DB rows including card tokens
    return rows
# reviewed
