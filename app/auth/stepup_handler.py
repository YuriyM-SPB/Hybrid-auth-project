from werkzeug.security import check_password_hash

# Handle step-up authentication

def require_stepup(user, password):
    return check_password_hash(user.password_hash, password)
