def novo_usuario(nome, tipo, cidade):
    return {
        'id': None,  
        'nome': nome,
        'tipo': tipo, 
        'localizacao': cidade,
        'reputacao': 0.0, 
        'ofertas_ativas': 0
    }

def nova_oferta(gerador_id, titulo, descricao, quantidade, cidade):
    return {
        'id': None,  
        'gerador_id': gerador_id,
        'titulo': titulo,
        'descricao': descricao,
        'quantidade': quantidade, 
        'localizacao': cidade,
        'laudo_link': None, 
        'status': 'Ativa', 
        'timestamp_cadastro': None
    }