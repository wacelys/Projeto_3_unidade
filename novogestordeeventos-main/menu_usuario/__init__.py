from eventos import *
from menu_adm import menu_adm
from estatisticas_financeiro import *


def menu_usuario(usuario):
    while True:
        print("\n--- Menu Usuário ---")
        print("1 - Participar de Evento")
        print("2 - Participar de Evento (Código)")
        print("3 - Buscar Eventos")
        print("4 - Listar Eventos")
        print("5 - Listar Eventos que Estou Inscrito")
        print("6 - Cancelar Inscrição")
        print("7 - Doar para um Evento")
        print("8 - Menu Administrativo")
        print("0 - Retornar ao Menu de Acesso")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            realizar_inscricao(usuario)
        elif opcao == '2':
            realizar_inscricao_por_codigo(usuario)
        elif opcao == '3':
            buscar_eventos()
        elif opcao == '4':
            listar_eventos()
        elif opcao == '5':
            listar_eventos_inscritos(usuario)
        elif opcao == '6':
            remover_inscricao(usuario)
        elif opcao == '7':
            realizar_doacao()
        elif opcao == '8':
            menu_adm(usuario)
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")
