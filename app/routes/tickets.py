from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app.models import Ticket, User
from app import db

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        flash('Você precisa estar logado para ver esta página.')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = session['user_id']

        new_ticket = Ticket(title=title, content=content, user_id=user_id)
        db.session.add(new_ticket)
        db.session.commit()
        flash('Seu ticket foi criado com sucesso!')
        return redirect(url_for('tickets.index'))

    user = User.query.get(session['user_id'])
    tickets = user.tickets

    return render_template('tickets.html', tickets=tickets)
