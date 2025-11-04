import time
import datetime
import json
from persistencia import *

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

def obter_entrada_nao_vazia(mensagem: str) -> str:
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("❌ Este campo não pode ficar vazio. Tente novamente.")

def obter_entrada_numerica(mensagem: str, tipo=float):
    while True:
        try:
            valor = input(mensagem).strip()
            if not valor:
                raise ValueError
            
            numero = tipo(valor)
            if numero <= 0:
                print("❌ O valor deve ser positivo.")
                continue
            return numero
        except ValueError:
            print("❌ Entrada inválida. Digite um número válido e positivo.")

def cadastrar_usuario():
    print("\nCADASTRO DE NOVO USUÁRIO")
    
    nome = obter_entrada_nao_vazia("Nome completo: ").title()
    
    while True:
        tipo = input("Tipo (Gerador ou Receptor): ").strip().capitalize()
        if tipo in ['Gerador', 'Receptor']:
            break
        print("❌ Tipo inválido. Digite exatamente 'Gerador' ou 'Receptor'.")

    cidade = obter_entrada_nao_vazia("Localização/Cidade: ").title()
    
    try:
        novo = novo_usuario(nome, tipo, cidade)
        usuario_salvo = salvar_novo_usuario(novo)
        
        print("\n✅ Usuário cadastrado com sucesso!")
        print(f"ID: {usuario_salvo['id']}")
        print(f"Nome: {usuario_salvo['nome']}")
        print(f"Tipo: {usuario_salvo['tipo']}")
        print(f"Localização: {usuario_salvo['localizacao']}")
    except Exception as e:
        print(f"❌ Erro ao salvar usuário: {e}")

def listar_usuarios():
    print("\nLISTA DE USUÁRIOS CADASTRADOS")
    
    try:
        dados_usuarios = load_data(USUARIOS_FILE)
    except Exception as e:
        print(f"❌ Erro ao carregar usuários: {e}")
        return

    if not dados_usuarios:
        print("❌ Nenhum usuário cadastrado.")
        return

    for usuario_id, usuario in dados_usuarios.items():
        print(f"\nID: {usuario_id}")
        print(f"Nome: {usuario['nome']}")
        print(f"Tipo: {usuario['tipo']}")
        print(f"Localização: {usuario['localizacao']}")
        print("-" * 30)

def simular_login():
    dados_usuarios = load_data(USUARIOS_FILE)
    if not dados_usuarios:
        print("❌ Erro: Nenhum usuário cadastrado para logar.")
        return None

    listar_usuarios()
    
    user_input = input("Digite o ID ou Nome do usuário para 'logar' como ativo: ").strip()
    
    usuarios_encontrados = []
    
    for uid, usuario in dados_usuarios.items():
        if user_input == uid or user_input.lower() in usuario['nome'].lower():
            usuarios_encontrados.append(usuario)

    if len(usuarios_encontrados) == 1:
        usuario_logado = usuarios_encontrados[0]
        print(f"✅ Login simulado com sucesso! Bem-vindo(a), {usuario_logado['nome']}.")
        return usuario_logado
    elif len(usuarios_encontrados) > 1:
        print("\nForam encontrados múltiplos usuários. Qual deles você deseja usar?")
        for i, u in enumerate(usuarios_encontrados):
            print(f"{i + 1}. {u['nome']} (ID: {u['id']})")
        
        while True:
            try:
                escolha = int(input(f"Escolha um número (1-{len(usuarios_encontrados)}): "))
                if 1 <= escolha <= len(usuarios_encontrados):
                    usuario_logado = usuarios_encontrados[escolha - 1]
                    print(f"✅ Login simulado com sucesso! Bem-vindo(a), {usuario_logado['nome']}.")
                    return usuario_logado
            except (ValueError, IndexError):
                print("❌ Opção inválida. Tente novamente.")
    else:
        print("❌ Erro: ID de usuário não encontrado.")
        return None

def cadastrar_oferta(USUARIO_ATIVO):
    
    if USUARIO_ATIVO is None or USUARIO_ATIVO['tipo'] != 'Gerador':
        print("Apenas Geradores logados podem cadastrar ofertas.")
        return
        
    print("\nCADASTRAR NOVA OFERTA DE RESÍDUO")

    titulo = input("Título da Oferta: ").capitalize()
    descricao = input("Descrição: ").capitalize()
    quantidade = input("Quantidade Kg: ")
    valor_de_venda = input("Valor de venda por Kg (R$): ")
    
    cidade = USUARIO_ATIVO['localizacao']
    
    nova = nova_oferta(
        gerador_id=USUARIO_ATIVO['id'],
        titulo=titulo,
        descricao=descricao,
        quantidade=quantidade,
        cidade=cidade
    )
    nova['valor_de_venda'] = valor_de_venda

    oferta_salva = salvar_nova_oferta(nova)
    
    print("\n✅ Oferta cadastrada com sucesso!")
    print(f"ID da Oferta: {oferta_salva['id']}, Gerador ID: {oferta_salva['gerador_id']}")

def listar_ofertas():
    print("\nOFERTAS DE RESÍDUOS ATIVAS")
    
    dados_ofertas = load_data(OFERTAS_FILE)
    dados_usuarios = load_data(USUARIOS_FILE) 
    
    if not dados_ofertas:
        print("Nenhuma oferta ativa no momento.")
        return
    
    ofertas_ativas = {oid: oferta for oid, oferta in dados_ofertas.items() if oferta.get('status') == 'Ativa'}
    
    if not ofertas_ativas:
        print("Nenhuma oferta ativa no momento.")
        return
        
    for oferta_id, oferta in ofertas_ativas.items():
            gerador = dados_usuarios.get(oferta['gerador_id'], {'nome': 'Desconhecido'}) 
            print(f"[{oferta_id}] Título: {oferta['titulo']}")
            print(f"  > Gerador: {gerador['nome']} | Cidade: {oferta['localizacao']}")
            print(f"  > Qtd Kg: {oferta['quantidade']} | Valor de Venda Kg: R${oferta.get('valor_de_venda', 'N/A')}")

def editar_oferta(USUARIO_ATIVO):
    if USUARIO_ATIVO is None or USUARIO_ATIVO['tipo'] != 'Gerador':
        print("❌ Apenas Geradores logados podem editar ofertas.")
        return

    dados_ofertas = load_data(OFERTAS_FILE)
    
    minhas_ofertas = {oid: oferta for oid, oferta in dados_ofertas.items() 
    if oferta['gerador_id'] == USUARIO_ATIVO['id'] and oferta['status'] == 'Ativa'}
    
    if not minhas_ofertas:
        print("\nVocê não possui ofertas no momento!")
        return
    
    print("\nSUAS OFERTAS:")
    for oid, oferta in minhas_ofertas.items():
        print(f"\nID: {oid} (Status: {oferta['status']})")
        print(f"Título: {oferta['titulo']}")
        print(f"Descrição: {oferta['descricao']}")
        print(f"Quantidade: {oferta['quantidade']} Kg")
        print(f"Valor de venda: R$ {oferta['valor_de_venda']}/Kg")
        print(f"Status: {oferta['status']}")
        print("-" * 30)
    
    oferta_id = input("\nDigite o ID da oferta que deseja editar: ").strip()
    
    if oferta_id not in minhas_ofertas:
        print("❌ ID inválido ou oferta não encontrada.")
        return
    
    oferta = dados_ofertas[oferta_id]
    
    print("\nDeixe em branco para manter o valor atual")
    
    novo_titulo = input(f"Novo título [{oferta['titulo']}]: ").strip()
    if novo_titulo:
        oferta['titulo'] = novo_titulo
        
    nova_descricao = input(f"Nova descrição [{oferta['descricao']}]: ").strip()
    if nova_descricao:
        oferta['descricao'] = nova_descricao
        
    while True:
        nova_quantidade = input(f"Nova quantidade em Kg [{oferta['quantidade']}]: ").strip()
        if not nova_quantidade:
            break
        try:
            quantidade = float(nova_quantidade)
            if quantidade > 0:
                oferta['quantidade'] = str(quantidade)
                break
            print("❌ A quantidade deve ser maior que zero.")
        except ValueError:
            print("❌ Por favor, digite um número válido.")
            
    while True:
        novo_valor = input(f"Novo valor de venda por Kg [R$ {oferta['valor_de_venda']}]: ").strip()
        if not novo_valor:
            break
        try:
            valor = float(novo_valor)
            if valor >= 0:
                oferta['valor_de_venda'] = str(valor)
                break
            print("❌ O valor não pode ser negativo.")
        except ValueError:
            print("❌ Por favor, digite um número válido.")
    
    save_data(dados_ofertas, OFERTAS_FILE)
    print("\n✅ Oferta atualizada com sucesso!")
    if oferta['status'] == 'Removida' and float(oferta['quantidade']) > 0:
        confirmar_reativacao = input("Esta oferta estava 'Removida' por esgotamento. Deseja reativá-la? (S/N): ").strip().upper()
        if confirmar_reativacao == 'S':
            oferta['status'] = 'Ativa'
            save_data(dados_ofertas, OFERTAS_FILE)
            print("✅ Oferta reativada com sucesso!")

def excluir_oferta(USUARIO_ATIVO):
    if USUARIO_ATIVO is None or USUARIO_ATIVO['tipo'] != 'Gerador':
        print("❌ Apenas Geradores logados podem excluir ofertas.")
        return

    dados_ofertas = load_data(OFERTAS_FILE)

    minhas_ofertas = {oid: oferta for oid, oferta in dados_ofertas.items()
                     if oferta['gerador_id'] == USUARIO_ATIVO['id'] and
                     (oferta['status'] == 'Ativa' or oferta['status'] == 'Removida')}
    
    if not minhas_ofertas:
        print("\nVocê não possui ofertas no momento!")
        return
    
    print("\nSUAS OFERTAS ATIVAS:")
    for oid, oferta in minhas_ofertas.items():
        print(f"\nID: {oid}")
        print(f"Título: {oferta['titulo']}")
        print(f"Descrição: {oferta['descricao']}")
        print(f"Quantidade: {oferta['quantidade']} Kg")
        print(f"Valor de Venda: R$ {oferta['valor_de_venda']}/Kg")
        print(f"Status: {oferta['status']}")
        print("-" * 30)
    
    oferta_id = input("\nDigite o ID da oferta que deseja excluir: ").strip()
    
    if oferta_id not in minhas_ofertas:
        print("❌ ID inválido ou oferta não encontrada.")
        return
    
    oferta = dados_ofertas[oferta_id]
    
    if 'historico_compras' in oferta and oferta['historico_compras']:
        print("\n⚠️ Esta oferta possui histórico de compras:")
        print("\nHISTÓRICO DE COMPRAS:")
        dados_usuarios = load_data(USUARIOS_FILE)
        
        for compra in oferta['historico_compras']:
            comprador = dados_usuarios.get(compra['comprador_id'], {'nome': 'Usuário Desconhecido'})
            data_hora = datetime.datetime.fromtimestamp(compra['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            print(f"- Comprador: {comprador['nome']}")
            print(f"  Quantidade: {compra['quantidade']:.2f} Kg")
            print(f"  Data: {data_hora}")
            print("-" * 30)

        if oferta['status'] == 'Ativa':
            print("\n⚠️ ATENÇÃO: Por ter histórico de compras, a oferta será marcada como 'Removida' e manterá o histórico.")
        else: 
            print("\n⚠️ ATENÇÃO: Esta oferta já está 'Removida' e possui histórico. Ela será excluída permanentemente.")
    
    confirmacao = input("\nTem certeza que deseja excluir esta oferta? (S/N): ").strip().upper()
    if confirmacao != 'S':
        print("Operação cancelada.")
        return
    
    if oferta['status'] == 'Ativa' and 'historico_compras' in oferta and oferta['historico_compras']:
        oferta['status'] = 'Removida'
    else:
        del dados_ofertas[oferta_id]
    
    save_data(dados_ofertas, OFERTAS_FILE)
    print("\n✅ Oferta excluída com sucesso!")

def listar_minhas_ofertas_ativas(USUARIO_ATIVO):
    dados_ofertas = load_data(OFERTAS_FILE)
    minhas_ofertas = {oid: oferta for oid, oferta in dados_ofertas.items() 
                     if oferta['gerador_id'] == USUARIO_ATIVO['id'] and 
                     oferta['status'] == 'Ativa'}
    
    if not minhas_ofertas:
        print("\nVocê não possui ofertas ativas no momento!")
        return
    
    print("\nSUAS OFERTAS ATIVAS:")
    for oid, oferta in minhas_ofertas.items():
        print(f"\nID: {oid}")
        print(f"Título: {oferta['titulo']}")
        print(f"Descrição: {oferta['descricao']}")
        print(f"Quantidade: {oferta['quantidade']} Kg")
        print(f"Valor de venda: R$ {oferta['valor_de_venda']}/Kg")

def buscar_oferta(USUARIO_ATIVO):
    if USUARIO_ATIVO is None or USUARIO_ATIVO['tipo'] != 'Receptor':
        print("❌ Apenas usuários do tipo 'Receptor' podem buscar ofertas.")
        return
    
    dados_ofertas = load_data(OFERTAS_FILE)
    dados_usuarios = load_data(USUARIOS_FILE)
    
    ofertas_ativas = {oid: oferta for oid, oferta in dados_ofertas.items() if oferta.get('status') == 'Ativa'}
    
    if not ofertas_ativas:
        print("❌ Nenhuma oferta ativa no momento.")
        return
    
    print("\nBUSCA DE OFERTAS")
    palavra_chave = input("Digite uma palavra para buscar (ex: Borra, Casca, Polpa): ").strip().lower()
    
    if not palavra_chave:
        print("❌ É necessário digitar uma palavra para buscar.")
        return
    
    ofertas_encontradas = False
    print("\n" + "=" * 50)
    print(f"Resultados da busca por: '{palavra_chave}'")
    print("=" * 50)
    
    for oferta_id, oferta in ofertas_ativas.items():
        if (palavra_chave in oferta['titulo'].lower() or 
            palavra_chave in oferta['descricao'].lower()):
            
            ofertas_encontradas = True
            gerador = dados_usuarios.get(oferta['gerador_id'], {'nome': 'Desconhecido'})
            
            print(f"\n[{oferta_id}] {oferta['titulo']}")
            print(f"  > Gerador: {gerador['nome']} | Cidade: {oferta['localizacao']}")
            print(f"  > Descrição: {oferta['descricao']}")
            print(f"  > Quantidade: {oferta['quantidade']} Kg")
            print(f"  > Valor de Venda: R$ {oferta.get('valor_de_venda', 'N/A')}/Kg")
            print("-" * 50)
    
    if not ofertas_encontradas:
        print(f"Nenhuma oferta encontrada contendo '{palavra_chave}'.")
        return
    
    print("\nDeseja comprar alguma dessas ofertas?")
    resposta = input("Digite o ID da oferta para comprar ou Enter para voltar: ").strip()
    
    if resposta:
        if resposta in ofertas_ativas:
            comprar_oferta_especifica(resposta, USUARIO_ATIVO)
        else:
            print("❌ ID de oferta inválido.")

def comprar_oferta_especifica(oferta_id, USUARIO_ATIVO):
    dados_ofertas = load_data(OFERTAS_FILE)
    
    if oferta_id not in dados_ofertas or dados_ofertas[oferta_id]['status'] != 'Ativa':
        print("❌ Oferta não encontrada ou não está mais ativa.")
        return
        
    oferta = dados_ofertas[oferta_id]
    try:
        quantidade_disponivel = float(oferta['quantidade'])
    except ValueError:
        print("❌ Erro: Quantidade da oferta está em formato inválido.")
        return

    print(f"\nDisponível para compra: {quantidade_disponivel:.2f} Kg.")
    quantidade_desejada = obter_entrada_numerica("Quantos Kg você deseja comprar? ", tipo=float)

    if quantidade_desejada > quantidade_disponivel:
        print(f"❌ Erro: Quantidade solicitada ({quantidade_desejada:.2f} Kg) excede o saldo disponível.")
        return

    nova_quantidade_disponivel = quantidade_disponivel - quantidade_desejada
    
    if 'historico_compras' not in oferta:
        oferta['historico_compras'] = []
        
    oferta['historico_compras'].append({
        'comprador_id': USUARIO_ATIVO['id'],
        'quantidade': quantidade_desejada,
        'timestamp': int(time.time())
    })
    
    if nova_quantidade_disponivel <= 0.01: 
        oferta['status'] = 'Removida' 
        oferta['quantidade'] = "0.00" 
        save_data(dados_ofertas, OFERTAS_FILE)
        print(f"\n✅ Compra realizada com sucesso!")
        print(f"   Quantidade Comprada: {quantidade_desejada:.2f} Kg")
        print("⚠️ Último lote comprado.")
        return 
    else:
        oferta['quantidade'] = str(nova_quantidade_disponivel)

    save_data(dados_ofertas, OFERTAS_FILE)
    
    print(f"\n✅ Compra realizada com sucesso!")
    print(f"   Quantidade Comprada: {quantidade_desejada:.2f} Kg")
    print(f"   Quantidade Restante: {nova_quantidade_disponivel:.2f} Kg")

def comprar_oferta(USUARIO_ATIVO):
    if USUARIO_ATIVO is None or USUARIO_ATIVO['tipo'] != 'Receptor':
        print("❌ Apenas usuários do tipo 'Receptor' podem comprar ofertas.")
        return

    listar_ofertas()
    
    dados_ofertas = load_data(OFERTAS_FILE)
    
    ofertas_ativas = {oid: oferta for oid, oferta in dados_ofertas.items() if oferta.get('status') == 'Ativa'}
    if not ofertas_ativas:
        print("❌ Nenhuma oferta ativa para comprar no momento.")
        return 

    oferta_id = input("Digite o ID da oferta que deseja comprar: ").strip()

    if oferta_id in ofertas_ativas:
        comprar_oferta_especifica(oferta_id, USUARIO_ATIVO)
    else:
        print("❌ ID da oferta inválido ou a oferta não está mais ativa.")

def historico_transacoes(USUARIO_ATIVO):
    if USUARIO_ATIVO is None:
        print("❌ Você precisa estar logado para ver o histórico.")
        return

    user_id = USUARIO_ATIVO['id']
    user_tipo = USUARIO_ATIVO['tipo']

    print(f"\nHISTÓRICO DE TRANSAÇÕES ({USUARIO_ATIVO['nome']})")

    try:
        dados_ofertas = load_data(OFERTAS_FILE)
        dados_usuarios = load_data(USUARIOS_FILE)
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return

    if user_tipo == 'Gerador':
        print("\n[ITENS VENDIDOS POR VOCÊ]")
        vendas_encontradas = False
        
        for oferta_id, oferta in dados_ofertas.items():
            if oferta['gerador_id'] == user_id:
                vendas_encontradas = True
                
                print(f"\nOferta ID {oferta_id}: {oferta['titulo']} (Saldo Atual: {oferta['quantidade']} Kg)")
                
                if 'historico_compras' in oferta and oferta['historico_compras']:
                    print("  DETALHES DAS VENDAS:")
                    for compra in oferta['historico_compras']:
                        comprador = dados_usuarios.get(compra['comprador_id'], {'nome': 'Usuário Desconhecido'})
                        
                        data_hora = datetime.datetime.fromtimestamp(compra['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                        
                        print(f"    - Venda: {comprador['nome']} | Qtd: {compra['quantidade']:.2f} Kg | Data: {data_hora}")
                else:
                    print("  Nenhuma venda registrada nesta oferta ainda.")
        
        if not vendas_encontradas:
            print("Nenhuma oferta registrada por você possui histórico de vendas.")

    elif user_tipo == 'Receptor':
        print("\n[ITENS COMPRADOS POR VOCÊ]")
        compras_encontradas = False
        
        for oferta_id, oferta in dados_ofertas.items():
            if 'historico_compras' in oferta and oferta['historico_compras']:
                gerador = dados_usuarios.get(oferta['gerador_id'], {'nome': 'Gerador Desconhecido'})
                
                for compra in oferta['historico_compras']:
                    if compra['comprador_id'] == user_id:
                        compras_encontradas = True
                        
                        data_hora = datetime.datetime.fromtimestamp(compra['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                        
                        print(f"Compra na Oferta ID {oferta_id}")
                        print(f"  > Título: {oferta['titulo']}")
                        print(f"  > Gerador: {gerador['nome']} | Qtd Comprada: {compra['quantidade']:.2f} Kg | Data: {data_hora}")

        if not compras_encontradas:
            print("Nenhuma compra registrada ainda.")
