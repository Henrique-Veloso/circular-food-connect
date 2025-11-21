import time
import datetime
import math
from persistencia import *
from modelos import *

def obter_todos_usuarios():
    dados_usuarios = load_data(USUARIOS_FILE)
    return list(dados_usuarios.values())

def autenticar_usuario(email, senha):
    dados_usuarios = load_data(USUARIOS_FILE)
    for usuario in dados_usuarios.values():
        if usuario.get('email', '') == email and usuario.get('senha', '') == senha:
            usuario_limpo = usuario.copy()
            usuario_limpo.pop('senha', None)
            return usuario_limpo
    return None

def obter_usuario_por_email(email):
    dados_usuarios = load_data(USUARIOS_FILE)
    for usuario in dados_usuarios.values():
        if usuario.get('email', '') == email:
            return usuario
    return None

def obter_usuario_por_credencial(input_busca):
    dados_usuarios = load_data(USUARIOS_FILE)
    for usuario in dados_usuarios.values():
        if input_busca == usuario.get('id') or input_busca.lower() == usuario.get('nome', '').lower():
            return usuario
    return None

def criar_usuario_servico(nome, tipo, cidade, email, senha):
    if tipo not in ['Gerador', 'Receptor']:
        raise ValueError("Tipo de usuário inválido.")
    if obter_usuario_por_email(email):
        raise ValueError("Este E-mail já está cadastrado.")
    novo = novo_usuario(nome, tipo, cidade, email, senha)
    return salvar_novo_usuario(novo)

def obter_todas_ofertas_ativas():
    dados_ofertas = load_data(OFERTAS_FILE)
    ofertas_ativas = [oferta for oferta in dados_ofertas.values() if oferta.get('status') == 'Ativa']
    return ofertas_ativas

def obter_oferta_por_id(oferta_id):
    dados_ofertas = load_data(OFERTAS_FILE)
    return dados_ofertas.get(oferta_id)

def obter_ofertas_por_gerador_id(gerador_id):
    dados_ofertas = load_data(OFERTAS_FILE)
    ofertas_do_gerador = [
        oferta 
        for oferta in dados_ofertas.values() 
        if oferta.get('gerador_id') == gerador_id
    ]
    return ofertas_do_gerador

def criar_oferta_servico(gerador_id, titulo, descricao, quantidade, valor_de_venda, cidade, imagens=None):
    if not all([titulo, descricao, quantidade, valor_de_venda]):
        raise ValueError("Campos obrigatórios faltando.")
    try:
        float(quantidade)
        float(valor_de_venda)
    except ValueError:
        raise ValueError("Quantidade e Valor devem ser números válidos.")
    nova = nova_oferta(
        gerador_id=gerador_id,
        titulo=titulo,
        descricao=descricao,
        quantidade=str(quantidade),
        cidade=cidade,
        imagens=imagens 
    )
    nova['valor_de_venda'] = str(valor_de_venda)
    return salvar_nova_oferta(nova)

def editar_oferta_servico(oferta_id, gerador_id, novos_dados):
    dados_ofertas = load_data(OFERTAS_FILE)
    oferta = dados_ofertas.get(oferta_id)
    if not oferta or oferta['gerador_id'] != gerador_id:
        raise PermissionError("Oferta não encontrada ou sem permissão de edição.")
    oferta['titulo'] = novos_dados.get('titulo', oferta['titulo'])
    oferta['descricao'] = novos_dados.get('descricao', oferta['descricao'])   
    nova_quantidade_str = novos_dados.get('quantidade')
    if nova_quantidade_str:
        try:
            nova_quantidade = float(nova_quantidade_str)
            if nova_quantidade > 0:
                oferta['quantidade'] = str(nova_quantidade)
        except ValueError:
            pass
    nova_valor_str = novos_dados.get('valor_de_venda')
    if nova_valor_str:
        try:
            novo_valor = float(nova_valor_str)
            if novo_valor >= 0:
                oferta['valor_de_venda'] = str(novo_valor)
        except ValueError:
            pass
    if oferta['status'] == 'Removida' and float(oferta['quantidade']) > 0:
        oferta['status'] = 'Ativa'
    save_data(dados_ofertas, OFERTAS_FILE)
    return oferta

def deletar_oferta_servico(oferta_id, gerador_id):
    dados_ofertas = load_data(OFERTAS_FILE)
    oferta = dados_ofertas.get(oferta_id)
    if not oferta or oferta['gerador_id'] != gerador_id:
        raise PermissionError("Oferta não encontrada ou sem permissão de exclusão.")
    if 'historico_compras' in oferta and oferta['historico_compras']:
        oferta['status'] = 'Removida'
        save_data(dados_ofertas, OFERTAS_FILE)
        return True, "Oferta marcada como 'Removida' (histórico preservado)."
    else:
        del dados_ofertas[oferta_id]
        save_data(dados_ofertas, OFERTAS_FILE)
        return True, "Oferta excluída permanentemente."
    
def transacao_compra_servico(oferta_id, comprador_id, quantidade_desejada):
    dados_ofertas = load_data(OFERTAS_FILE)
    oferta = dados_ofertas.get(oferta_id)
    if not oferta or oferta['status'] != 'Ativa':
        raise ValueError("Oferta inválida ou não ativa.")
    try:
        quantidade_disponivel = float(oferta['quantidade'])
    except ValueError:
        raise ValueError("Quantidade da oferta em formato inválido.")
    if quantidade_desejada > quantidade_disponivel:
        raise ValueError("Quantidade solicitada excede o saldo disponível.")
    nova_quantidade_disponivel = quantidade_disponivel - quantidade_desejada
    if 'historico_compras' not in oferta:
        oferta['historico_compras'] = []
    oferta['historico_compras'].append({
        'comprador_id': comprador_id,
        'quantidade': quantidade_desejada,
        'timestamp_aceite': int(time.time())
    })
    if nova_quantidade_disponivel <= 0.01:
        oferta['status'] = 'Removida'
        oferta['quantidade'] = "0.00"
    else:
        oferta['quantidade'] = str(nova_quantidade_disponivel)
    save_data(dados_ofertas, OFERTAS_FILE)
    return {
        'comprado': quantidade_desejada, 
        'restante': nova_quantidade_disponivel, 
        'status': oferta['status']
    }

def obter_historico_transacoes(user_id, user_tipo):
    dados_ofertas = load_data(OFERTAS_FILE)
    dados_usuarios = load_data(USUARIOS_FILE)
    historico = []
    for oferta_id, oferta in dados_ofertas.items():
        if 'historico_compras' in oferta and oferta['historico_compras']:
            gerador = dados_usuarios.get(oferta['gerador_id'], {'nome': 'Gerador Desconhecido'})
            for compra in oferta['historico_compras']:
                comprador = dados_usuarios.get(compra['comprador_id'], {'nome': 'Comprador Desconhecido'})
                compra_timestamp = compra.get('timestamp_aceite')
                if not compra_timestamp:
                    compra_timestamp = compra.get('timestamp')
                if compra_timestamp:
                    data_hora = datetime.datetime.fromtimestamp(compra_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    data_hora = "Data Indisponível"
                transacao = {
                    'oferta_id': oferta_id,
                    'titulo': oferta['titulo'],
                    'quantidade': compra['quantidade'],
                    'data': data_hora,
                }
                if user_tipo == 'Gerador' and oferta['gerador_id'] == user_id:
                    transacao['parceiro'] = comprador['nome']
                    transacao['tipo'] = 'Venda'
                    historico.append(transacao)
                elif user_tipo == 'Receptor' and compra['comprador_id'] == user_id:
                    transacao['parceiro'] = gerador['nome']
                    transacao['tipo'] = 'Compra'
                    historico.append(transacao)
    return historico

def obter_ofertas_otimizadas():
    ofertas_ativas = obter_todas_ofertas_ativas()
    def get_sort_key(oferta):
        try:
            return float(oferta.get('valor_de_venda', 999999.0)) 
        except ValueError:
            return 999999.0
    ofertas_otimizadas = sorted(ofertas_ativas, key=get_sort_key)
    return ofertas_otimizadas