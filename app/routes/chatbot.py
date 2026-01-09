import os
import google.generativeai as genai
from flask import Blueprint, request, jsonify, render_template
from flask_login import current_user
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

chatbot_bp = Blueprint('chatbot', __name__)

# --- Configuração da IA Generativa do Google ---
API_KEY = os.getenv("GEMINI_API_KEY")
model = None

if not API_KEY:
    print("\033[91mAviso: A variável de ambiente GEMINI_API_KEY não foi definida.\033[0m")
    print("O chatbot ficará desativado até que a chave seja configurada.")
else:
    try:
        genai.configure(api_key=API_KEY)
        
        generation_config = {
            "temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048
        }
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        
        # CORREÇÃO: Usa o nome de modelo estável para evitar conflito de recursos.
        model = genai.GenerativeModel(
            model_name="gemini-1.0-pro",
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        print("\033[92mModelo Generative AI configurado com sucesso.\033[0m")

    except Exception as e:
        print(f"\033[91mErro Crítico ao configurar o modelo Generative AI: {e}\033[0m")
        model = None

# Rota para renderizar a página do chatbot
@chatbot_bp.route('/')
def chat_page():
    """Exibe a página de chat."""
    chatbot_enabled = model is not None and API_KEY
    return render_template('chatbot.html', chatbot_enabled=chatbot_enabled)


# Dicionário em memória para históricos de chat
chat_histories = {}

def get_chatbot_response_ai(user_id, message):
    """Obtém uma resposta do modelo de IA mantendo o histórico."""
    if user_id not in chat_histories:
        chat_histories[user_id] = model.start_chat(history=[])
    
    chat_session = chat_histories[user_id]

    try:
        contextual_prompt = f"""
        Você é um assistente virtual de atendimento da empresa SACFocus. 
        Seu objetivo é ajudar usuários com dúvidas sobre suporte e produtos.
        Se a pergunta for complexa ou exigir dados pessoais, instrua o usuário a abrir um chamado.
        Não responda a perguntas fora do contexto de atendimento ao cliente.
        
        Pergunta: {message}
        """
        response = chat_session.send_message(contextual_prompt)
        return response.text
    except Exception as e:
        # RESTAURAÇÃO FINAL: Volta para a mensagem de erro genérica.
        print(f"\033[91mErro ao se comunicar com a API do Gemini: {e}\033[0m")
        return "Desculpe, ocorreu um erro ao processar sua solicitação. Tente mais tarde."


@chatbot_bp.route('/ask', methods=['POST'])
def ask():
    """Lida com as perguntas enviadas pelo chatbot no frontend."""
    if not model or not API_KEY:
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

    bot_response = get_chatbot_response_ai(user_id, user_message)
    return jsonify({'answer': bot_response})
