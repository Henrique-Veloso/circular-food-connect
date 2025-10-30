from modelos import *
from persistencia import *
import json

USUARIO_ATIVO = None

def obter_entrada_nao_vazia(mensagem: str) -> str:
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("🚫 Este campo não pode ficar vazio. Tente novamente.")

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

def comprar_oferta():
    global USUARIO_ATIVO
    if USUARIO_ATIVO is None or USUARIO_ATIVO['tipo'] != 'Receptor':
        print("❌ Apenas usuários do tipo 'Receptor' podem comprar ofertas.")
        return

    listar_ofertas()
    
    dados_ofertas = load_data(OFERTAS_FILE)
    if not any(o['status'] == 'Ativa' for o in dados_ofertas.values()):
        return 

    oferta_id = input("Digite o ID da oferta que deseja comprar: ").strip()

    if oferta_id in dados_ofertas and dados_ofertas[oferta_id]['status'] == 'Ativa':
        dados_ofertas[oferta_id]['status'] = 'Vendida'
        dados_ofertas[oferta_id]['comprador_id'] = USUARIO_ATIVO['id']
        save_data(dados_ofertas, OFERTAS_FILE)
        print(f"\n✅ Parabéns! Você comprou a oferta '{dados_ofertas[oferta_id]['titulo']}'.")
    else:
        print("❌ ID da oferta inválido ou a oferta não está mais ativa.")

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
                print("3. Fazer Logout")
                
                escolha = input("Escolha uma opção: ").strip()

                if escolha == '1':
                    cadastrar_oferta()
                elif escolha == '2':
                    listar_ofertas()
                elif escolha == '3':
                    USUARIO_ATIVO = None
                    print("✅ Logout realizado com sucesso.")
                else:
                    print("🚫 Opção inválida. Tente novamente.")

            elif USUARIO_ATIVO['tipo'] == 'Receptor':
                print("1. Listar Ofertas Ativas")
                print("2. Comprar Oferta")
                print("3. Fazer Logout")
                escolha = input("Escolha uma opção: ").strip()
                if escolha == '1':
                    listar_ofertas()
                elif escolha == '2':
                    comprar_oferta()
                elif escolha == '3':
                    USUARIO_ATIVO = None
                    print("✅ Logout realizado com sucesso.")
            else: 
                USUARIO_ATIVO = None
                print("✅ Logout realizado com sucesso.")

if __name__ == "__main__":
    menu()
