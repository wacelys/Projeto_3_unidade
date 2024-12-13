from eventos import *
from estatisticas_financeiro import *


def menu_adm(usuario):

    while True:
        print("\n--- Menu Administrativo ---")
        print("1 - Cadastrar Evento")
        print("2 - Deletar Evento")
        print("3 - Listar Participantes do Evento")
        print("4 - Area Financeira / Estatisticas")
        print("5 - Exibir Detalhes dos Seus Eventos")
        print("6 - Cadastrar Cupom de Desconto")
        print("7 - Gerenciar a lista de indesejados de seu evento")
        print("8 - Inscrever participante manualmente")
        print("9 - Deletar inscrição de usuario em seu evento")
        print("0 - Retornar ao Menu Usuario")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_evento(usuario)
        elif opcao == '2':
            deletar_evento(usuario)
        elif opcao == '3':
            listar_participantes_evento(usuario)
        elif opcao == '4':
            while True:
                print('1 - Vizualizar Estatísticas Financeiras do evento')
                print('2 - Vizualizar Estatísticas Quantitativas do Evento')
                print('3 - Vizualizar Estatísticas Sobre Gênero, Idade e Estado')
                print('0 - Voltar ao menu administrativo')
                opcao = input("Escolha uma opção: ")
                if opcao == '1':
                    verificar_valor_arrecadado(usuario)
                elif opcao == '2':
                    estatisticas_inscritos(usuario)
                elif opcao == '3':
                    obter_e_gerar_grafico_estatisticas_avancadas(usuario)
                elif opcao == '0':
                    break
        elif opcao == '5':
            exibir_detalhes_evento(usuario)
        elif opcao == '6':
            capturar_infos_cupom(usuario)
        elif opcao == '7':
            while True:
                print('1 - Adicionar usuarios na lista de indesejados de seu evento')
                print('2 - Remover usuarios da lista de indesejados de seu evento ')
                print('3 - Exibir a lista de indesejados de seu evento')
                print('0 - Voltar ao menu administrativo')
                opcao = input("Escolha uma opção: ")
                if opcao == '1':
                    adicionar_blacklist(usuario)
                elif opcao == '2':
                    remover_blacklist(usuario)
                elif opcao == '3':
                    listar_blacklist(usuario)
                elif opcao == '0':
                    break
        elif opcao == '8':
            inscrever_participante(usuario)
        elif opcao == '9':
            deletar_inscricao(usuario)
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")
