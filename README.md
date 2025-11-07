# Circular Food Connect - Protótipo Web (Flask + JSON)

Repositório do protótipo **Circular Food Connect**!

Este projeto é uma aplicação web construída com **Flask** para simular uma plataforma de economia circular. Seu principal diferencial é a lógica de otimização (IA) em segundo plano, que conecta Geradores de excedentes a Receptores de matéria-prima, promovendo a sustentabilidade alimentar.

## Como Executar o Protótipo Web

### Pré-requisitos

1.  **Python 3.x** instalado.
2.  **Ambiente Virtual (`venv`)** ativado.
3.  **Flask** instalado: `pip install Flask`

### Inicialização do Servidor (Instrução Corrigida!)

Para evitar erros de `ModuleNotFound`, o servidor deve ser executado a partir da pasta `/src`.

1.  Abra seu terminal.
2.  **Navegue para a pasta `src`** dentro do diretório do projeto:

    ```bash
    cd src
    ```
3.  **Certifique-se de que o ambiente virtual está ativo.**
4.  Execute o servidor Flask:

    ```bash
    python app.py
    ```
5.  Abra seu navegador e acesse a URL que o Flask fornecerá (geralmente: `http://127.0.0.1:5000/`).

## 📋 Funcionalidades Chave (Backend Atualizado)

| Funcionalidade | Implementação |
| :--- | :--- |
| **Login e Cadastro** | Refatorado para autenticação por **E-mail e Senha**. Rotas `/api/login` (POST) e `/cadastro` (GET) implementadas. |
| **CRUD de Oferta (C/R/U/D)** | Lógica completa de CRUD de Oferta no módulo `servicos.py`. **Front-end de listagem e detalhes agora é 100% dinâmico.** |
| **Transação** | Lógica de compra fracionada por Kg implementada em `servicos.py`. |
| **Histórico** | Lógica de rastreabilidade (compras/vendas) integrada à tela `/historicoDeCompras.html` de forma dinâmica. |
| **Controle de Acesso** | Rotas de cadastro e edição de ofertas são restritas via *decorator* `@requer_perfil('Gerador')`. |