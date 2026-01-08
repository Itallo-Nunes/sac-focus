from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Secret key for session management
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_default_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    # Set the login view so Flask-Login knows where to redirect anonymous users
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        # Import the User model here to avoid circular imports
        from .models import User
        return User.query.get(int(user_id))

    # Import and Register Blueprints within the app context to avoid circular imports
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.tickets import tickets_bp
    from .routes.chatbot import chatbot_bp
    from .routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(tickets_bp, url_prefix='/tickets')
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
