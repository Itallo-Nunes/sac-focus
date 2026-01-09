from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
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
