from app import db
from app.models.user import User
from werkzeug.security import check_password_hash
from app import login_manager  # <-- make sure you import this

# Verify credentials
def verify_credentials(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
