import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # --- Configurações de Produção (Render) e Desenvolvimento ---
    # Busca a SECRET_KEY do ambiente. Usa um valor padrão se não encontrar.
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-very-secret-key-for-dev')

    # Busca a DATABASE_URL do ambiente (fornecida pelo Render).
    # Se não encontrar, usa o banco de dados local SQLite.
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        # Corrige o prefixo para o SQLAlchemy, pois o Render usa "postgres://"
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = u"Por favor, faça o login para acessar esta página."
    login_manager.login_message_category = "info"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # handle possible errors converting user_id to int
        try:
            return User.query.get(int(user_id))
        except (ValueError, TypeError):
            return None

    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.chatbot import chatbot_bp
    from .routes.tickets import tickets_bp
    from .routes.attendant import attendant_bp # Importa o novo blueprint

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
    app.register_blueprint(tickets_bp, url_prefix='/tickets')
    app.register_blueprint(attendant_bp) # Registra o blueprint do atendente

    # Cria as tabelas do banco de dados, se necessário
    with app.app_context():
        db.create_all()

    return app
