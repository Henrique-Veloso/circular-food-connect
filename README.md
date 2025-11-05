# ♻️ Circular Food Connect - Protótipo Web (Flask + JSON)

Repositório do protótipo **Circular Food Connect**!

Este projeto evoluiu do console para uma aplicação web, utilizando **Flask** como framework de backend. Nosso principal diferencial é o uso de lógica de otimização (IA) para conectar geradores de resíduos a receptores de matéria-prima.

**Status Atual:** **Início da Sprint 3 (Flask Core e Interface Gráfica)**. O backend de CRUD está refatorado em Serviços (sem `input()`/`print()`).

---

## 🚀 Como Executar o Protótipo Web

### Pré-requisitos

1.  **Python 3.x** instalado.
2.  **Ambiente Virtual (`venv`)** ativado.
3.  **Flask** instalado: `pip install Flask`

### 1. Estrutura do Projeto

/projetocfc ├── /src # Camada de Backend (Servidor Flask e Lógica) │ ├── app.py # Servidor Flask e Rotas (O novo 'main') │ ├── servicos.py # Lógica de Negócio (CRUD Refatorado - SEM print/input) │ ├── modelos.py # Estruturas de Dados │ └── persistencia.py # Leitura e escrita em JSON │ ├── /data # Simulação do Banco de Dados (JSON) │ ├── ofertas.json │ └── usuarios.json │ └── /web # Camada Visual (Frontend) ├── /css ├── /js └── *.html # Templates Jinja (Ex: loginUsuario.html, listaDeProdutos.html)

### 2. Inicialização do Servidor

1.  Abra seu terminal na pasta `/projetocfc/src`.
2.  **Certifique-se de que o ambiente virtual está ativo.**
3.  Execute o servidor Flask:

    ```bash
    python app.py
    ```
4.  Abra seu navegador e acesse a URL que o Flask fornecerá (geralmente: `http://127.0.0.1:5000/`).

## 📋 Funcionalidades Chave 

A lógica das seguintes funcionalidades está completa e disponível para ser integrada ao Front-end via rotas Flask:

| Funcionalidade | Implementação |
| :--- | :--- |
| **Login e Cadastro** | Rotas `/login` (POST) e `/cadastro` (GET) implementadas para controle de acesso. |
| **CRUD de Oferta (C/R/U/D)** | Lógica completa de CRUD de Oferta (incluindo Edição e Exclusão Segura) no módulo `servicos.py`. |
| **Transação** | Lógica de compra fracionada por Kg implementada em `servicos.py`. |
| **Histórico** | Lógica de rastreabilidade (compras/vendas) pronta para ser consumida pela API. |