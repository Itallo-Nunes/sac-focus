from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
# Importamos o modelo Evaluation que estava faltando
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

        if not title or not description:
            flash('Título e Descrição são obrigatórios!', 'warning')
            return render_template('create_ticket.html', title=title, description=description)

        new_ticket = Ticket(
            title=title, 
            description=description, 
            priority=priority,
            user_id=current_user.id # CORRIGIDO: de requester_id para user_id
        )
        db.session.add(new_ticket)
        db.session.commit()

        flash('Seu ticket de suporte foi aberto com sucesso!', 'success')
        return redirect(url_for('main.index'))

    return render_template('create_ticket.html')

@tickets_bp.route('/<int:ticket_id>')
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    # Garante que o cliente só possa ver seus próprios tickets
    if ticket.user_id != current_user.id: # CORRIGIDO: de requester_id para user_id
        flash('Acesso negado.', 'danger')
        return redirect(url_for('main.index'))
    
    comments = Comment.query.filter_by(ticket_id=ticket.id).order_by(Comment.created_at.asc()).all()
    return render_template('ticket_detail.html', ticket=ticket, comments=comments)

@tickets_bp.route('/<int:ticket_id>/evaluate', methods=['GET', 'POST'])
@login_required
def evaluate(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    # Segurança: Garante que só o dono do ticket, que esteja resolvido, possa avaliar.
    if ticket.user_id != current_user.id or ticket.status != 'Resolvido': # CORRIGIDO: de requester_id para user_id
        flash('Este ticket não pode ser avaliado no momento.', 'warning')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        rating = request.form.get('rating')
        comment = request.form.get('comment')

        if not rating:
            flash('A nota é obrigatória para a avaliação.', 'danger')
            return render_template('evaluate_ticket.html', ticket=ticket)
        
        # --- LÓGICA DE AVALIAÇÃO CORRIGIDA ---
        # 1. Cria uma nova entrada na tabela Evaluation
        new_evaluation = Evaluation(
            rating=int(rating),
            comment=comment,
            ticket_id=ticket.id,
            user_id=current_user.id
        )
        db.session.add(new_evaluation)

        # 2. Atualiza o status do ticket para 'Fechado'
        ticket.status = 'Fechado'
        
        db.session.commit()

        flash('Obrigado pelo seu feedback! O ticket foi fechado.', 'success')
        return redirect(url_for('main.index'))

    return render_template('evaluate_ticket.html', ticket=ticket)
