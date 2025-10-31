from modelos import *
from persistencia import *
import time
import datetime
import json

USUARIO_ATIVO = None

def obter_entrada_nao_vazia(mensagem: str) -> str:
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("🚫 Este campo não pode ficar vazio. Tente novamente.")

def obter_entrada_numerica(mensagem: str, tipo=float):
    while True:
        try:
            valor = input(mensagem).strip()
            if not valor:
                raise ValueError
            
            numero = tipo(valor)
            if numero <= 0:
                print("🚫 O valor deve ser positivo.")
                continue
            return numero
        except ValueError:
            print("🚫 Entrada inválida. Digite um número válido e positivo.")

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
        print("🚫 Nenhum usuário cadastrado.")
        return

    for usuario_id, usuario in dados_usuarios.items():
        print(f"\nID: {usuario_id}")
        print(f"Nome: {usuario['nome']}")
        print(f"Tipo: {usuario['tipo']}")
        print(f"Localização: {usuario['localizacao']}")
        print("-" * 30)

def simular_login():
    global USUARIO_ATIVO
    
    dados_usuarios = load_data(USUARIOS_FILE)
    if not dados_usuarios:
        print("❌ Erro: Nenhum usuário cadastrado para logar.")
        return
        
    listar_usuarios()
    
    user_input = input("Digite o ID ou Nome do usuário para 'logar' como ativo: ").strip()
    
    usuarios_encontrados = []
    
    for uid, usuario in dados_usuarios.items():
        if user_input == uid or user_input.lower() in usuario['nome'].lower():
            usuarios_encontrados.append(usuario)

    if len(usuarios_encontrados) == 1:
        USUARIO_ATIVO = usuarios_encontrados[0]
        print(f"✅ Login simulado com sucesso! Bem-vindo(a), {USUARIO_ATIVO['nome']}.")
    elif len(usuarios_encontrados) > 1:
        print("\nForam encontrados múltiplos usuários. Qual deles você deseja usar?")
        for i, u in enumerate(usuarios_encontrados):
            print(f"{i + 1}. {u['nome']} (ID: {u['id']})")
        
        while True:
            try:
                escolha = int(input(f"Escolha um número (1-{len(usuarios_encontrados)}): "))
                if 1 <= escolha <= len(usuarios_encontrados):
                    USUARIO_ATIVO = usuarios_encontrados[escolha - 1]
                    print(f"✅ Login simulado com sucesso! Bem-vindo(a), {USUARIO_ATIVO['nome']}.")
                    break
            except (ValueError, IndexError):
                print("🚫 Opção inválida. Tente novamente.")
    else:
        print("❌ Erro: ID de usuário não encontrado.")

def cadastrar_oferta():
    global USUARIO_ATIVO
    
    if USUARIO_ATIVO is None or USUARIO_ATIVO['tipo'] != 'Gerador':
        print("Apenas Geradores logados podem cadastrar ofertas.")
        return
        
    print("\nCADASTRAR NOVA OFERTA DE RESÍDUO")
    
    titulo = input("Título da Oferta: ")
    descricao = input("Descrição: ")
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
        
    for oferta_id, oferta in dados_ofertas.items():
        if oferta.get('status') == 'Ativa':
            gerador = dados_usuarios.get(oferta['gerador_id'], {'nome': 'Desconhecido'}) 
            print(f"[{oferta_id}] Título: {oferta['titulo']}")
            print(f"  > Gerador: {gerador['nome']} | Cidade: {oferta['localizacao']}")
            print(f"  > Qtd Kg: {oferta['quantidade']} | Valor de Venda Kg: R${oferta.get('valor_de_venda', 'N/A')}")

def editar_oferta():
    global USUARIO_ATIVO
    
    if USUARIO_ATIVO is None or USUARIO_ATIVO['tipo'] != 'Gerador':
        print("❌ Apenas Geradores logados podem editar ofertas.")
        return

    dados_ofertas = load_data(OFERTAS_FILE)
    
    minhas_ofertas = {oid: oferta for oid, oferta in dados_ofertas.items() 
    if oferta['gerador_id'] == USUARIO_ATIVO['id'] and (oferta['status'] == 'Ativa' or oferta['status'] == 'Esgotada')}
    
    if not minhas_ofertas:
        print("\nVocê não possui ofertas no momento!")
        return
    
    print("\nSUAS OFERTAS:")
    for oid, oferta in minhas_ofertas.items():
        print(f"\nID: {oid}")
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
    
    if oferta['status'] == 'Esgotada':
        reativar = input("\nDeseja reativar esta oferta? (S/N): ").strip().upper()
        if reativar == 'S':
            while True:
                nova_quantidade = input("Digite a nova quantidade disponível em Kg: ").strip()
                try:
                    quantidade = float(nova_quantidade)
                    if quantidade > 0:
                        oferta['quantidade'] = str(quantidade)
                        oferta['status'] = 'Ativa'
                        print("\n✅ Oferta reativada com sucesso!")
                        break
                    print("❌ A quantidade deve ser maior que zero.")
                except ValueError:
                    print("❌ Por favor, digite um número válido.")
    
    save_data(dados_ofertas, OFERTAS_FILE)
    print("\n✅ Oferta atualizada com sucesso!")

def excluir_oferta():
    global USUARIO_ATIVO
    
    if USUARIO_ATIVO is None or USUARIO_ATIVO['tipo'] != 'Gerador':
        print("❌ Apenas Geradores logados podem excluir ofertas.")
        return

    dados_ofertas = load_data(OFERTAS_FILE)

    minhas_ofertas = {oid: oferta for oid, oferta in dados_ofertas.items() 
                     if oferta['gerador_id'] == USUARIO_ATIVO['id'] and 
                     (oferta['status'] == 'Ativa' or oferta['status'] == 'Esgotada')}
    
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
            
        print("\n⚠️ ATENÇÃO: Por ter histórico de compras, a oferta será marcada como 'Removida' e manterá o histórico.")
    
    confirmacao = input("\nTem certeza que deseja excluir esta oferta? (S/N): ").strip().upper()
    if confirmacao != 'S':
        print("Operação cancelada.")
        return
    
    if 'historico_compras' in oferta and oferta['historico_compras']:
        oferta['status'] = 'Removida'
    else:
        del dados_ofertas[oferta_id]
    
    save_data(dados_ofertas, OFERTAS_FILE)
    print("\n✅ Oferta excluída com sucesso!")

def listar_minhas_ofertas_ativas():
    global USUARIO_ATIVO
    
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

def listar_minhas_ofertas_esgotadas():
    global USUARIO_ATIVO
    
    dados_ofertas = load_data(OFERTAS_FILE)
    minhas_ofertas = {oid: oferta for oid, oferta in dados_ofertas.items() 
                     if oferta['gerador_id'] == USUARIO_ATIVO['id'] and 
                     oferta['status'] == 'Esgotada'}
    
    if not minhas_ofertas:
        print("\nVocê não possui ofertas esgotadas no momento!")
        return
    
    print("\nSUAS OFERTAS ESGOTADAS:")
    for oid, oferta in minhas_ofertas.items():
        print(f"\nID: {oid}")
        print(f"Título: {oferta['titulo']}")
        print(f"Descrição: {oferta['descricao']}")
        print(f"Quantidade: {oferta['quantidade']} Kg")
        print(f"Valor de venda: R$ {oferta['valor_de_venda']}/Kg")

def minhas_ofertas():
    global USUARIO_ATIVO
    
    if USUARIO_ATIVO is None or USUARIO_ATIVO['tipo'] != 'Gerador':
        print("\nAcesso negado! Apenas Geradores podem acessar suas ofertas.")
        return

    while True:
        print("\nGERENCIAMENTO DE OFERTAS")
        print("1. Listar Ofertas Ativas")
        print("2. Listar Ofertas Esgotadas")
        print("3. Editar uma Oferta")
        print("4. Excluir uma Oferta")
        print("5. Voltar ao Menu Principal")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            listar_minhas_ofertas_ativas()
        elif opcao == '2':
            listar_minhas_ofertas_esgotadas()
        elif opcao == '3':
            editar_oferta()
        elif opcao == '4':
            excluir_oferta()
        elif opcao == '5':
            break
        else:
            print("\nOpção inválida! Por favor, tente novamente.")

def buscar_oferta():
    global USUARIO_ATIVO
    
    if USUARIO_ATIVO is None or USUARIO_ATIVO['tipo'] != 'Receptor':
        print("❌ Apenas usuários do tipo 'Receptor' podem buscar ofertas.")
        return
    
    dados_ofertas = load_data(OFERTAS_FILE)
    dados_usuarios = load_data(USUARIOS_FILE)
    
    ofertas_ativas = {oid: oferta for oid, oferta in dados_ofertas.items() if oferta.get('status') == 'Ativa'}
    
    if not ofertas_ativas:
        print("🚫 Nenhuma oferta ativa no momento.")
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
            comprar_oferta_especifica(resposta)
        else:
            print("❌ ID de oferta inválido.")

def comprar_oferta_especifica(oferta_id):
    global USUARIO_ATIVO
    
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
    
    oferta['quantidade'] = str(nova_quantidade_disponivel) 
    
    if nova_quantidade_disponivel <= 0.01: 
        oferta['status'] = 'Esgotada'
        print("⚠️ Último lote comprado. A oferta foi marcada como 'Esgotada'.")
        
    if 'historico_compras' not in oferta:
        oferta['historico_compras'] = []
        
    oferta['historico_compras'].append({
        'comprador_id': USUARIO_ATIVO['id'],
        'quantidade': quantidade_desejada,
        'timestamp': int(time.time())
    })

    save_data(dados_ofertas, OFERTAS_FILE)
    
    print(f"\n✅ Compra realizada com sucesso!")
    print(f"   Quantidade Comprada: {quantidade_desejada:.2f} Kg")
    print(f"   Quantidade Restante: {nova_quantidade_disponivel:.2f} Kg")

def comprar_oferta():
    global USUARIO_ATIVO
    if USUARIO_ATIVO is None or USUARIO_ATIVO['tipo'] != 'Receptor':
        print("❌ Apenas usuários do tipo 'Receptor' podem comprar ofertas.")
        return

    listar_ofertas()
    
    dados_ofertas = load_data(OFERTAS_FILE)
    
    ofertas_ativas = {oid: oferta for oid, oferta in dados_ofertas.items() if oferta.get('status') == 'Ativa'}
    if not ofertas_ativas:
        print("🚫 Nenhuma oferta ativa para comprar no momento.")
        return 

    oferta_id = input("Digite o ID da oferta que deseja comprar: ").strip()

    if oferta_id in ofertas_ativas:
        comprar_oferta_especifica(oferta_id)
    else:
        print("❌ ID da oferta inválido ou a oferta não está mais ativa.")

def historico_transacoes():
    global USUARIO_ATIVO
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

def menu():
    global USUARIO_ATIVO 
    
    while True:        
        if USUARIO_ATIVO is None:
            print("\nCIRCULAR FOOD CONNECT - DESLOGADO")
            print("1. Cadastrar Novo Usuário")
            print("2. Listar Usuários")
            print("3. Login")
            print("4. Sair")

            escolha = input("Escolha uma opção: ").strip()
            
            if escolha == '1':
                cadastrar_usuario()
            elif escolha == '2':
                listar_usuarios()
            elif escolha == '3':
                simular_login()
            elif escolha == '4':
                print("Saindo do sistema!")
                break    
            elif escolha.startswith('pyenv') or escolha == '':
                continue
            else:
                print("🚫 Opção inválida. Tente novamente.")
        
        else: 
            print(f"\nLogado como: {USUARIO_ATIVO['nome']} ({USUARIO_ATIVO['tipo']})")
            
            if USUARIO_ATIVO['tipo'] == 'Gerador':
                print("1. Cadastrar Nova Oferta") 
                print("2. Listar Ofertas Ativas")
                print("3. Listar Ofertas Esgotadas")
                print("4. Editar uma Oferta")
                print("5. Excluir uma Oferta")
                print("6. Visualizar Histórico de Vendas") 
                print("7. Fazer Logout") 
                
                escolha = input("Escolha uma opção: ").strip()

                if escolha == '1':
                    cadastrar_oferta()
                elif escolha == '2':
                    listar_minhas_ofertas_ativas()
                elif escolha == '3':
                    listar_minhas_ofertas_esgotadas()
                elif escolha == '4':
                    editar_oferta()
                elif escolha == '5':
                    excluir_oferta()
                elif escolha == '6':
                    historico_transacoes()
                elif escolha == '7':
                    USUARIO_ATIVO = None
                    print("✅ Logout realizado com sucesso.")
                else:
                    print("🚫 Opção inválida. Tente novamente.")

            elif USUARIO_ATIVO['tipo'] == 'Receptor':
                print("1. Listar Ofertas Ativas")
                print("2. Buscar Ofertas")
                print("3. Comprar Oferta")
                print("4. Visualizar Histórico de Compras") 
                print("5. Fazer Logout") 
                
                escolha = input("Escolha uma opção: ").strip()
                if escolha == '1':
                    listar_ofertas()
                elif escolha == '2':
                    buscar_oferta()
                elif escolha == '3':
                    comprar_oferta()
                elif escolha == '4': 
                    historico_transacoes()
                elif escolha == '5':
                    USUARIO_ATIVO = None
                    print("✅ Logout realizado com sucesso.")
            else: 
                USUARIO_ATIVO = None
                print("✅ Logout realizado com sucesso.")

if __name__ == "__main__":
    menu()
