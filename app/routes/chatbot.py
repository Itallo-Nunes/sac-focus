import os
import google.generativeai as genai
from flask import Blueprint, request, jsonify
from flask_login import current_user
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

chatbot_bp = Blueprint('chatbot', __name__)

# --- Configuração da IA Generativa do Google ---
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("\033[91mAviso: A variável de ambiente GEMINI_API_KEY não foi definida.\033[0m")
        print("O chatbot usará respostas padrão. Crie um arquivo .env e adicione GEMINI_API_KEY='sua_chave'.")
        genai.configure(api_key="DUMMY_KEY_FOR_TESTING") # Evita crash se a chave não existir
    else:
        genai.configure(api_key=api_key)

    # Configurações do modelo
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
except Exception as e:
    print(f"\033[91mErro ao configurar o modelo Generative AI: {e}\033[0m")
    model = None

# Simples dicionário em memória para guardar o histórico de cada usuário
chat_histories = {}

def get_chatbot_response_ai(user_id, message):
    """Obtém uma resposta do modelo de IA mantendo o histórico."""
    if not model or not api_key:
        return "Desculpe, a conexão com o serviço de IA não está configurada corretamente."
    
    # Recupera ou inicia um novo histórico de chat
    if user_id not in chat_histories:
        chat_histories[user_id] = model.start_chat(history=[])
    
    chat_session = chat_histories[user_id]

    try:
        # Adiciona um contexto ao prompt para manter o foco no atendimento
        contextual_prompt = f"""
        Você é um assistente virtual de atendimento ao cliente para uma empresa chamada SACFocus. 
        Seu objetivo é ajudar os usuários com suas dúvidas sobre produtos, serviços e suporte.
        Se a pergunta for muito complexa ou exigir acesso a dados pessoais, 
        instrua o usuário a abrir um chamado para que um atendente humano possa ajudar.
        Não responda a perguntas que não tenham relação com atendimento ao cliente.
        
        Pergunta do usuário: {message}
        """
        response = chat_session.send_message(contextual_prompt)
        return response.text
    except Exception as e:
        print(f"\033[91mErro ao se comunicar com a API do Gemini: {e}\033[0m")
        return "Desculpe, ocorreu um erro ao processar sua solicitação. Por favor, tente novamente mais tarde."

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """Lida com as mensagens do chat do usuário."""
    data = request.get_json()
    user_message = data.get('message', '')
    
    # Identifica o usuário (logado ou anônimo pela session ID)
    if current_user.is_authenticated:
        user_id = f"user_{current_user.id}"
    else:
        # Para usuários não logados, usamos o ID da sessão do Flask
        user_id = f"session_{request.cookies.get('session')}"

    bot_response = get_chatbot_response_ai(user_id, user_message)
    return jsonify({'response': bot_response})

