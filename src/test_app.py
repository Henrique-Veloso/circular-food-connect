import pytest
from unittest.mock import patch

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app as flask_app

@pytest.fixture
def app():
    """Cria e configura uma nova instância do app para cada teste."""
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    """Um cliente de teste para o app."""
    return app.test_client()

def test_index_page(client):
    """
    Testa se a página inicial (/) carrega corretamente.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Circular Food Conect" in response.data

@patch('app.autenticar_usuario')
def test_login_sucesso(mock_autenticar_usuario, client):
    """
    Testa o fluxo de login com sucesso via POST para /api/login.
    """
    mock_autenticar_usuario.return_value = {
        "id": "1",
        "nome": "Usuario Teste",
        "email": "teste@exemplo.com",
        "tipo": "Receptor"
    }

    response = client.post('/api/login', data={
        'email': 'teste@exemplo.com',
        'senha': 'senha123'
    })

    mock_autenticar_usuario.assert_called_once_with('teste@exemplo.com', 'senha123')

    assert response.status_code == 302 # 302 é o código para redirecionamento
    assert response.location == '/ofertas/listagem'

    with client.session_transaction() as sess:
        assert sess['usuario_ativo']['email'] == 'teste@exemplo.com'

@patch('app.autenticar_usuario')
def test_login_falha(mock_autenticar_usuario, client):
    """
    Testa o fluxo de login com falha via POST para /api/login.
    """
    mock_autenticar_usuario.return_value = None

    response = client.post('/api/login', data={
        'email': 'teste@exemplo.com',
        'senha': 'senha_errada'
    })

    assert response.status_code == 200
    assert b"E-mail ou senha inv\xc3\xa1lidos." in response.data

def test_cadastro_oferta_page_sem_login(client):
    """
    Testa se um usu\xc3\xa1rio n\xc3\xa3o logado \xc3\xa9 redirecionado da p\xc3\xa1gina de cadastro de oferta.
    """
    response = client.get('/ofertas/cadastro')
    assert response.status_code == 302  # Redirecionamento
    assert response.location == '/login?erro=Acesso+restrito.'

@patch('app.criar_usuario_servico')
def test_cadastro_usuario_sucesso(mock_criar_usuario, client):
    """
    Testa o fluxo de cadastro de usu\xc3\xa1rio com sucesso.
    """
    response = client.post('/api/cadastro_usuario', data={
        'nome': 'Novo Usu\xc3\xa1rio',
        'email': 'novo@email.com',
        'senha': 'senha123',
        'tipo': 'Receptor',
        'cidade': 'Recife'
    })

    mock_criar_usuario.assert_called_once()
    assert response.status_code == 302
    assert response.location == '/login?sucesso=Cadastro+realizado+com+sucesso!+Fa%C3%A7a+seu+login.'

@patch('app.render_template')
@patch('app.criar_usuario_servico')
def test_cadastro_usuario_falha_email_existente(mock_criar_usuario, mock_render_template, client):
    """
    Testa a falha no cadastro de usu\xc3\xa1rio quando o e-mail j\xc3\xa1 existe.
    """
    error_message = "Este E-mail j\xc3\xa1 est\xc3\xa1 cadastrado."
    mock_criar_usuario.side_effect = ValueError(error_message)

    response = client.post('/api/cadastro_usuario', data={
        'nome': 'Usuario Repetido',
        'email': 'existente@email.com',
        'senha': 'senhaqualquer',
        'tipo': 'Receptor',
        'cidade': 'Recife'
    })

    mock_render_template.assert_called_once_with(
        'cadastrarUsuario.html', erro=f"Erro no cadastro: {error_message}"
    )

@patch('app.criar_oferta_servico')
def test_cadastro_oferta_sucesso_com_login(mock_criar_oferta, client):
    """
    Testa o cadastro de uma nova oferta por um usuário 'Gerador' logado.
    """
    with client.session_transaction() as sess:
        sess['usuario_ativo'] = {
            "id": "2", "nome": "Usuario Gerador", "tipo": "Gerador"
        }

    response = client.post('/api/cadastro_oferta', data={
        'titulo': 'Casca de Laranja',
        'descricao': 'Cascas para fazer doce.',
        'quantidade': '10',
        'valor_de_venda': '5',
        'cidade': 'Olinda'
    })

    mock_criar_oferta.assert_called_once()
    assert response.status_code == 302
    assert response.location == '/ofertas/listagem?sucesso=Oferta+publicada+com+sucesso%21'

@patch('app.transacao_compra_servico')
def test_compra_oferta_sucesso(mock_transacao, client):
    """
    Testa a compra de uma oferta por um usuário 'Receptor' logado.
    """
    with client.session_transaction() as sess:
        sess['usuario_ativo'] = {
            "id": "1", "nome": "Usuario Receptor", "tipo": "Receptor"
        }

    mock_transacao.return_value = {'status': 'Ativa', 'restante': '8.0'}

    response = client.post('/api/ofertas/comprar/1', data={'quantidade_desejada': '2.0'})

    mock_transacao.assert_called_once_with('1', '1', 2.0)
    assert response.status_code == 302
    assert 'sucesso=Compra+de+2.0+Kg+realizada+com+sucesso' in response.location

def test_compra_oferta_falha_perfil_invalido(client):
    """
    Testa se um usuário 'Gerador' é impedido de comprar uma oferta.
    """
    with client.session_transaction() as sess:
        sess['usuario_ativo'] = {
            "id": "2", "nome": "Usuario Gerador", "tipo": "Gerador"
        }

    response = client.post('/api/ofertas/comprar/1', data={'quantidade_desejada': '1.0'})

    assert response.status_code == 302
    assert 'erro=Apenas+usu%C3%A1rios+Receptores+podem+realizar+esta+transa%C3%A7%C3%A3o.' in response.location

@patch('app.obter_historico_transacoes')
def test_historico_page_com_login(mock_obter_historico, client):
    """
    Testa se a página de histórico é carregada para um usuário logado.
    """
    with client.session_transaction() as sess:
        sess['usuario_ativo'] = {"id": "1", "nome": "Usuario Teste", "tipo": "Receptor"}

    mock_obter_historico.return_value = []
    response = client.get('/historico')

    assert response.status_code == 200
    mock_obter_historico.assert_called_once_with("1", "Receptor")