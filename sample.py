def calculate_total(items):
    total = 0
    for item in items:
        total = total + item.price
    return total

def get_user_email(user_id):
    query = f"SELECT email FROM users WHERE id = {user_id}"
    return query
