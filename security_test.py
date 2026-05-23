def login(username, password):
    # SQL injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    return execute_sql(query)

def payment():
    # Hardcoded credit card
    cc_number = "4532-1234-5678-9010"
    return process_payment(cc_number)

def api_call():
    # No error handling
    data = requests.get("https://api.example.com/data")
    return parse(data)
