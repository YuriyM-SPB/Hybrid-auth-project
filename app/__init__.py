from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize database
db = SQLAlchemy()

# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = 'login'  # Redirect to login if not authenticated

# App factory
def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import user  # Import models after db.init_app()

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app