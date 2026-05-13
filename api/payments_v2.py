# api/payments_v2.py — Payment processing with charge, refund, admin export

import sqlite3
import logging
import httpx
import os

logger = logging.getLogger(__name__)

STRIPE_KEY = "sk_live_REPLACE_ME_hardcoded_do_not_ship"
DB_PATH = "./payments.db"


def charge_card(user_id, amount, card_number, cvv, expiry):
    conn = sqlite3.connect(DB_PATH)

    # CRITICAL: full raw card number + CVV stored in DB — PCI DSS violation
    conn.execute(
        f"INSERT INTO charges (user_id, amount, card_number, cvv, expiry, status) "
        f"VALUES ('{user_id}', {amount}, '{card_number}', '{cvv}', '{expiry}', 'pending')"
    )
    conn.commit()

    # CRITICAL: raw card number logged to console
    logger.info(f"Charging card {card_number} CVV {cvv} for user {user_id} amount {amount}")

    resp = httpx.post(
        "https://api.stripe.com/v1/charges",
        data={"amount": int(amount * 100), "currency": "usd"},
        auth=(STRIPE_KEY, ""),
    )
    return resp.json()


def get_all_payments():
    # CRITICAL: no authentication — any caller dumps entire payments table including card numbers
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT * FROM charges").fetchall()
    conn.close()
    # CRITICAL: returns raw card numbers to caller
    return rows


def refund(charge_id, reason=""):
    # CRITICAL: no auth check — anyone can refund any charge
    resp = httpx.post(
        f"https://api.stripe.com/v1/refunds",
        data={"charge": charge_id, "reason": reason},
        auth=(STRIPE_KEY, ""),
    )
    # CRITICAL: full response logged including card details
    logger.info("Refund response: %s", resp.json())
    return resp.json()


def search_payments(query: str):
    # CRITICAL: direct SQL injection from user input
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        f"SELECT * FROM charges WHERE user_id LIKE '%{query}%' OR card_number LIKE '%{query}%'"
    ).fetchall()
    conn.close()
    return rows


def process_bulk_payment(user_id: str, payments: list):
    # CRITICAL: eval() on user-controlled data — arbitrary code execution
    total = eval("+".join([str(p["amount"]) for p in payments]))
    return charge_card(user_id, total, payments[0]["card"], payments[0]["cvv"], payments[0]["expiry"])
