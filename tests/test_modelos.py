import pytest

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from modelos import novo_usuario, nova_oferta

def test_novo_usuario_estrutura_correta():
    """
    Testa se a função novo_usuario cria um dicionário com a estrutura esperada.
    """
    usuario = novo_usuario("Nome Teste", "Gerador", "Recife", "email@teste.com", "senha123")
    
    assert isinstance(usuario, dict)
    assert usuario['nome'] == "Nome Teste"
    assert usuario['tipo'] == "Gerador"
    assert usuario['localizacao'] == "Recife"
    assert usuario['email'] == "email@teste.com"
    assert usuario['senha'] == "senha123"
    assert 'reputacao' in usuario
    assert 'ofertas_ativas' in usuario

def test_nova_oferta_estrutura_correta():
    """
    Testa se a função nova_oferta cria um dicionário com a estrutura esperada.
    """
    imagens_mock = ["img1.jpg", "img2.jpg"]
    oferta = nova_oferta("1", "Título Teste", "Descrição Teste", "10.5", "Olinda", imagens_mock)

    assert isinstance(oferta, dict)
    assert oferta['gerador_id'] == "1"
    assert oferta['titulo'] == "Título Teste"
    assert oferta['descricao'] == "Descrição Teste"
    assert oferta['quantidade'] == "10.5"
    assert oferta['localizacao'] == "Olinda"
    assert oferta['imagens'] == imagens_mock
    assert oferta['status'] == 'Ativa'
    assert 'laudo_link' in oferta
    assert 'timestamp_cadastro' in oferta