from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models import User, Ticket

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
def index():
    if 'username' not in session or session['username'] != 'admin':
        flash('Você deve ser um administrador para ver esta página.')
        return redirect(url_for('main.index'))

    users = User.query.all()
    tickets = Ticket.query.all()
    return render_template('admin.html', users=users, tickets=tickets)
