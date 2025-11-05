import time
import datetime
from persistencia import *
from modelos import *

def obter_todos_usuarios():
    dados_usuarios = load_data(USUARIOS_FILE)
    return list(dados_usuarios.values())

def obter_usuario_por_credencial(input_busca):
    dados_usuarios = load_data(USUARIOS_FILE)
    usuarios_encontrados = []
    for usuario in dados_usuarios.values():
        if input_busca == usuario['id'] or input_busca.lower() in usuario['nome'].lower():
            usuarios_encontrados.append(usuario)           
    if len(usuarios_encontrados) == 1:
        return usuarios_encontrados[0]        
    return None

def criar_usuario_servico(nome, tipo, cidade):
    if tipo not in ['Gerador', 'Receptor']:
        raise ValueError("Tipo de usuário inválido.")    
    novo = novo_usuario(nome, tipo, cidade)
    return salvar_novo_usuario(novo)

def obter_todas_ofertas_ativas():
    dados_ofertas = load_data(OFERTAS_FILE)
    ofertas_ativas = [oferta for oferta in dados_ofertas.values() if oferta.get('status') == 'Ativa']
    return ofertas_ativas

def obter_oferta_por_id(oferta_id):
    dados_ofertas = load_data(OFERTAS_FILE)
    return dados_ofertas.get(oferta_id)

def criar_oferta_servico(gerador_id, titulo, descricao, quantidade, valor_de_venda, cidade):
    if not all([titulo, descricao, quantidade, valor_de_venda]):
        raise ValueError("Campos obrigatórios faltando.")
    nova = nova_oferta(
        gerador_id=gerador_id,
        titulo=titulo,
        descricao=descricao,
        quantidade=str(quantidade),
        cidade=cidade
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
        'timestamp': int(time.time())
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
                data_hora = datetime.datetime.fromtimestamp(compra['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                transacao = {
                    'oferta_id': oferta_id,
                    'titulo': oferta['titulo'],
                    'quantidade': compra['quantidade'],
                    'data': data_hora
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