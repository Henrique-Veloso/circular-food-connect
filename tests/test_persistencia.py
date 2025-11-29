import pytest
import json
from unittest.mock import patch

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from persistencia import load_data, save_data, get_next_id, salvar_novo_usuario

def test_load_data_arquivo_inexistente(tmp_path):
    arquivo_inexistente = tmp_path / "nao_existe.json"
    dados = load_data(str(arquivo_inexistente))
    assert dados == {}

def test_save_e_load_data(tmp_path):
    arquivo_teste = tmp_path / "teste.json"
    dados_originais = {"1": {"nome": "Teste"}}

    save_data(dados_originais, str(arquivo_teste))

    dados_carregados = load_data(str(arquivo_teste))
    assert dados_carregados == dados_originais

def test_get_next_id():
    assert get_next_id({}) == "1"
    assert get_next_id({"1": {}, "3": {}}) == 4

@patch('persistencia.OFERTAS_FILE', 'dummy_path_ofertas')
@patch('persistencia.USUARIOS_FILE', 'dummy_path_usuarios')
@patch('persistencia.load_data')
@patch('persistencia.save_data')
def test_salvar_novo_usuario_chama_funcoes_corretas(mock_save, mock_load):
    mock_load.return_value = {"1": {"id": "1", "nome": "Usuario Antigo"}}
    
    novo_usuario_data = {"nome": "Novo Usuario"}
    salvar_novo_usuario(novo_usuario_data)

    mock_load.assert_called_once_with('dummy_path_usuarios')

    dados_esperados = {"1": {"id": "1", "nome": "Usuario Antigo"}, "2": {"id": "2", "nome": "Novo Usuario"}}
    mock_save.assert_called_once_with(dados_esperados, 'dummy_path_usuarios')