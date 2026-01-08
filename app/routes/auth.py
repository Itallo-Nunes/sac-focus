from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user:
            flash('Nome de usuário já existe.')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))

        db.session.add(new_user)
        db.session.commit()

        flash('Cadastro realizado com sucesso. Por favor, faça o login.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Por favor, verifique seus dados de login e tente novamente.')
            return redirect(url_for('auth.login'))

        session['user_id'] = user.id
        session['username'] = user.username
        flash('Login realizado com sucesso!')
        return redirect(url_for('tickets.index'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Você foi desconectado.')
    return redirect(url_for('main.index'))
