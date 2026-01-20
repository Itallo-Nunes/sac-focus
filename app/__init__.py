
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from urllib.parse import urlparse, urlunparse

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # --- Configurações de Produção (Render) e Desenvolvimento ---
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-very-secret-key-for-dev')

    database_url = os.environ.get('DATABASE_URL')
    
    # Solução robusta para a URL do Banco de Dados em Produção
    if database_url:
        try:
            url = urlparse(database_url)
            # Se o esquema for 'postgres' ou 'postgresql', troca pelo dialeto correto.
            if url.scheme in ['postgres', 'postgresql']:
                new_url_tuple = url._replace(scheme='postgresql+psycopg')
                database_url = urlunparse(new_url_tuple)
        except Exception as e:
            # Em caso de erro, apenas loga um aviso e continua com a URL original
            print(f"Aviso: Falha ao processar DATABASE_URL. Usando valor original. Erro: {e}")

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///db.sqlite'

    db.init_app(app)

    # --- Configuração do LoginManager ---
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # --- Registro de Blueprints ---
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.attendant import attendant_bp 
    from .routes.chatbot import chatbot_bp
    from .routes.tickets import tickets_bp # <<< ADICIONADO

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(attendant_bp)
    app.register_blueprint(chatbot_bp, url_prefix='/chat')
    app.register_blueprint(tickets_bp, url_prefix='/tickets') # <<< ADICIONADO
    
    # --- Carregamento do Usuário ---
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

