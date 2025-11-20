import json
import os
import time
USUARIOS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'usuarios.json')
OFERTAS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'ofertas.json')
def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    if not isinstance(data, dict):
        return {}
    return data
def save_data(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
def get_next_id(data_dict):
    if not data_dict:
        return "1"
    return max([int(k) for k in data_dict.keys()]) + 1
def salvar_novo_usuario(novo_usuario):
    dados_usuarios = load_data(USUARIOS_FILE)
    novo_id = str(get_next_id(dados_usuarios))
    novo_usuario['id'] = novo_id
    dados_usuarios[novo_id] = novo_usuario
    save_data(dados_usuarios, USUARIOS_FILE)
    return novo_usuario
def salvar_nova_oferta(nova_oferta):
    dados_oferta = load_data(OFERTAS_FILE)
    novo_id = str(get_next_id(dados_oferta))
    nova_oferta['id'] = novo_id
    nova_oferta['timestamp_cadastro'] = int(time.time())
    dados_oferta[novo_id] = nova_oferta
    save_data(dados_oferta, OFERTAS_FILE)
    return nova_oferta