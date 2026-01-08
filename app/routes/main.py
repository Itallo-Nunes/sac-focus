
# Adicionamos redirect e url_for para o redirecionamento
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from ..models import Ticket

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # --- LÓGICA DE REDIRECIONAMENTO PARA ATENDENTES ---
    # Se o usuário logado for um atendente, ele é redirecionado para o dashboard correto.
    if current_user.is_authenticated and current_user.is_attendant:
        return redirect(url_for('attendant.dashboard'))

    tickets = []
    # Se o usuário for um cliente logado, buscamos apenas os seus tickets.
    if current_user.is_authenticated:
        tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(Ticket.created_at.desc()).all()
    
    # Para usuários não logados ou clientes, renderiza a página inicial.
    return render_template('index.html', tickets=tickets)
