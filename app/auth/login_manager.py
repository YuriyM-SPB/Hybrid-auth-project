from app.models.user import User
from werkzeug.security import check_password_hash

# Verify credentials

def verify_credentials(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None