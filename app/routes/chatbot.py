
import os
import json
import google.generativeai as genai
from flask import Blueprint, request, jsonify, render_template
from flask_login import current_user
from dotenv import load_dotenv

load_dotenv()

chatbot_bp = Blueprint('chatbot', __name__)

faq_data = {}
try:
    with open('faq.json', 'r', encoding='utf-8') as f:
        faq_data = json.load(f).get('perguntas', [])
    print("\033[92mBase de conhecimento (faq.json) carregada.\033[0m")
except FileNotFoundError:
    print("\033[93mAviso: O arquivo faq.json não foi encontrado. O chatbot usará apenas a IA Generativa.\033[0m")
except json.JSONDecodeError:
    print("\033[91mErro: Falha ao decodificar o arquivo faq.json. Verifique a formatação.\033[0m")

API_KEY = os.getenv("GEMINI_API_KEY")
model = None

if not API_KEY:
    print("\033[91mAviso: A variável de ambiente GEMINI_API_KEY não foi definida.\033[0m")
else:
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.0-pro')
        print("\033[92mModelo Generative AI configurado com sucesso.\033[0m")
    except Exception as e:
        print(f"\033[91mErro Crítico ao configurar o modelo Generative AI: {e}\033[0m")
        model = None

def find_in_faq(user_message):
    if not faq_data:
        return None
    user_words = set(user_message.lower().split())
    best_match = None
    max_match_count = 0
    for item in faq_data:
        question_words = set(item['pergunta'].lower().split())
        match_count = len(user_words.intersection(question_words))
        if match_count > max_match_count:
            max_match_count = match_count
            best_match = item['resposta']
    if max_match_count > 1:
        return best_match
    return None

chat_histories = {}

def get_chatbot_response(user_id, user_message):
    faq_answer = find_in_faq(user_message)
    if faq_answer:
        return faq_answer
    if not model:
        return "Desculpe, não encontrei uma resposta na nossa base de conhecimento e o serviço de IA não está disponível no momento."
    if user_id not in chat_histories:
        chat_histories[user_id] = model.start_chat(history=[])
    chat_session = chat_histories[user_id]
    try:
        contextual_prompt = f"""
        Você é um assistente virtual de atendimento da empresa SACFocus.
        Seu objetivo é ajudar usuários com dúvidas sobre suporte e produtos.
        Se a pergunta for complexa ou exigir dados pessoais, instrua o usuário a abrir um chamado.
        Não responda a perguntas fora do contexto de atendimento ao cliente.
        
        Pergunta: {user_message}
        """
        response = chat_session.send_message(contextual_prompt)
        return response.text
    except Exception as e:
        print(f"\033[91mErro ao se comunicar com a API do Gemini: {e}\033[0m")
        return "Desculpe, ocorreu um erro ao processar sua solicitação. Tente mais tarde."

@chatbot_bp.route('/')
def chat_page():
    chatbot_enabled = API_KEY is not None
    return render_template('chatbot.html', chatbot_enabled=chatbot_enabled)

@chatbot_bp.route('/ask', methods=['POST'])
def ask():
    if not API_KEY:
        return jsonify({'answer': "Desculpe, o serviço de chatbot não está ativado no momento."}), 503
    if current_user.is_authenticated and current_user.is_attendant:
        return jsonify({'answer': "A funcionalidade de chatbot não se aplica a atendentes."}), 403
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'A pergunta (question) é obrigatória.'}), 400
    user_message = data['question']
    if current_user.is_authenticated:
        user_id = f"user_{current_user.id}"
    else:
        user_id = f"session_{request.cookies.get('session', 'anonymous')}"
    bot_response = get_chatbot_response(user_id, user_message)
    return jsonify({'answer': bot_response})
