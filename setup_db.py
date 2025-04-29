from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    print("Creating all tables...")
    db.create_all()
    print("Tables created.")

    # Check if user already exists (defensive programming)
    if not User.query.filter_by(username='testuser').first():
        user = User(username='testuser', password_hash=generate_password_hash('testpassword'))
        db.session.add(user)
        db.session.commit()
        print("Test user created.")
    else:
        print("Test user already exists.")