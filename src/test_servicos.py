import pytest
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from servicos import autenticar_usuario, criar_usuario_servico

# --- Dados Falsos (Mocks) para os Testes ---

MOCK_USUARIOS = {
    "1": {
        "id": "1",
        "nome": "Usuario Teste",
        "email": "teste@exemplo.com",
        "senha": "senha123",
        "tipo": "Receptor"
    }
}

# --- Testes para autenticar_usuario ---

@patch('servicos.load_data')
def test_autenticar_usuario_sucesso(mock_load_data):
    """
    Testa se um usuário consegue se autenticar com credenciais corretas.
    """
    # Configura o mock para retornar nossos dados falsos quando load_data for chamado
    mock_load_data.return_value = MOCK_USUARIOS

    # Chama a função que queremos testar
    usuario = autenticar_usuario("teste@exemplo.com", "senha123")

    # Verifica os resultados
    assert usuario is not None
    assert usuario['email'] == "teste@exemplo.com"
    assert 'senha' not in usuario  # Garante que a senha foi removida

@patch('servicos.load_data')
def test_autenticar_usuario_falha(mock_load_data):
    """
    Testa se a autenticação falha com uma senha incorreta.
    """
    mock_load_data.return_value = MOCK_USUARIOS

    usuario = autenticar_usuario("teste@exemplo.com", "senha_errada")

    assert usuario is None

@patch('servicos.salvar_novo_usuario')
@patch('servicos.obter_usuario_por_email')
def test_criar_usuario_servico_sucesso(mock_obter_por_email, mock_salvar_novo_usuario):
    """
    Testa a criação de um novo usuário com sucesso.
    """
    mock_obter_por_email.return_value = None  # Simula que o email não existe
    mock_salvar_novo_usuario.return_value = {"id": "2", "nome": "Novo Usuario"}

    novo_usuario = criar_usuario_servico("Novo Usuario", "Gerador", "Recife", "novo@email.com", "senhaforte")

    mock_salvar_novo_usuario.assert_called_once()
    assert novo_usuario is not None
    assert novo_usuario["nome"] == "Novo Usuario"

@patch('servicos.obter_usuario_por_email')
def test_criar_usuario_servico_falha_email_existente(mock_obter_por_email):
    """
    Testa se a criação de usuário falha quando o e-mail já existe.
    """
    mock_obter_por_email.return_value = MOCK_USUARIOS["1"]

    with pytest.raises(ValueError) as excinfo:
        criar_usuario_servico("Outro Usuario", "Receptor", "Olinda", "teste@exemplo.com", "outrasenha")

    assert "Este E-mail já está cadastrado." in str(excinfo.value)