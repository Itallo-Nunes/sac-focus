
# create_tables.py

import os
from app import create_app, db

# Verifica se está no ambiente do Render e se a DATABASE_URL está disponível.
# Só executa a criação de tabelas se AMBAS as condições forem verdadeiras.
if os.environ.get('RENDER') and os.environ.get('DATABASE_URL'):
    print("Ambiente de produção detectado. Conectando ao banco de dados...")
    app = create_app()
    with app.app_context():
        print("Criando todas as tabelas no banco de dados de produção...")
        try:
            db.create_all()
            print("Tabelas criadas com sucesso!")
        except Exception as e:
            print(f"Ocorreu um erro ao criar as tabelas: {e}")
else:
    print("Não é um ambiente de produção ou DATABASE_URL não encontrada. O script não será executado.")

