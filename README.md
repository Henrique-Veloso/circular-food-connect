# ♻️ Circular Food Connect - Protótipo (Python Puro)

Repositório do protótipo **Circular Food Connect**!

Este projeto visa prototipar um marketplace B2B inteligente focado na economia circular de resíduos industriais do setor de alimentos e bebidas. Nosso principal diferencial é o uso de lógica de otimização (IA) para conectar geradores de resíduos a receptores de matéria-prima.

**Status Atual:** **CRUD Completo e Lógica Transacional Concluída (Sprint 2)**. A interface gráfica (HTML/CSS) está sendo construída na Sprint 3.

## 🚀 Como Executar o Protótipo (Console)

### Pré-requisitos

* **Python 3.x** instalado.

### 1. Estrutura do Projeto

A arquitetura do projeto está dividida entre o Python (`/src`) e a camada de interface (`/web`):

### 2. Inicialização

1.  Abra seu terminal na pasta do projeto (raiz).
2.  Navegue até a pasta do código:
    ```bash
    cd src
    ```
3.  Execute o arquivo principal:

    ```bash
    python main.py
    ```
    *(Você será apresentado ao menu de Login/Cadastro/Sair.)*

## 📋 Funcionalidades Chave

| Funcionalidade | Módulo | Descrição |
| :--- | :--- | :--- |
| **Login e Acesso** | `main.py` | Controla o acesso e as opções disponíveis por perfil (`Gerador`/`Receptor`). |
| **Cadastro de Usuário (C)** | `main.py` | Permite criar Gerador/Receptor e salva os dados. |
| **CRUD de Oferta (C/R/U/D)** | `main.py` | Permite cadastrar, listar, **editar (Update)** e **excluir (Delete)** ofertas de resíduo. |
| **Transação Parcial** | `main.py` | O Receptor pode **comprar uma quantidade fracionada (Kg)**, atualizando o saldo da oferta. |
| **Histórico** | `main.py` | O usuário pode visualizar seu histórico completo de compras e vendas. |
| **Persistência de Dados** | `persistencia.py` | Garante que os dados sejam salvos e carregados corretamente via JSON. |