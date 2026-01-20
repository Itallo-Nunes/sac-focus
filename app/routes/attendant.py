from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.models import Ticket, Comment
from app.forms import CommentForm, UpdateStatusForm # Importa os formulários
from app import db

# Define o Blueprint para as rotas de atendente
attendant_bp = Blueprint('attendant', __name__, url_prefix='/atendente')

@attendant_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Exibe o painel principal para atendentes com uma lista de todos os tickets.
    """
    if not current_user.is_attendant:
        flash('Acesso negado. Esta área é restrita a atendentes.', 'danger')
        return redirect(url_for('main.index'))

    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    
    return render_template('attendant_dashboard.html', tickets=tickets)


@attendant_bp.route('/ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def view_ticket(ticket_id):
    """
    Exibe os detalhes de um ticket, permite adicionar comentários e mudar o status.
    """
    if not current_user.is_attendant:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('main.index'))
    
    ticket = Ticket.query.get_or_404(ticket_id)
    comment_form = CommentForm()
    status_form = UpdateStatusForm()

    # Lógica para adicionar um novo comentário
    if comment_form.validate_on_submit() and comment_form.submit_comment.data:
        new_comment = Comment(
            text=comment_form.text.data,
            user_id=current_user.id,
            ticket_id=ticket.id
        )
        db.session.add(new_comment)
        db.session.commit()
        flash('Comentário adicionado com sucesso!', 'success')
        return redirect(url_for('attendant.view_ticket', ticket_id=ticket.id))

    # Lógica para atualizar o status do ticket
    if status_form.validate_on_submit() and status_form.submit_status.data:
        new_status = status_form.status.data
        if ticket.status != new_status:
            ticket.status = new_status
            db.session.commit()
            flash(f'Status do ticket atualizado para "{new_status}"!', 'success')
        else:
            flash('O novo status é o mesmo do status atual.', 'info')
        return redirect(url_for('attendant.view_ticket', ticket_id=ticket.id))

    # Popula o formulário de status com o valor atual do ticket
    status_form.status.data = ticket.status
    
    # Busca os comentários para exibir no template
    comments = Comment.query.filter_by(ticket_id=ticket.id).order_by(Comment.created_at.asc()).all()

    return render_template(
        'view_ticket_atendente.html', 
        ticket=ticket, 
        comments=comments,
        comment_form=comment_form, 
        status_form=status_form
    )
