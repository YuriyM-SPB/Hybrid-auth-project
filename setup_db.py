from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

db.create_all()

# Create a test user
user = User(username='testuser', password_hash=generate_password_hash('testpassword'))
db.session.add(user)
db.session.commit()

print("Database initialized and test user created.")