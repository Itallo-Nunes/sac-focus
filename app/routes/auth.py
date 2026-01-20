from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User, Ticket, Comment, Evaluation
from .. import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Email ou senha inválidos. Por favor, tente novamente.', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        flash('Login realizado com sucesso!', 'success')
        
        if user.is_attendant:
            return redirect(url_for('attendant.dashboard'))
        else:
            return redirect(url_for('main.index'))

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role') # Captura o papel do formulário

        if not email or not password or not role:
            flash('Por favor, preencha todos os campos.', 'danger')
            return redirect(url_for('auth.register'))

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Este email já está cadastrado.', 'warning')
            return redirect(url_for('auth.register'))

        new_user = User(
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            role=role # Salva o papel no banco
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Cadastro realizado com sucesso! Faça o login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not check_password_hash(current_user.password, current_password):
            flash('Sua senha atual está incorreta.', 'danger')
            return redirect(url_for('auth.change_password'))

        if new_password != confirm_password:
            flash('A nova senha e a confirmação não correspondem.', 'danger')
            return redirect(url_for('auth.change_password'))

        current_user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        db.session.commit()

        flash('Sua senha foi alterada com sucesso!', 'success')
        return redirect(url_for('main.index'))

    return render_template('change_password.html')

@auth_bp.route('/confirm-delete', methods=['GET'])
@login_required
def confirm_delete():
    """Exibe a página de confirmação para deletar a conta."""
    return render_template('confirm_delete.html')

@auth_bp.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    """
    Anonimiza os dados do usuário (tickets, comentários, avaliações)
    e, em seguida, deleta a conta do usuário de forma atômica e segura.
    """
    user_to_delete = current_user

    try:
        # O bloco `no_autoflush` impede que o SQLAlchemy tente salvar
        # alterações no banco de dados prematuramente enquanto iteramos
        # sobre as relações do usuário. As alterações só serão enviadas
        # com o `db.session.commit()` final.
        with db.session.no_autoflush:
            # Anonimiza os tickets, comentários e avaliações
            for ticket in user_to_delete.tickets:
                ticket.user_id = None
            for comment in user_to_delete.comments:
                comment.user_id = None
            for evaluation in user_to_delete.evaluations:
                evaluation.user_id = None

            # Após anonimizar as referências, o usuário pode ser deletado
            db.session.delete(user_to_delete)

        # Agora, todas as alterações são salvas de uma vez (atomicamente)
        db.session.commit()

        logout_user()
        flash('Sua conta foi removida com sucesso.', 'success')

    except Exception as e:
        # Se ocorrer qualquer erro, reverte todas as alterações
        db.session.rollback()
        # Log do erro seria ideal em um app de produção
        print(f"Erro ao deletar conta: {e}")
        flash('Ocorreu um erro inesperado ao remover sua conta. Tente novamente.', 'danger')

    return redirect(url_for('main.index'))
