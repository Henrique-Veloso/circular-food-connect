def novo_usuario(nome, tipo, cidade, email, senha):
    return {
        'nome': nome,
        'email': email,
        'senha': senha,
        'tipo': tipo,
        'localizacao': cidade,
        'reputacao': 0.0,
        'ofertas_ativas': 0
    }

def nova_oferta(gerador_id, titulo, descricao, quantidade, cidade):
    return {
        'gerador_id': gerador_id,
        'titulo': titulo,
        'descricao': descricao,
        'quantidade': quantidade,
        'localizacao': cidade,
        'laudo_link': None,
        'status': 'Ativa',
        'timestamp_cadastro': None
    }