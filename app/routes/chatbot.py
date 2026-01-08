from flask import Blueprint, render_template, request, session

chatbot_bp = Blueprint('chatbot', __name__)

def ai_chatbot(message):
    message = message.lower()
    if "produto" in message:
        return "Oferecemos uma variedade de produtos para atender às suas necessidades. Em que tipo de produto você está interessado?"
    elif "preço" in message:
        return "Você pode encontrar nossas informações de preços na página de preços. Gostaria que eu o redirecionasse para lá?"
    elif "problema" in message or "dificuldade" in message:
        return "Lamento saber que você está com um problema. Você pode descrever o problema com mais detalhes? Talvez eu possa ajudá-lo a solucionar o problema."
    elif "ticket" in message:
        if 'user_id' in session:
            return "Posso ajudá-lo a criar um ticket de suporte. Qual é o título do seu ticket?"
        else:
            return "Você precisa estar logado para criar um ticket de suporte. Por favor, faça o login e tente novamente."
    elif "contato" in message:
        return "Você pode entrar em contato com nossa equipe de suporte criando um ticket de suporte. Gostaria que eu o ajudasse com isso?"
    elif "olá" in message:
        return "Olá! Como posso ajudá-lo hoje?"
    elif "adeus" in message:
        return "Adeus! Tenha um ótimo dia!"
    else:
        return "Não tenho certeza se entendi. Você pode reformular sua pergunta?"

@chatbot_bp.route('/', methods=['GET', 'POST'])
def index():
    response = None
    if request.method == 'POST':
        user_message = request.form['message']
        response = ai_chatbot(user_message)
    return render_template('chatbot.html', response=response)
