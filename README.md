# ♻️ Circular Food Connect - Protótipo (Python Puro)

Repositório do protótipo **Circular Food Connect**!

Este projeto visa prototipar um marketplace B2B inteligente focado na economia circular de resíduos industriais do setor de alimentos e bebidas. Nosso principal diferencial é o uso de lógica de otimização (IA) para conectar geradores de resíduos a receptores de matéria-prima.

**Status Atual:** Protótipo de console funcional com CRUD completo para usuários e ofertas, lógica transacional e persistência de dados.

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

## 📋 Funcionalidades Implementadas

O protótipo atual é totalmente funcional via console e simula as interações principais da plataforma.

### Gerais
*   **Gestão de Usuários:**
    *   Cadastro de novos usuários com perfis de **Gerador** ou **Receptor**.
    *   Listagem de todos os usuários cadastrados.
    *   Simulação de **Login** para operar o sistema como um usuário específico.
*   **Persistência de Dados:** Todas as informações de usuários e ofertas são salvas em arquivos JSON, garantindo que os dados persistam entre as execuções.

### 👤 Funcionalidades do Gerador
*   **CRUD de Ofertas:**
    *   **Cadastrar** novas ofertas de resíduos.
    *   **Listar** suas ofertas ativas.
    *   **Editar** informações de suas ofertas (título, descrição, quantidade, valor).
    *   **Excluir** ofertas. A lógica de exclusão protege o histórico:
        *   Se uma oferta já teve vendas, seu status é alterado para `Removida` para manter o registro.
        *   Se não houver histórico, a oferta é permanentemente deletada.
*   **Histórico de Vendas:** Visualização detalhada de todas as vendas realizadas, agrupadas por oferta, incluindo quem comprou, a quantidade e a data da transação.

### 👤 Funcionalidades do Receptor
*   **Visualização e Compra:**
    *   **Listar** todas as ofertas ativas de todos os geradores.
    *   **Buscar** ofertas por palavras-chave no título ou descrição.
    *   **Comprar** uma quantidade total ou parcial (em Kg) de uma oferta.
    *   Quando uma compra esgota o estoque de uma oferta, a oferta é automaticamente marcada como `Removida`.
*   **Histórico de Compras:** Acesso a um registro completo de todas as compras feitas, detalhando o produto, o gerador, a quantidade e a data.