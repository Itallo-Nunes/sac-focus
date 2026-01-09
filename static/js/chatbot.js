
document.addEventListener('DOMContentLoaded', function() {
    // Verifica se o container do chatbot existe na página
    const chatbotContainer = document.getElementById('chatbot-container');
    if (!chatbotContainer) {
        return; // Se não houver container, não faz nada
    }

    // --- CRIAÇÃO DO HTML DO CHATBOT ---
    const chatbotHTML = `
        <!-- Botão Flutuante (FAB) para abrir o chat -->
        <div id="chatbot-fab">
            <i class="bi bi-robot"></i>
        </div>

        <!-- Janela do Chat -->
        <div id="chatbot-window" class="card hidden">
            <div class="card-header">
                <span>SACFocus Chatbot</span>
                <button type="button" class="btn-close" aria-label="Close" id="close-chatbot"></button>
            </div>
            <div class="card-body" id="chat-log">
                <!-- Mensagens do chat serão inseridas aqui -->
                <div class="chat-message bot-message">
                    <div class="message-content">
                        Olá! Como posso te ajudar hoje?
                    </div>
                </div>
            </div>
            <div class="card-footer">
                <form id="chat-form">
                    <div class="input-group">
                        <input type="text" id="chat-input" class="form-control" placeholder="Digite sua mensagem..." autocomplete="off" required>
                        <button type="submit" class="btn btn-primary">
                            <i class="bi bi-send"></i>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    `;

    chatbotContainer.innerHTML = chatbotHTML;

    // --- SELETORES DE ELEMENTOS DO DOM ---
    const chatbotFab = document.getElementById('chatbot-fab');
    const chatbotWindow = document.getElementById('chatbot-window');
    const closeChatbotBtn = document.getElementById('close-chatbot');
    const chatLog = document.getElementById('chat-log');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    
    // --- LÓGICA DE FUNCIONAMENTO DO CHATBOT ---

    // Abrir a janela do chat ao clicar no botão flutuante
    chatbotFab.addEventListener('click', () => {
        chatbotWindow.classList.toggle('hidden');
        chatbotFab.classList.add('hidden'); // Esconde o FAB quando a janela está aberta
    });

    // Fechar a janela do chat
    closeChatbotBtn.addEventListener('click', () => {
        chatbotWindow.classList.add('hidden');
        chatbotFab.classList.remove('hidden'); // Mostra o FAB novamente
    });

    // Envio da mensagem do formulário
    chatForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const userMessage = chatInput.value.trim();

        if (userMessage) {
            addMessageToLog(userMessage, 'user');
            chatInput.value = '';
            sendMessageToBot(userMessage);
        }
    });

    /**
     * Adiciona uma mensagem à janela de chat.
     * @param {string} message - O texto da mensagem.
     * @param {'user' | 'bot'} sender - Quem enviou a mensagem.
     */
    function addMessageToLog(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', sender === 'user' ? 'user-message' : 'bot-message');
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.textContent = message;

        messageDiv.appendChild(contentDiv);
        chatLog.appendChild(messageDiv);

        // Rola para a mensagem mais recente
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    /**
     * Envia a mensagem do usuário para o endpoint da API do chatbot.
     * @param {string} message - A mensagem a ser enviada.
     */
    async function sendMessageToBot(message) {
        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: message }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            const botReply = data.answer;

            addMessageToLog(botReply, 'bot');

        } catch (error) {
            console.error('Erro ao contatar o chatbot:', error);
            addMessageToLog('Desculpe, não consigo me conectar ao meu cérebro agora. Tente novamente mais tarde.', 'bot');
        }
    }
    
    // --- LÓGICA DA AVALIAÇÃO DE ESTRELAS ---
    const starRatingContainer = document.getElementById('star-rating-container');
    if (starRatingContainer) {
        const stars = starRatingContainer.querySelectorAll('.star-rating input');
        
        stars.forEach(star => {
            star.addEventListener('change', () => {
                const rating = star.value;
                // Esconde as estrelas e mostra a mensagem de agradecimento
                const ratingSystem = document.getElementById('rating-system');
                const thanksMessage = document.getElementById('thanks-for-rating');
                
                if (ratingSystem && thanksMessage) {
                    ratingSystem.classList.add('hidden');
                    thanksMessage.classList.remove('hidden');
                }
                
                console.log(`Usuário avaliou com ${rating} estrelas.`);
                // Aqui você poderia enviar a avaliação para o backend, se necessário.
            });
        });
    }
});
