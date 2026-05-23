def new_security_vulnerability():
    # SQL injection vulnerability
    user_input = request.args.get('user')
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    execute(query)
    
    # Hardcoded API key
    api_key = "sk_live_1234567890abcdef"
    
    return {"success": True}
