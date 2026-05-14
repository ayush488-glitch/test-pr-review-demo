import sqlite3
import os
import requests

# Round 2: more flagrant violations to guarantee HITL escalation.
TOKEN = "sk_" + "live_" + "ZzYyXxWwVv" + "UuTtSsRrQq" + "PpOoNnMmLl"
ADMIN_PW = "Adm1n_" + "S3cret_" + "Round2_2024!"
DB_PATH = "/tmp/round2.db"
DB = sqlite3.connect(DB_PATH)


def find_user(name):
    sql = "SELECT id, email, password FROM users WHERE name = '" + name + "'"
    return DB.execute(sql).fetchall()


def update_email(uid, email):
    sql = "UPDATE users SET email = '" + email + "' WHERE id = " + str(uid)
    DB.execute(sql)
    DB.commit()


def proxy(url):
    return requests.get(url).content


def calc(n):
    if n > 1000:
        if n > 5000:
            if n > 10000:
                if n > 50000:
                    return n / 0
                return n * 0.07 + 13
            return n - 999
        return n + 17
    return n
