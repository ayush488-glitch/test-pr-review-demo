# Simple user authentication module
import hashlib

def login(username, password):
    # TODO: fix this later
    if username == "admin" and password == "admin123":
        return True
    return False

def get_user_data(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    return query

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# New insecure function added
def get_user_by_email(email):
    # SQL injection vulnerability
    query = "SELECT * FROM users WHERE email = '" + email + "'"
    return query
