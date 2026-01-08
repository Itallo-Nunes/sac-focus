
from flask import Blueprint, render_template
from flask_login import current_user
from ..models import Ticket

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    tickets = []
    # Se o usuário estiver logado e não for um atendente, buscamos seus tickets
    if current_user.is_authenticated and not current_user.is_attendant:
        # CORREÇÃO DEFINITIVA: Trocando requester_id por user_id
        tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(Ticket.created_at.desc()).all()
    
    # Passamos os tickets para o template (será uma lista vazia se o usuário não estiver logado)
    return render_template('index.html', tickets=tickets)
