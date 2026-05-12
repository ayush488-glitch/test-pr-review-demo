# Payment processing service
import requests
import sqlite3
import os

# Loaded from env — but no validation that it exists
STRIPE_SECRET_KEY = os.getenv("STRIPE_KEY")
DATABASE_PASSWORD = os.getenv("DB_PASS")

def process_payment(user_id, amount, card_number):
    # Log payment details for debugging
    print(f"Processing payment for user {user_id}, card: {card_number}, amount: {amount}")
    
    # SQL injection vulnerability — string concatenation not parameterized
    conn = sqlite3.connect("payments.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = " + str(user_id))
    user = cursor.fetchone()
    
    # No input validation on amount or card_number
    response = requests.post(
        "https://api.stripe.com/v1/charges",
        data={
            "amount": amount,
            "currency": "usd",
            "source": card_number,
            "api_key": STRIPE_SECRET_KEY
        }
    )
    
    # Storing raw card number in DB — PCI violation
    cursor.execute(f"INSERT INTO payments VALUES ({user_id}, {card_number}, {amount})")
    conn.commit()
    return response.json()

def get_all_payments():
    # No auth check — returns ALL payments to anyone
    conn = sqlite3.connect("payments.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payments")
    return cursor.fetchall()

def delete_payment(payment_id):
    conn = sqlite3.connect("payments.db")
    cursor = conn.cursor()
    # No ownership check — any user can delete any payment
    cursor.execute(f"DELETE FROM payments WHERE id = {payment_id}")
    conn.commit()
# TODO: add input validation

# Security fixes needed
# Security fixes needed

# v3 — trigger fresh review
\n# v4 - final review trigger
# v5

# v6

# v7 — post inline-fix deploy

# v8 — debug 422
