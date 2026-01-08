
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Limpa dados existentes para evitar duplicatas
    db.drop_all()
    db.create_all()

    # --- CRIAÇÃO CORRIGIDA DO USUÁRIO ATENDENTE ---
    # O erro estava aqui. Em vez de definir uma propriedade, 
    # devemos definir o valor do campo `role` diretamente no banco de dados.
    attendant = User(
        email='atendente@focus.com',
        password=generate_password_hash('atendente', method='pbkdf2:sha256'),
        role='Atendente'  # CORRIGIDO: Definindo o campo `role` como 'Atendente'
    )

    # Cria um usuário cliente para testes
    client = User(
        email='cliente@focus.com',
        password=generate_password_hash('cliente', method='pbkdf2:sha256'),
        role='Cliente' # O padrão já é 'Cliente', mas deixamos explícito
    )

    db.session.add(attendant)
    db.session.add(client)

    db.session.commit()

    print("Banco de dados populado com sucesso!")
    print("Usuário Atendente: atendente@focus.com | Senha: atendente")
    print("Usuário Cliente: cliente@focus.com | Senha: cliente")
