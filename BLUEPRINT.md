### **Blueprint do Projeto: Aplicação de HelpDesk "SACFocus"**

Este documento descreve a estrutura, os recursos e os componentes da aplicação que desenvolvemos.

#### **1. Visão Geral dos Recursos**

Construímos um sistema de suporte ao cliente completo com os seguintes recursos principais:

*   **Autenticação de Usuários:**
    *   Registro de novas contas (clientes).
    *   Login e Logout seguros.
    *   Distinção de papéis: **Cliente** e **Atendente**.

*   **Sistema de Tickets (Chamados):**
    *   **Clientes** podem criar, visualizar e acompanhar seus próprios tickets.
    *   Os tickets possuem título, descrição, prioridade e status.
    *   O ciclo de vida de um ticket segue os status: `Aberto` -> `Em andamento` -> `Resolvido` -> `Fechado`.

*   **Painel do Atendente:**
    *   Uma área restrita (`/atendente/dashboard`) onde os atendentes podem ver **todos** os tickets do sistema.
    *   Atendentes podem visualizar os detalhes de cada ticket, alterar seu status e interagir com os clientes.

*   **Sistema de Comentários:**
    *   Clientes e atendentes podem se comunicar através de comentários dentro de cada ticket.
    *   Os comentários são exibidos em ordem cronológica.
    *   A interface diferencia visualmente os comentários de atendentes.

*   **Avaliação do Atendimento:**
    *   Após um ticket ser marcado como "Resolvido", o cliente tem a opção de avaliar o atendimento com uma nota (1 a 5 estrelas) e um comentário.
    *   Ao avaliar, o ticket é automaticamente movido para o status "Fechado".
    *   A avaliação fica registrada e visível na página do ticket.

*   **Chatbot de Suporte Básico:**
    *   Um chatbot simples na página inicial que responde a perguntas frequentes sobre produtos, preços e como abrir um chamado.

#### **2. Estrutura do Projeto (Arquivos e Pastas)**

A aplicação está organizada de forma modular, principalmente dentro da pasta `app/`.

```
/
|-- app/
|   |-- __init__.py             # Fábrica da aplicação: inicializa o Flask, o DB e registra os Blueprints.
|   |-- models.py               # Modelos do banco de dados (User, Ticket, Comment, Evaluation).
|   |-- db.sqlite               # Arquivo do banco de dados SQLite.
|   |
|   |-- routes/
|   |   |-- __init__.py         # (Vazio, apenas para o pacote)
|   |   |-- auth.py             # Rotas de autenticação (/register, /login, /logout).
|   |   |-- main.py             # Rota principal (página inicial).
|   |   |-- tickets.py          # Rotas para clientes (criar, ver e avaliar tickets).
|   |   |-- attendant.py        # Rotas do painel do atendente (dashboard, ver ticket, mudar status).
|   |   |-- chatbot.py          # Rota da API do chatbot.
|   |
|   |-- templates/
|   |   |-- base.html               # Template base com a estrutura HTML e navegação.
|   |   |-- index.html              # Página inicial (com chatbot e lista de tickets do cliente).
|   |   |-- login.html              # Formulário de login.
|   |   |-- register.html           # Formulário de registro.
|   |   |-- create_ticket.html      # Formulário de criação de ticket.
|   |   |-- ticket_detail.html      # Página de detalhes de um ticket (usada por clientes e atendentes).
|   |   |-- attendant_dashboard.html# Painel principal dos atendentes.
|   |   |-- evaluate_ticket.html    # Formulário de avaliação do atendimento.
|   |
|   |-- static/
|       |-- js/
|           |-- chatbot.js          # Lógica de front-end para o chatbot.
|       |-- css/
|           |-- style.css           # Estilos globais e para o chatbot.
|
|-- requirements.txt            # Dependências Python do projeto (Flask, SQLAlchemy, etc.).
|-- devserver.sh                # Script para iniciar o servidor de desenvolvimento.
|-- .venv/                      # Pasta do ambiente virtual Python.
|-- BLUEPRINT.md                # Este arquivo de resumo.
```

#### **3. Componentes (Blueprints e Banco de Dados)**

*   **Banco de Dados (`models.py`):**
    *   `User`: Armazena `id`, `email`, `password` e `role` (Cliente/Atendente).
    *   `Ticket`: Contém `title`, `description`, `priority`, `status` e as relações com `User` e `Evaluation`.
    *   `Comment`: Armazena o `text` do comentário e as relações com `User` e `Ticket`.
    *   `Evaluation`: Guarda o `rating` (nota), `comment` da avaliação e a relação com o `Ticket`.

*   **Blueprints (`routes/`):**
    *   `main_bp`: Serve a página principal (`index.html`).
    *   `auth_bp` (`/auth`): Gerencia o registro, login e logout de usuários.
    *   `chatbot_bp` (`/chatbot`): Fornece o endpoint `/ask` para a API do chatbot.
    *   `tickets_bp` (`/tickets`): Permite que clientes criem (`/create`), visualizem (`/<id>`) e avaliem (`/<id>/evaluate`) seus tickets.
    *   `attendant_bp` (`/atendente`): Fornece o painel restrito para atendentes (`/dashboard`) e a visualização detalhada de tickets (`/ticket/<id>`).
