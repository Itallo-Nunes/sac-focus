### e) Diagrama de Sequência

Este diagrama mostra a interação entre os objetos do sistema ao longo do tempo para o caso de uso **"Criar Ticket"**.

*   **Objetos**: `:Cliente`, `:TelaCriarTicket`, `:ControladorTickets`, `novo_ticket:Ticket`

*   **Sequência de Mensagens:**
    1.  O `:Cliente` invoca `clicar_novo_ticket()` na `:TelaCriarTicket`.
    2.  A `:TelaCriarTicket` renderiza o formulário para o cliente.
    3.  O `:Cliente` preenche os dados e chama `submeter(dados_form)`.
    4.  A `:TelaCriarTicket` envia a mensagem `criar_ticket(dados_form)` para o `:ControladorTickets`.
    5.  O `:ControladorTickets` realiza a auto-mensagem `validar(dados_form)`.
    6.  Assumindo que a validação é bem-sucedida, o `:ControladorTickets` cria uma nova instância `novo_ticket:Ticket`.
    7.  O `novo_ticket:Ticket` é salvo no banco de dados (não representado aqui para simplicidade).
    8.  O `:ControladorTickets` retorna uma confirmação de sucesso para a `:TelaCriarTicket`.
    9.  A `:TelaCriarTicket` exibe a mensagem "Ticket criado com sucesso!" para o `:Cliente`.
