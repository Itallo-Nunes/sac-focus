### c) Casos de Uso Textuais

Aqui detalhamos os passos de três funcionalidades centrais.

#### **1. Criar Ticket**
- **Nome do Caso de Uso**: Criar Ticket de Suporte
- **Ator Principal**: Cliente
- **Pré-condições**: O Cliente deve estar autenticado no sistema.
- **Fluxo Principal**:
  1.  O Cliente seleciona a opção "Criar Novo Ticket".
  2.  O sistema exibe um formulário com campos para Título, Descrição e Prioridade.
  3.  O Cliente preenche os campos obrigatórios.
  4.  O Cliente submete o formulário.
  5.  O sistema valida os dados (todos os campos devem ser preenchidos).
  6.  O sistema cria um novo Ticket, associa-o ao Cliente logado e define seu status como "Aberto".
  7.  O sistema exibe uma mensagem de confirmação e redireciona o Cliente para a lista de seus tickets.
- **Fluxos Alternativos**:
  - **5a. Dados Inválidos**: Se a validação falhar, o sistema exibe mensagens de erro junto aos campos correspondentes e não cria o ticket, permitindo que o Cliente corrija os dados.
- **Pós-condições**: Um novo ticket com status "Aberto" existe no sistema, visível para o Cliente que o criou e para todos os Atendentes.

#### **2. Atender Ticket**
- **Nome do Caso de Uso**: Atender Ticket
- **Ator Principal**: Atendente
- **Pré-condições**: O Atendente deve estar autenticado. Existe pelo menos um ticket no sistema.
- **Fluxo Principal**:
  1.  O Atendente acessa o "Dashboard de Tickets" e vê a lista de todos os chamados.
  2.  O Atendente seleciona um ticket para visualizar seus detalhes.
  3.  O sistema exibe o histórico de conversas e o status atual do ticket.
  4.  O Atendente escreve uma resposta ou pergunta no campo de comentários.
  5.  O Atendente submete o comentário.
  6.  O sistema salva o comentário, diferenciando-o visualmente como uma mensagem de um atendente.
  7.  Se o status do ticket era "Aberto", o sistema o altera automaticamente para "Em andamento".
- **Fluxos Alternativos**:
  - **5a. Resolver Ticket**: Se o Atendente considera a dúvida resolvida, ele pode, além de comentar, alterar o status do ticket para "Resolvido".
- **Pós-condições**: O ticket contém um novo comentário do Atendente e seu status pode ser atualizado. O Cliente é notificado.

#### **3. Avaliar Atendimento**
- **Nome do Caso de Uso**: Avaliar Atendimento
- **Ator Principal**: Cliente
- **Pré-condições**: O Cliente deve estar autenticado. O ticket que ele deseja avaliar deve estar com o status "Resolvido".
- **Fluxo Principal**:
  1.  O Cliente abre a página de detalhes de um ticket com status "Resolvido".
  2.  O sistema exibe um formulário de avaliação (nota de 1 a 5 estrelas e um campo de comentário).
  3.  O Cliente seleciona uma nota e, opcionalmente, escreve um comentário.
  4.  O Cliente submete a avaliação.
  5.  O sistema salva a nota e o comentário, associando-os ao ticket.
  6.  O sistema altera o status do ticket para "Fechado".
  7.  O sistema exibe uma mensagem de "Obrigado pelo feedback!".
- **Fluxos Alternativos**:
  - **3a. Tentativa de avaliar ticket não resolvido**: Se o ticket não estiver com status "Resolvido", o formulário de avaliação não é exibido.
- **Pós-condições**: A avaliação fica registrada no sistema. O ticket é movido para o estado final "Fechado".
