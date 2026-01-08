from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

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

    return app
