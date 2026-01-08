from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Ticket, Comment, Evaluation
from app import db

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_ticket():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        new_ticket = Ticket(title=title, description=description, priority=priority, user_id=current_user.id)
        db.session.add(new_ticket)
        db.session.commit()
        flash('Seu chamado foi aberto com sucesso!', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_ticket.html')

@tickets_bp.route('/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.user_id != current_user.id and not current_user.is_attendant:
        flash('Você não tem permissão para ver este ticket.', 'danger')
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        comment_text = request.form.get('comment_text')
        if comment_text:
            new_comment = Comment(text=comment_text, user_id=current_user.id, ticket_id=ticket.id)
            db.session.add(new_comment)
            db.session.commit()
            flash('Seu comentário foi adicionado.', 'success')
            return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))
    comments = Comment.query.filter_by(ticket_id=ticket.id).order_by(Comment.created_at.asc()).all()
    return render_template('ticket_detail.html', ticket=ticket, comments=comments)

@tickets_bp.route('/<int:ticket_id>/evaluate', methods=['GET', 'POST'])
@login_required
def evaluate_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.user_id != current_user.id:
        flash('Você não tem permissão para avaliar este ticket.', 'danger')
        return redirect(url_for('main.index'))
    if ticket.status != 'Resolvido':
        flash('Só é possível avaliar tickets com o status "Resolvido".', 'warning')
        return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))
    if ticket.evaluation:
        flash('Este ticket já foi avaliado.', 'info')
        return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))
    if request.method == 'POST':
        rating = request.form.get('rating')
        comment = request.form.get('comment')
        if not rating:
            flash('Por favor, selecione uma nota.', 'danger')
            return render_template('evaluate_ticket.html', ticket=ticket)
        evaluation = Evaluation(rating=int(rating), comment=comment, ticket_id=ticket.id, user_id=current_user.id)
        db.session.add(evaluation)
        ticket.status = 'Fechado'
        db.session.commit()
        flash('Obrigado pela sua avaliação! O ticket foi fechado.', 'success')
        return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))
    return render_template('evaluate_ticket.html', ticket=ticket)
