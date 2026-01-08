from flask import Blueprint, render_template, request, jsonify

chatbot_bp = Blueprint('chatbot', __name__)

def get_chatbot_response(message):
    message = message.lower().strip()
    if "produto" in message:
        return "Oferecemos uma variedade de produtos para atender às suas necessidades. Em que tipo de produto você está interessado?"
    elif "preço" in message:
        return "Você pode encontrar nossas informações de preços na página de preços."
    elif "problema" in message or "dificuldade" in message:
        return "Lamento saber que você está com um problema. Por favor, abra um chamado para que um de nossos atendentes possa ajudá-lo em detalhes."
    elif "ticket" in message or "chamado" in message:
        return "Para criar um chamado, você precisa estar logado. Depois, basta clicar em 'Criar Ticket' no menu de navegação."
    elif "contato" in message:
        return "A melhor forma de entrar em contato é abrindo um chamado através da sua conta. Se não conseguir acessar sua conta, pode nos contatar pelo email: suporte@sacfocus.com"
    elif "olá" in message or "oi" in message:
        return "Olá! Como posso te ajudar hoje?"
    elif "adeus" in message or "tchau" in message:
        return "Até mais! Se precisar de algo, estarei por aqui."
    else:
        return "Não tenho certeza se entendi. Você pode reformular sua pergunta ou digitar 'contato' para ver as opções de suporte."

@chatbot_bp.route('/')
def index():
    """Renders the chatbot page."""
    return render_template('chatbot.html')

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """Handles chat messages from the user."""
    data = request.get_json()
    user_message = data.get('message', '')
    bot_response = get_chatbot_response(user_message)
    return jsonify({'response': bot_response})
