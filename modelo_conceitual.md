### a) Modelo Conceitual

Este modelo representa as entidades principais do domínio do sistema de HelpDesk e como elas se relacionam.

*   **Entidades e Atributos:**
    *   **Usuário**: Representa uma pessoa que usa o sistema.
        *   *Atributos*: ID, Nome, Email, Senha, Papel (Cliente ou Atendente).
    *   **Ticket**: O registro de uma solicitação (chamado) de um cliente.
        *   *Atributos*: ID, Título, Descrição, Prioridade, Status (Aberto, Em andamento, Resolvido, Fechado).
    *   **Comentário**: Uma mensagem trocada dentro de um ticket.
        *   *Atributos*: ID, Texto do Comentário, Data de Postagem.
    *   **Avaliação**: O feedback dado pelo cliente sobre um atendimento.
        *   *Atributos*: ID, Nota (1 a 5), Comentário da Avaliação.

*   **Relacionamentos e Cardinalidade:**
    *   Um `Cliente` (que é um tipo de `Usuário`) **cria** 1 ou mais `Tickets`. (1,N)
    *   Um `Atendente` (que é um tipo de `Usuário`) **atende** 0 ou mais `Tickets`. (0,N)
    *   Um `Ticket` **contém** 0 ou mais `Comentários`. (0,N)
    *   Um `Usuário` (Cliente ou Atendente) **posta** 0 ou mais `Comentários`. (0,N)
    *   Um `Ticket` **recebe** 0 ou 1 `Avaliação`. (0,1)
    *   Um `Cliente` **faz** 0 ou mais `Avaliações`. (0,N)
