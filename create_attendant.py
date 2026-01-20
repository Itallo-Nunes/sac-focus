import argparse
from getpass import getpass
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def create_attendant():
    """
    Script de linha de comando para criar um usuário com a função de Atendente.
    """
    app = create_app()
    with app.app_context():
        print("--- Criação de Novo Atendente ---")
        
        # Solicita o email
        while True:
            email = input("Digite o email do novo atendente: ").strip()
            if not email:
                print("O email não pode ser vazio.")
                continue
            
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                print(f"Erro: O email '{email}' já está cadastrado. Tente outro.")
                continue
            break

        # Solicita a senha
        while True:
            password = getpass("Digite a senha (mínimo 6 caracteres): ")
            if len(password) < 6:
                print("A senha deve ter pelo menos 6 caracteres.")
                continue
            
            confirm_password = getpass("Confirme a senha: ")
            if password != confirm_password:
                print("As senhas não correspondem. Tente novamente.")
                continue
            break

        # Cria o novo usuário com a função 'Atendente'
        try:
            new_attendant = User(
                email=email,
                password=generate_password_hash(password, method='pbkdf2:sha256'),
                role='Atendente' # Define a função diretamente
            )
            
            db.session.add(new_attendant)
            db.session.commit()
            
            print(f"\n\033[92mSucesso! O atendente '{email}' foi criado.\033[0m")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n\033[91mErro ao criar o usuário: {e}\033[0m")

if __name__ == '__main__':
    create_attendant()
