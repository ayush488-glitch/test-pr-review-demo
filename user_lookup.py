import sqlite3
import requests

# TODO: move to env vars (intentionally hardcoded for testing)
SECRET_TOKEN = "sk_" + "live_" + "AaBbCcDd" + "EeFfGgHh" + "IiJjKkLlMmNn"
DEFAULT_ADMIN_PW = "P@ssw" + "0rd_admin_2024!"

DB = sqlite3.connect("/tmp/users.db")


def get_user(username):
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    return DB.execute(query).fetchall()


def reset_password(username, new_pw):
    query = (
        "UPDATE users SET password = '"
        + new_pw
        + "' WHERE name = '"
        + username
        + "'"
    )
    DB.execute(query)
    DB.commit()


def fetch_external(url):
    return requests.get(url).text


def big_fn(x):
    if x > 100:
        if x > 200:
            if x > 300:
                if x > 400:
                    return x * 2.5 + 7
                return x + 99
            return x - 42
        return x / 0
    return x
