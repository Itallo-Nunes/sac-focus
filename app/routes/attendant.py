
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Ticket, Comment
from app import db

attendant_bp = Blueprint('attendant', __name__, url_prefix='/atendente')

# Decorator para verificar se o usuário é um atendente
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

@attendant_bp.route('/ticket/<int:ticket_id>')
@login_required
@attendant_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    comments = Comment.query.filter_by(ticket_id=ticket.id).order_by(Comment.created_at.asc()).all()
    return render_template('attendant_ticket_detail.html', ticket=ticket, comments=comments)

@attendant_bp.route('/ticket/<int:ticket_id>/respond', methods=['POST'])
@login_required
@attendant_required
def post_response(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    response_text = request.form.get('response')
    new_status = request.form.get('status')

    if not response_text:
        flash('A resposta não pode estar em branco.', 'danger')
        return redirect(url_for('attendant.view_ticket', ticket_id=ticket.id))

    new_comment = Comment(
        text=response_text, 
        ticket_id=ticket.id, 
        user_id=current_user.id # CORRIGIDO: de author_id para user_id
    )
    db.session.add(new_comment)

    if new_status and new_status != ticket.status:
        ticket.status = new_status

    db.session.commit()
    flash('Sua resposta foi enviada com sucesso.', 'success')

    return redirect(url_for('attendant.view_ticket', ticket_id=ticket.id))

