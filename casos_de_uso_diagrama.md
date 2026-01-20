### b) Diagrama de Casos de Uso

Este diagrama mostra as funcionalidades do sistema (casos de uso) e quem as utiliza (atores).

*   **Atores:**
    *   **Cliente**: O usuário final que busca suporte.
    *   **Atendente**: O funcionário que presta o suporte.

*   **Diagrama (descrição textual):**

    *   **Ator: Cliente**
        *   `Fazer Login/Logout`
        *   `Registrar Conta`
        *   `Criar Ticket`
        *   `Visualizar Meus Tickets`
        *   `Adicionar Comentário ao Ticket`
        *   `Avaliar Atendimento` (<<extends>> de uma ação do Atendente)
        *   `Usar Chatbot`

    *   **Ator: Atendente**
        *   `Fazer Login/Logout`
        *   `Visualizar Dashboard de Tickets` (vê todos os tickets)
        *   `Adicionar Comentário ao Ticket`
        *   `Alterar Status do Ticket` (Esta ação pode levar ao caso de uso `Avaliar Atendimento` do Cliente)
