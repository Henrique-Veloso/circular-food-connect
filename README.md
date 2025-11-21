# ♻️ Circular Food Connect - Protótipo Web (Flask + JSON)

Este projeto é um protótipo de aplicação web construído com **Flask** que simula uma plataforma de **economia circular**. O objetivo é conectar **Geradores** de excedentes e subprodutos (matérias-primas circulares) a **Receptores** que buscam insumos, com uma lógica de otimização em segundo plano para promover a sustentabilidade alimentar e industrial.

***

## ⚙️ Tecnologias Utilizadas

O projeto é desenvolvido primariamente em Python e utiliza os seguintes componentes:

| Componente | Função |
| :--- | :--- |
| **Python 3.x** | Linguagem de programação principal. |
| **Flask** | Micro-framework web para a criação das rotas e do servidor. |
| **Jinja2** | Motor de *templates* para renderização dinâmica das páginas HTML. |
| **JSON** | Utilizado para persistência de dados de usuários e ofertas (`data/usuarios.json` e `data/ofertas.json`). |
| **Tailwind CSS** | Framework de CSS para o *design* das páginas (`.html`). |

### Dependências

As principais dependências do projeto estão listadas em `requirements.txt`:
* `Flask==3.1.2`
* `Jinja2==3.1.6`
* `Werkzeug==3.1.3`
* `pytest==9.0.1` (Para execução de testes).

***

## 🚀 Como Executar o Protótipo Web

Siga as instruções abaixo para configurar e iniciar o servidor Flask localmente.

### Pré-requisitos

1.  Tenha o **Python 3.x** instalado.
2.  Clone este repositório.

### Instalação

1.  Crie e ative um ambiente virtual (`venv`):
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No Linux/macOS:
    source venv/bin/activate
    ```
2.  Instale as dependências do projeto:
    ```bash
    pip install -r requirements.txt
    ```

### Inicialização do Servidor

Para evitar erros de importação (`ModuleNotFound`), o servidor **deve ser executado a partir da pasta `/src`**.

1.  Navegue para a pasta `src`:
    ```bash
    cd src
    ```
2.  Execute o servidor Flask:
    ```bash
    python app.py
    ```
3.  Abra seu navegador e acesse a URL fornecida (geralmente: `http://127.0.0.1:5000/`).

***

## 📋 Funcionalidades Chave (Backend Atualizado)

O protótipo implementa um fluxo completo para Geradores e Receptores de matéria-prima:

| Funcionalidade | Detalhes da Implementação |
| :--- | :--- |
| **Login e Cadastro** | Autenticação de usuários por **E-mail e Senha**. O usuário escolhe entre os perfis **Gerador** (quem oferta) ou **Receptor** (quem compra). |
| **Listagem de Ofertas** | Exibe as ofertas ativas para todos. Utiliza a função `obter_ofertas_otimizadas` (simulando otimização/IA) para priorizar a listagem, geralmente por menor preço. |
| **CRUD de Oferta** | Usuários **Geradores** podem criar, listar (`/ofertas/minhas`), editar e remover suas ofertas. A edição inclui a atualização de título, descrição, quantidade e valor por Kg. |
| **Transação de Compra** | Usuários **Receptores** podem comprar uma quantidade fracionada (em Kg) de uma oferta ativa. A transação atualiza o saldo disponível do produto no banco de dados JSON. |
| **Histórico de Transações** | Rastreabilidade de todas as transações realizadas. Exibe um histórico de **"Minhas Compras"** (para Receptores) e **"Minhas Vendas"** (para Geradores). |
| **Controle de Acesso** | Rotas sensíveis (cadastro, edição de ofertas, listagem de minhas ofertas) são restritas por perfil via *decorator* `@requer_perfil`. |

***

## 🧪 Executando Testes

O projeto inclui testes unitários e de integração utilizando **Pytest**.

Para executar todos os testes, certifique-se de que o ambiente virtual está ativo e execute o comando na raiz do projeto:

```bash
pytest