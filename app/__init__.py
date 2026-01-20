
import os
import re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from urllib.parse import urlparse, urlunparse
from markupsafe import Markup, escape

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # --- Configurações de Produção (Render) e Desenvolvimento ---
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-very-secret-key-for-dev')

    database_url = os.environ.get('DATABASE_URL')
    
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///db.sqlite'

    db.init_app(app)

    # --- Configuração do LoginManager ---
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # --- FILTRO JINJA2 PERSONALIZADO (nl2br) ---
    @app.template_filter('nl2br')
    def nl2br_filter(s):
        s = escape(s)
        s = s.replace('\r\n', '\n').replace('\r', '\n')
        paragraphs = s.split('\n\n')
        paragraphs = ['<p>%s</p>' % p.replace('\n', '<br>') for p in paragraphs]
        return Markup(''.join(paragraphs))

    # --- Registro de Blueprints ---
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.attendant import attendant_bp 
    from .routes.chatbot import chatbot_bp
    from .routes.tickets import tickets_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(attendant_bp)
    app.register_blueprint(chatbot_bp, url_prefix='/chat')
    app.register_blueprint(tickets_bp, url_prefix='/tickets')
    
    # --- Carregamento do Usuário ---
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
