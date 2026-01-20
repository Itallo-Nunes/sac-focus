### d) Diagrama de Classes

Este diagrama traduz o modelo conceitual para uma estrutura de software orientada a objetos.

*   **`Usuario (Abstrata)`**
    *   `- id: int`
    *   `- nome: str`
    *   `- email: str`
    *   `- senha_hash: str`
    *   `+ login()`
    *   `+ logout()`

*   **`Cliente`** (Herda de `Usuario`)
    *   `+ criar_ticket(titulo, desc, prio): Ticket`
    *   `+ avaliar_atendimento(ticket, nota, comentario)`

*   **`Atendente`** (Herda de `Usuario`)
    *   `+ visualizar_dashboard(): list[Ticket]`
    *   `+ alterar_status_ticket(ticket, novo_status)`

*   **`Ticket`**
    *   `- id: int`
    *   `- titulo: str`
    *   `- descricao: str`
    *   `- prioridade: str`
    *   `- status: str`
    *   `- criador: Cliente` (Associação)
    *   `- comentarios: list[Comentario]` (Composição)
    *   `- avaliacao: Avaliacao` (Associação)
    *   `+ adicionar_comentario(texto, autor)`
    *   `+ alterar_status(novo_status)`

*   **`Comentario`**
    *   `- id: int`
    *   `- texto: str`
    *   `- data: datetime`
    *   `- autor: Usuario` (Associação)

*   **`Avaliacao`**
    *   `- id: int`
    *   `- nota: int`
    *   `- comentario_texto: str`
