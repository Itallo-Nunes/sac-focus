from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Ticket, Comment
from app import db

attendant_bp = Blueprint('attendant', __name__, url_prefix='/atendente')

# Decorator to check if the user is an attendant
def attendant_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_attendant:
            flash('Acesso negado. Você precisa ser um atendente para ver esta página.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@attendant_bp.route('/dashboard')
@login_required
@attendant_required
def dashboard():
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return render_template('attendant_dashboard.html', tickets=tickets)

@attendant_bp.route('/ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
@attendant_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if request.method == 'POST':
        if 'status' in request.form:
            new_status = request.form.get('status')
            if new_status and new_status != ticket.status:
                ticket.status = new_status
                db.session.commit()
                flash(f'O status do ticket #{ticket.id} foi atualizado para {new_status}.', 'success')
        
        if 'comment_text' in request.form:
            comment_text = request.form.get('comment_text')
            if comment_text:
                new_comment = Comment(text=comment_text, user_id=current_user.id, ticket_id=ticket.id)
                db.session.add(new_comment)
                db.session.commit()
                flash('Seu comentário foi adicionado.', 'success')

        return redirect(url_for('attendant.view_ticket', ticket_id=ticket.id))

    comments = Comment.query.filter_by(ticket_id=ticket.id).order_by(Comment.created_at.asc()).all()
    return render_template('ticket_detail.html', ticket=ticket, comments=comments)
