from modelos import *
from persistencia import *

USUARIO_ATIVO = None

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
                USUARIO_ATIVO = simular_login()
            elif escolha == '4':
                print("Saindo do sistema!")
                break    
            elif escolha.startswith('pyenv') or escolha == '':
                continue
            else:
                print("❌ Opção inválida. Tente novamente.")
        
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
                    cadastrar_oferta(USUARIO_ATIVO)
                elif escolha == '2':
                    listar_minhas_ofertas_ativas(USUARIO_ATIVO)
                elif escolha == '3':
                    listar_minhas_ofertas_esgotadas(USUARIO_ATIVO)
                elif escolha == '4':
                    editar_oferta(USUARIO_ATIVO)
                elif escolha == '5':
                    excluir_oferta(USUARIO_ATIVO)
                elif escolha == '6':
                    historico_transacoes(USUARIO_ATIVO)
                elif escolha == '7':
                    USUARIO_ATIVO = None
                    print("✅ Logout realizado com sucesso.")
                else:
                    print("❌ Opção inválida. Tente novamente.")

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
                    buscar_oferta(USUARIO_ATIVO)
                elif escolha == '3':
                    comprar_oferta(USUARIO_ATIVO)
                elif escolha == '4': 
                    historico_transacoes(USUARIO_ATIVO)
                elif escolha == '5':
                    USUARIO_ATIVO = None
                    print("✅ Logout realizado com sucesso.")
            else: 
                USUARIO_ATIVO = None
                print("✅ Logout realizado com sucesso.")

if __name__ == "__main__":
    menu()
