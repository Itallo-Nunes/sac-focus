
import os
import json
from flask import Blueprint, request, jsonify, render_template

chatbot_bp = Blueprint('chatbot', __name__)

# Carrega a árvore de conversas do novo arquivo JSON
with open('chatbot_tree.json', 'r', encoding='utf-8') as f:
    chatbot_tree = json.load(f)

@chatbot_bp.route('/')
def chat_page():
    # A página do chatbot agora está sempre ativa.
    return render_template('chatbot.html', chatbot_enabled=True)

@chatbot_bp.route('/flow', methods=['POST'])
def flow():
    """
    Esta nova rota controla o fluxo da conversa.
    Recebe o nó atual e retorna a mensagem e as opções correspondentes.
    """
    data = request.get_json()
    node_id = data.get('node', 'inicio') # Começa pelo nó 'inicio' se nenhum for fornecido

    node = chatbot_tree.get(node_id)

    if not node:
        # Se um nó inválido for solicitado, retorna para o início
        node = chatbot_tree.get('inicio')

    return jsonify(node)
