from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from .routes.main import main_bp
from .routes.auth import auth_bp
from .routes.tickets import tickets_bp
from .routes.chatbot import chatbot_bp
from .routes.admin import admin_bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Secret key for session management
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_default_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(tickets_bp, url_prefix='/tickets')
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
