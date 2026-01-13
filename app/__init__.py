import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # --- Configurações de Produção (Render) e Desenvolvimento ---
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-very-secret-key-for-dev')

    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///db.sqlite'

    db.init_app(app)

    # --- Configuração do LoginManager ---
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # --- Registro de Blueprints (CORRIGIDO) ---
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    # CORREÇÃO: Importa o blueprint correto do arquivo correto.
    from .routes.attendant import attendant_bp 
    from .routes.chatbot import chatbot_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    # CORREÇÃO: Registra o blueprint do atendente.
    app.register_blueprint(attendant_bp)
    app.register_blueprint(chatbot_bp, url_prefix='/chat')
    
    # --- Carregamento do Usuário ---
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
