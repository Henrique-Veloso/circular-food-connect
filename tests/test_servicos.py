import pytest
from unittest.mock import patch, MagicMock, ANY

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from servicos import (autenticar_usuario, criar_usuario_servico,
                      transacao_compra_servico, editar_oferta_servico, deletar_oferta_servico,
                      obter_historico_transacoes, obter_usuario_por_email)

MOCK_USUARIOS = {
    "1": {
        "id": "1",
        "nome": "Usuario Receptor",
        "email": "receptor@exemplo.com",
        "senha": "senha123",
        "tipo": "Receptor"
    },
    "2": {
        "id": "2",
        "nome": "Usuario Gerador",
        "email": "gerador@exemplo.com",
        "senha": "senha456",
        "tipo": "Gerador"
    }
}

MOCK_OFERTAS = {
    "1": {
        "id": "1",
        "titulo": "Tomates",
        "descricao": "Tomates frescos da horta.",
        "quantidade": "5.0", # 5.0 kg disponíveis
        "status": "Ativa",
        "historico_compras": [
            {
                "comprador_id": "1", # Comprado pelo Usuario Receptor
                "quantidade": 2.0, "timestamp": 1672531200
            }
        ]
    }
}

@patch('servicos.load_data')
def test_autenticar_usuario_sucesso(mock_load_data):
    """
    Testa se um usuário consegue se autenticar com credenciais corretas.
    """
    mock_load_data.return_value = MOCK_USUARIOS

    usuario = autenticar_usuario("receptor@exemplo.com", "senha123")

    assert usuario is not None
    assert usuario['email'] == "receptor@exemplo.com"
    assert 'senha' not in usuario  # Garante que a senha foi removida

@patch('servicos.load_data')
def test_autenticar_usuario_falha(mock_load_data):
    """
    Testa se a autenticação falha com uma senha incorreta.
    """
    mock_load_data.return_value = MOCK_USUARIOS

    usuario = autenticar_usuario("receptor@exemplo.com", "senha_errada")

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
        criar_usuario_servico("Outro Usuario", "Receptor", "Olinda", "receptor@exemplo.com", "outrasenha")

    assert "Este E-mail já está cadastrado." in str(excinfo.value)

@patch('servicos.load_data')
def test_transacao_compra_servico_falha_quantidade_insuficiente(mock_load_data):
    """
    Testa se a transação de compra falha ao solicitar uma quantidade maior que a disponível.
    """
    mock_load_data.return_value = {
        "1": { "id": "1", "quantidade": "5.0", "status": "Ativa" }
    }

    with pytest.raises(ValueError) as excinfo:
        transacao_compra_servico(oferta_id="1", comprador_id="3", quantidade_desejada=10.0)

    assert "Quantidade solicitada excede o saldo disponível." in str(excinfo.value)

@patch('servicos.save_data')
@patch('servicos.load_data')
def test_editar_oferta_sucesso(mock_load_data, mock_save_data):
    """
    Testa se um usuário consegue editar sua própria oferta com sucesso.
    """
    oferta_original = {
        "1": {"id": "1", "gerador_id": "2", "titulo": "Tomates", "descricao": "Tomates frescos.", "status": "Ativa"}
    }
    mock_load_data.return_value = oferta_original

    novos_dados = {'titulo': 'Tomates Orgânicos', 'quantidade': '7.5'}
    oferta_editada = editar_oferta_servico(oferta_id="1", gerador_id="2", novos_dados=novos_dados)

    assert oferta_editada['titulo'] == 'Tomates Orgânicos'
    assert oferta_editada['quantidade'] == '7.5'

    mock_save_data.assert_called_once()

@patch('servicos.load_data')
def test_editar_oferta_falha_sem_permissao(mock_load_data):
    """
    Testa se a edição falha quando um usuário tenta editar uma oferta que não é sua.
    """
    mock_load_data.return_value = {
        "1": {"id": "1", "gerador_id": "2", "titulo": "Tomates"}
    }

    novos_dados = {'titulo': 'Tentativa de Invasão'}
    with pytest.raises(PermissionError) as excinfo:
        editar_oferta_servico(oferta_id="1", gerador_id="99", novos_dados=novos_dados)

    assert "Oferta não encontrada ou sem permissão de edição." in str(excinfo.value)

@patch('servicos.save_data')
@patch('servicos.load_data')
def test_deletar_oferta_sucesso_sem_historico(mock_load_data, mock_save_data):
    """Testa se uma oferta sem histórico é excluída permanentemente."""
    mock_load_data.return_value = {
        "1": {"id": "1", "gerador_id": "2"}
    }

    deletar_oferta_servico(oferta_id="1", gerador_id="2")

    mock_save_data.assert_called_once_with({}, ANY)

@patch('servicos.save_data')
@patch('servicos.load_data')
def test_deletar_oferta_sucesso_com_historico(mock_load_data, mock_save_data):
    """Testa se uma oferta com histórico é marcada como 'Removida'."""
    mock_load_data.return_value = {
        "1": {"id": "1", "gerador_id": "2", "historico_compras": [{"id": "compra1"}]}
    }

    deletar_oferta_servico(oferta_id="1", gerador_id="2")

    args, _ = mock_save_data.call_args
    dados_salvos = args[0]
    assert dados_salvos["1"]["status"] == "Removida"

@patch('servicos.load_data')
def test_deletar_oferta_falha_sem_permissao(mock_load_data):
    """Testa se a exclusão falha quando o usuário não é o dono da oferta."""
    mock_load_data.return_value = {
        "1": {"id": "1", "gerador_id": "2"}
    }

    with pytest.raises(PermissionError) as excinfo:
        deletar_oferta_servico(oferta_id="1", gerador_id="99")

    assert "Oferta não encontrada ou sem permissão de exclusão." in str(excinfo.value)

@patch('servicos.load_data')
def test_obter_historico_transacoes_para_gerador(mock_load_data):
    """Testa se o histórico de um Gerador é retornado corretamente."""
    def side_effect(file_path):
        if 'usuarios' in file_path:
            return MOCK_USUARIOS
        if 'ofertas' in file_path:
            return MOCK_OFERTAS
        return {}
    mock_load_data.side_effect = side_effect

    historico = obter_historico_transacoes(user_id="2", user_tipo="Gerador")

    assert len(historico) == 1
    transacao = historico[0]
    assert transacao['tipo'] == 'Venda'
    assert transacao['parceiro'] == 'Usuario Receptor' # Nome do comprador
    assert transacao['titulo'] == 'Tomates'

@patch('servicos.load_data')
def test_obter_historico_transacoes_para_receptor(mock_load_data):
    """Testa se o histórico de um Receptor é retornado corretamente."""
    def side_effect(file_path):
        if 'usuarios' in file_path:
            return MOCK_USUARIOS
        if 'ofertas' in file_path:
            return MOCK_OFERTAS
        return {}
    mock_load_data.side_effect = side_effect

    historico = obter_historico_transacoes(user_id="1", user_tipo="Receptor")

    assert len(historico) == 1
    transacao = historico[0]
    assert transacao['tipo'] == 'Compra'
    assert transacao['parceiro'] == 'Usuario Gerador' # Nome do vendedor
    assert transacao['titulo'] == 'Tomates'