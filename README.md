# Circular Food Connect - Protótipo (Python Puro)

Repositório do protótipo **Circular Food Connect**!

Este projeto visa prototipar um marketplace B2B inteligente focado na economia circular de resíduos industriais do setor de alimentos e bebidas. Nosso principal diferencial é o uso de lógica de otimização (IA) para conectar geradores de resíduos a receptores de matéria-prima.

## Como Executar o Protótipo

### Pré-requisitos

* **Python 3** instalado.

### 1. Estrutura do Projeto

/projetocfc 

/src 

/ main.py - Ponto de entrada (Menu e Interface) 

/ modelos.py - Definição das estruturas de dados (Usuário, Oferta) 

/ persistencia.py - Lógica de leitura e escrita em JSON


/ data

/ ofertas.json - Base de dados (simulada) de Ofertas 

/ usuarios.json - Base de dados (simulada) de Usuários

### 2. Inicialização

1.  Abra seu terminal na pasta `/projetocfc/src`.
2.  Execute o arquivo principal:

    ```bash
    python main.py
    ```

### Funcionalidades

Ao executar o programa, você terá acesso ao menu inicial para testar as seguintes funcionalidades **MUST-HAVE**:

| Funcionalidade | Módulo | Descrição |

| **Cadastro de Usuário (C)** | `main.py` -> `cadastrar_usuario()` | Permite criar um novo Gerador ou Receptor e salva os dados no `usuarios.json`. |

| **Listagem de Usuários (R)** | `main.py` -> `listar_usuarios()` | Exibe todos os usuários cadastrados (Geradores e Receptores). |

| **Persistência de Dados** | `persistencia.py` | Garante que os dados sejam salvos e carregados corretamente entre as execuções do programa. |