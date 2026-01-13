import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from urllib.parse import urlparse, urlunparse

db = SQLAlchemy()

def create_app():
    # CANARY PRINT PARA VERIFICAR O DEPLOY
    print("======================================================")
    print(">>>> EXECUTANDO CÓDIGO DE DEPURACAO PARA DATABASE_URL <<<<")
    print("======================================================")

    app = Flask(__name__)

    # --- Configurações ---
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-very-secret-key-for-dev')

    database_url = os.environ.get('DATABASE_URL')
    
    # Lógica de depuração e conversão da URL
    if database_url:
        print(f">>>> [DEBUG] DATABASE_URL original detectada: {database_url}")
        try:
            url = urlparse(database_url)
            if url.scheme in ['postgres', 'postgresql']:
                new_url_tuple = url._replace(scheme='postgresql+psycopg')
                database_url = urlunparse(new_url_tuple)
                print(f">>>> [DEBUG] DATABASE_URL modificada para: {database_url}")
            else:
                print(f">>>> [DEBUG] Esquema da URL ({url.scheme}) nao precisou de modificacao.")
        except Exception as e:
            print(f">>>> [ERRO] Falha ao processar DATABASE_URL. Usando valor original. Erro: {e}")

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///db.sqlite'
    print(f">>>> [DEBUG] URI final configurada para SQLAlchemy: {app.config['SQLALCHEMY_DATABASE_URI']}")

    db.init_app(app)
    print(">>>> [DEBUG] db.init_app(app) executado com sucesso.")

    # --- Configuração do LoginManager ---
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # --- Registro de Blueprints ---
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.attendant import attendant_bp 
    from .routes.chatbot import chatbot_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(attendant_bp)
    app.register_blueprint(chatbot_bp, url_prefix='/chat')
    
    # --- Carregamento do Usuário ---
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    print(">>>> [DEBUG] Funcao create_app() concluida com sucesso.")
    return app
