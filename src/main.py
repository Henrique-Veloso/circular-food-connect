from modelos import *
from persistencia import *
import json 

def cadastrar_usuario():
    print("\n--- CADASTRO DE NOVO USUÁRIO ---")
    nome = input("Nome completo: ")
    
    while True:
        tipo = input("Tipo (Gerador ou Receptor): ").strip().capitalize()
        if tipo in ['Gerador', 'Receptor']:
            break
        print("Tipo inválido. Digite 'Gerador' ou 'Receptor'.")

    cidade = input("Localização/Cidade: ").strip()
    
    novo = novo_usuario(nome, tipo, cidade)
    usuario_salvo = salvar_novo_usuario(novo)
    
    print("\n✅ Usuário cadastrado com sucesso!")
    print(f"ID: {usuario_salvo['id']}, Nome: {usuario_salvo['nome']}, Tipo: {usuario_salvo['tipo']}")
    
def listar_usuarios():
    print("\n--- LISTA DE USUÁRIOS CADASTRADOS ---")
    
    dados_usuarios = load_data(USUARIOS_FILE)
    
    if not dados_usuarios:
        print("Nenhum usuário cadastrado.")
        return

    for usuario_id, usuario in dados_usuarios.items():
        print(f"[{usuario_id}] {usuario['nome']} ({usuario['tipo']})")
        print(f"Localização: {usuario['localizacao']}")

def menu():

    while True:
        print("\nCIRCULAR FOOD CONNECT")
        print("1. Cadastrar Novo Usuário")
        print("2. Listar Usuários")
        print("3. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            cadastrar_usuario()
        elif escolha == '2':
            listar_usuarios()
        elif escolha == '3':
            print("Saindo do sistema. Até a próxima Sprint!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()