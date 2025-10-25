from modelos import *
from persistencia import *
import json

USUARIOS_FILE = "usuarios.json"  

def obter_entrada_nao_vazia(mensagem: str) -> str:
    """Obtém uma entrada do usuário que não pode ser vazia."""
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Este campo não pode ficar vazio. Tente novamente.")

def cadastrar_usuario():
    print("\n--- CADASTRO DE NOVO USUÁRIO ---")
    
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
    print("\n--- LISTA DE USUÁRIOS CADASTRADOS ---")
    
    try:
        dados_usuarios = load_data(USUARIOS_FILE)
    except Exception as e:
        print(f"❌ Erro ao carregar usuários: {e}")
        return

    if not dados_usuarios:
        print("Nenhum usuário cadastrado.")
        return

    for usuario_id, usuario in dados_usuarios.items():
        print(f"\nID: {usuario_id}")
        print(f"Nome: {usuario['nome']}")
        print(f"Tipo: {usuario['tipo']}")
        print(f"Localização: {usuario['localizacao']}")
        print("-" * 30)

def menu():
    while True:
        print("\n🍽️  CIRCULAR FOOD CONNECT")
        print("1. Cadastrar Novo Usuário")
        print("2. Listar Usuários")
        print("3. Sair")
        
        escolha = input("\nEscolha uma opção: ").strip()
        
        if escolha == '1':
            cadastrar_usuario()
        elif escolha == '2':
            listar_usuarios()
        elif escolha == '3':
            print("\n👋 Saindo do sistema. Até logo!")
            break
        else:
            print("\n⚠️  Opção inválida. Por favor, escolha 1, 2 ou 3.")

if __name__ == "__main__":
    menu()
