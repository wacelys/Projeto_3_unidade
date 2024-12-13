from dao import *
import datetime
from auth import *
import random
import json


def cadastrar_evento(usuario):
    """
    Função para cadastrar um novo evento. Responsável apenas por coletar os dados e chamar as funções DAO.

    Args:
        usuario (list): Informações do usuário logado.
    """
    # Coletar e validar o nome do evento
    while True:
        nome_evento = input('Digite o nome do evento: ')
        if verificar_evento_existe(nome_evento):
            print("Já existe um evento com esse nome. Por favor, insira um nome diferente.")
        else:
            break

    # Coletar as demais informações do evento
    descricao = input('Insira a descrição do evento: ')

    while True:
        data_evento = input('Insira a data do evento no formato DD/MM/YYYY: ')
        try:
            data_evento = datetime.datetime.strptime(data_evento, '%d/%m/%Y').date()
            if data_evento < datetime.date.today():
                print("A data não pode ser no passado. Insira uma data futura.")
            else:
                break
        except ValueError:
            print("Formato de data inválido. Tente novamente.")

    local = input('Insira o local do evento: ')
    valor = float(input('Digite o valor da inscrição: '))

    # Cancelamento permitido (S/N)
    while True:
        cancelavel = input('Você deseja permitir o cancelamento de inscrições em seu evento? (S/N): ').upper()
        if cancelavel in ['S', 'N']:
            break
        print("Insira apenas 'S' ou 'N'.")

    idademinima = int(input('Insira a idade mínima para participar de seu evento: '))

    # Evento aberto para inscrições (s/n)
    aberto = input('Este evento estará aberto para inscrições? (s/n): ').lower()
    if aberto == 'n':
        aberto = False
    else:
        aberto = True

    # Gerar código de inscrição aleatório
    codigo_inscricao = random.randint(100000, 999999)

    # Montar dados do evento para envio ao DAO
    dados_evento = (
        nome_evento,
        descricao,
        data_evento,
        local,
        valor,
        cancelavel,
        idademinima,
        datetime.datetime.now(),
        usuario[0][0],  # ID ou nome do criador
        aberto,
        codigo_inscricao
    )
    print(dados_evento)

    # Inserir evento no banco de dados
    if inserir_evento(dados_evento):
        print(f"Evento cadastrado com sucesso! Código de inscrição: {codigo_inscricao}")
    else:
        print("Erro ao cadastrar o evento. Tente novamente.")


def buscar_eventos():
    # function02

    nome_evento = input('Insira o nome do evento que deseja buscar: ')

    conexao = conectardb()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT * 
            FROM eventos 
            WHERE nome_evento = %s AND aberto = TRUE
        """, (nome_evento,))
        resultado = cursor.fetchall()

        if resultado:
            for evento in resultado:
                evento_formatado = {
                    "ID do Evento": evento[0],
                    "Nome do Evento": evento[1],
                    "Descrição": evento[2],
                    "Criador do Evento": evento[9],
                    "Data do Evento": evento[3].strftime("%d/%m/%Y"),
                    "Local do Evento": evento[4],
                    "Valor da Inscrição": float(evento[10]),
                    "Cancelável": "Sim" if evento[6] == 'S' else "Não",
                    "Idade Mínima": evento[13] if evento[13] else "Não especificada",
                    "Código de inscrição do Evento": evento[15]
                }

                print("\n--- Detalhes do Evento ---")
                for chave, valor in evento_formatado.items():
                    print(f"{chave}: {valor}")
        else:
            print("Nenhum evento encontrado com esse nome ou o evento não está aberto ao público.")

    except Exception as e:
        print(f"Erro ao buscar eventos: {e}")

    finally:
        cursor.close()
        conexao.close()


def listar_eventos():
    # function03

    conexao = conectardb()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT * 
            FROM eventos 
            WHERE aberto = TRUE
        """)
        resultados = cursor.fetchall()

        if resultados:
            print("\n--- Lista de Eventos ---")
            for evento in resultados:
                evento_formatado = {
                    "ID do evento": evento[0],
                    "Nome do Evento": evento[1],
                    "Descrição": evento[2],
                    "Criador do Evento": evento[9],
                    "Data do Evento": evento[3].strftime("%d/%m/%Y"),
                    "Local do Evento": evento[4],
                    "Valor da Inscrição": float(evento[5]),
                    "Cancelável": "Sim" if evento[6] == 'S' else "Não",
                    "Idade Mínima": evento[7] if evento[7] else "Não especificada",
                    "Código de inscrição do Evento": evento[15]
                }

                print("\n--- Detalhes do Evento ---")
                for chave, valor in evento_formatado.items():
                    print(f"{chave}: {valor}")
                print('\n------------------------------------------')
        else:
            print("Nenhum evento aberto ao público encontrado.")

    except Exception as e:
        print(f"Erro ao listar eventos: {e}")

    finally:
        cursor.close()
        conexao.close()


def deletar_evento(usuario):
    #  function04

    conexao = conectardb()
    cursor = conexao.cursor()

    try:
        listar_eventos_criados(usuario)
        nome_evento = input('Digite o nome do evento que deseja remover: ')
        cursor.execute("SELECT criador FROM eventos WHERE nome_evento = %s", (nome_evento,))
        resultados = cursor.fetchall()
        if not resultados:
            print("Evento não encontrado!")
            return

        criador = verify_creator(usuario, resultados)
        if criador:
            confirmar = input("Tem certeza que deseja remover o evento? Digite 'S' ou 'N': ").upper()
            while confirmar not in ['S', 'N']:
                confirmar = input("Resposta inválida. Insira apenas 'S' ou 'N': ").upper()

            if confirmar == 'S':
                cursor.execute("DELETE FROM eventos WHERE nome_evento = %s", (nome_evento,))
                conexao.commit()
                print("Evento deletado com sucesso!")
            else:
                print("Ação cancelada. O evento não foi removido.")
        else:
            print("Você não é o criador desse evento. Não pode removê-lo.")

    except Exception as e:
        print(f"Erro ao deletar o evento: {e}")

    finally:
        cursor.close()
        conexao.close()


def deletar_inscricao(usuario):
    conexao = conectardb()
    cursor = conexao.cursor()

    try:
        eventos = listar_eventos_criados(usuario)
        if eventos:
            print("\n--- Eventos Criados por Você ---")
            for evento in eventos:
                print(f"- {evento[0]}")

        nome_evento = input("Digite o nome do evento que deseja gerenciar a lista de indesejados: ")

        cursor.execute("""
                    SELECT id_evento FROM eventos 
                    WHERE criador = %s AND nome_evento = %s
                """, (usuario[0][0], nome_evento))
        evento = cursor.fetchone()
        if not evento:
            print("Você não é o criador do evento ou o evento não existe!")
            return

        evento_id = evento[0]

        cursor.execute("""
            SELECT email, valor_pago
            FROM inscritos
            WHERE evento_id = %s
        """, (evento_id,))
        inscritos = cursor.fetchall()

        if not inscritos:
            print("Nenhum participante inscrito neste evento.")
            return

        print("\n--- Lista de Inscritos ---")
        for inscrito in inscritos:
            email, valor_pago = inscrito
            print(f"Email: {email}, Valor Pago: {valor_pago}")

        email_remover = input("\nDigite o email do participante que deseja remover: ")

        emails_inscritos = [inscrito[0] for inscrito in inscritos]
        if email_remover not in emails_inscritos:
            print("O email digitado não está na lista de inscritos.")
            return

        cursor.execute("""
            DELETE FROM inscritos
            WHERE evento_id = %s AND email = %s
        """, (evento_id, email_remover))
        conexao.commit()

        print(f"Inscrição do participante {email_remover} foi removida com sucesso.")

    except Exception as e:
        print(f"Erro ao deletar inscrição: {e}")

    finally:
        cursor.close()
        conexao.close()


def realizar_inscricao(usuario):

    nome_evento = input('Insira o nome do evento que deseja se inscrever: ')

    conexao = conectardb()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            "SELECT id_evento, valor, idade_minima, cupom_desconto FROM eventos WHERE nome_evento = %s",
            (nome_evento,))
        evento = cursor.fetchone()

        if not evento:
            print("Evento não encontrado!")
            return

        evento_id, valor_inscricao, idade_minima, cupom_desconto = evento

        cursor.execute(
            "SELECT * FROM blacklist_eventos WHERE email = %s AND id_evento = %s",
            (usuario[0][0], evento_id)
        )
        if cursor.fetchone():
            print("Você está na blacklist para este evento e não pode se inscrever.")
            return

        idade_usuario = usuario[0][3]
        if idade_minima and idade_usuario < idade_minima:
            print(f"Você não possui a idade mínima para se inscrever neste evento. Idade mínima: {idade_minima} anos.")
            return

        nome_participante = usuario[0][2]
        email = usuario[0][0]

        usar_cupom = input("Você tem um cupom de desconto? (S/N): ").upper()
        while usar_cupom not in ['S', 'N']:
            print("Resposta inválida! Insira 'S' para sim ou 'N' para não.")
            usar_cupom = input("Você tem um cupom de desconto? (S/N): ").upper()

        desconto_aplicado = 0
        if usar_cupom == 'S':
            codigo_cupom = input("Digite o código do seu cupom: ").strip()

            cursor.execute("SELECT cupom_desconto FROM eventos WHERE nome_evento = %s", (nome_evento,))
            resultado_cupom = cursor.fetchone()

            if resultado_cupom:
                try:
                    if isinstance(resultado_cupom[0], dict):  # Caso seja um dict
                        cupom_json = resultado_cupom[0]
                    else:
                        cupom_json = json.loads(resultado_cupom[0])

                    if cupom_json.get("codigo") == codigo_cupom:
                        desconto_percentual = cupom_json.get("valor", 0)
                        desconto_aplicado = (valor_inscricao * desconto_percentual) / 100
                        print(
                            f"Desconto de {desconto_percentual}% aplicado. Valor original: R${valor_inscricao:.2f}, desconto: R${desconto_aplicado:.2f}.")
                    else:
                        print("Código de cupom inválido!")
                except Exception as e:
                    print(f"Erro ao processar o cupom: {e}")
            else:
                print("Nenhum cupom encontrado.")

        valor_com_desconto = valor_inscricao - desconto_aplicado

        cursor.execute("""
            SELECT * FROM inscritos 
            WHERE email = %s AND evento_id = %s
        """, (email, evento_id))
        inscricao_existente = cursor.fetchone()

        if inscricao_existente:
            print("Você já está inscrito neste evento!")
            return

        escolha = input("Deseja pagar a inscrição agora? (S/N): ").upper()
        while escolha not in ['S', 'N']:
            print("Resposta inválida! Insira 'S' para pagar agora ou 'N' para pagar no evento.")
            escolha = input("Deseja pagar a inscrição agora? (S/N): ").upper()

        pagamento_realizado = (escolha == 'S')

        cursor.execute("""
            INSERT INTO inscritos (nome_participante, evento_id, pagamento_realizado, email, nome_evento, valor_pago)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome_participante, evento_id, pagamento_realizado, email, nome_evento, valor_com_desconto))

        conexao.commit()

        if pagamento_realizado:
            print("Inscrição paga com sucesso! Valor adicionado ao total arrecadado pelo evento via trigger.")
        else:
            print("Inscrição registrada! Valor será pago no evento e processado pelo trigger.")

    except Exception as e:
        conexao.rollback()
        print(f"Erro ao processar a inscrição: {e}")

    finally:
        cursor.close()
        conexao.close()


def realizar_inscricao_por_codigo(usuario):

    conexao = conectardb()
    cursor = conexao.cursor()

    try:
        codigo_inscricao = input("Digite o código de inscrição do evento: ").strip()

        cursor.execute("""
            SELECT id_evento, nome_evento, valor
            FROM eventos
            WHERE codigo_inscricao = %s
        """, (codigo_inscricao,))
        evento = cursor.fetchone()

        if evento:
            id_evento, nome_evento, valor_inscricao = evento

            cursor.execute("""
                SELECT * FROM inscritos
                WHERE evento_id = %s AND email = %s
            """, (id_evento, usuario[0][0]))
            inscricao_existente = cursor.fetchone()

            if inscricao_existente:
                print(f"Você já está inscrito no evento '{nome_evento}'.")
            else:
                escolha = input("Deseja pagar agora? (S/N): ").upper()
                while escolha not in ['S', 'N']:
                    print("Resposta inválida! Insira 'S' para pagar agora ou 'N' para pagar no evento.")
                    escolha = input("Deseja pagar agora? (S/N): ").upper()

                pagamento_realizado = (escolha == 'S')

                if pagamento_realizado:
                    cursor.execute("""
                        UPDATE eventos
                        SET valor_arrecadado = COALESCE(valor_arrecadado, 0) + %s
                        WHERE id_evento = %s
                    """, (valor_inscricao, id_evento))
                    print("Pagamento realizado com sucesso! Valor adicionado ao total arrecadado.")
                else:
                    cursor.execute("""
                        UPDATE eventos
                        SET valor_pendente = COALESCE(valor_pendente, 0) + %s
                        WHERE id_evento = %s
                    """, (valor_inscricao, id_evento))
                    print("Inscrição registrada! Valor será pago no evento.")

                nome_participante = usuario[0][2]
                email = usuario[0][0]

                cursor.execute("""
                    INSERT INTO inscritos (nome_participante, evento_id, pagamento_realizado, email, nome_evento)
                    VALUES (%s, %s, %s, %s, %s)
                """, (nome_participante, id_evento, pagamento_realizado, email, nome_evento))

                conexao.commit()
                print(f"Inscrição realizada com sucesso no evento '{nome_evento}'.")
        else:
            print("Erro: Código de inscrição inválido.")

    except Exception as e:
        conexao.rollback()
        print(f"Erro ao realizar a inscrição: {e}")

    finally:
        cursor.close()
        conexao.close()


def inscrever_participante(usuario):

    conexao = conectardb()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
                    SELECT nome_evento
                    FROM eventos
                    WHERE criador = %s
                """, (usuario[0][0],))
        eventos = cursor.fetchall()

        if eventos:
            print("\n--- Eventos Criados por Você ---")
            for evento in eventos:
                print(f"- {evento[0]}")

        nome_evento = input('Insira o nome do evento que deseja inscrever um usuario: ')

        cursor.execute(
            "SELECT id_evento, valor, idade_minima, cupom_desconto, criador FROM eventos WHERE nome_evento = %s",
            (nome_evento,))
        evento = cursor.fetchone()

        if not evento:
            print("Evento não encontrado!")
            return

        evento_id, valor_inscricao, idade_minima, cupom_desconto, criador = evento

        if not usuario[0][0] == criador:
            print('Você não tem permissão para gerenciar inscrições para este evento.')
            return
        idade = int(input('Insira a idade do usuario:'))
        if idade_minima and idade < idade_minima:
            print(f"Você não possui a idade mínima para se inscrever neste evento. Idade mínima: {idade_minima} anos.")
            return

        email_user = input('Insira o email do usuario:')
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email_user,))
        usuario_cadastrado = cursor.fetchone()
        if usuario_cadastrado:
            print('Este usuario já possui conta em nosso sistema, ele deve fazer a inscrição através de sua conta')
            return

        if not usuario_cadastrado:
            print("O email fornecido não pertence a nenhum usuário cadastrado!")

        cursor.execute(
            "SELECT * FROM blacklist_eventos WHERE email = %s AND id_evento = %s",
            (email_user, evento_id)
        )
        if cursor.fetchone():
            print("Este usuario está na blacklist para este evento e não pode se inscrever.")
            return

        nome_participante = input('Insira o nome do usuario: ')

        usar_cupom = input("Você tem um cupom de desconto? (S/N): ").upper()
        while usar_cupom not in ['S', 'N']:
            print("Resposta inválida! Insira 'S' para sim ou 'N' para não.")
            usar_cupom = input("Você tem um cupom de desconto? (S/N): ").upper()

        desconto_aplicado = 0
        if usar_cupom == 'S':
            codigo_cupom = input("Digite o código do seu cupom: ").strip()

            cursor.execute("SELECT cupom_desconto FROM eventos WHERE nome_evento = %s", (nome_evento,))
            resultado_cupom = cursor.fetchone()

            if resultado_cupom:
                try:
                    if isinstance(resultado_cupom[0], dict):
                        cupom_json = resultado_cupom[0]
                    else:
                        cupom_json = json.loads(resultado_cupom[0])

                    if cupom_json.get("codigo") == codigo_cupom:
                        desconto_percentual = cupom_json.get("valor", 0)
                        desconto_aplicado = (valor_inscricao * desconto_percentual) / 100
                        print(
                            f"Desconto de {desconto_percentual}% aplicado. Valor original: R${valor_inscricao:.2f}, desconto: R${desconto_aplicado:.2f}.")
                    else:
                        print("Código de cupom inválido!")
                except Exception as e:
                    print(f"Erro ao processar o cupom: {e}")
            else:
                print("Nenhum cupom encontrado.")

        valor_com_desconto = valor_inscricao - desconto_aplicado

        cursor.execute("""
                SELECT * FROM inscritos 
                WHERE email = %s AND evento_id = %s
            """, (email_user, evento_id))
        inscricao_existente = cursor.fetchone()

        if inscricao_existente:
            print(f"O usuário já está inscrito no evento '{nome_evento}'.")
            return

        escolha = input("Deseja pagar a inscrição agora? (S/N): ").upper()
        while escolha not in ['S', 'N']:
            print("Resposta inválida! Insira 'S' para pagar agora ou 'N' para pagar no evento.")
            escolha = input("Deseja pagar a inscrição agora? (S/N): ").upper()

        pagamento_realizado = (escolha == 'S')

        cursor.execute("""
                INSERT INTO inscritos (nome_participante, evento_id, pagamento_realizado, email, nome_evento, valor_pago)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nome_participante, evento_id, pagamento_realizado, email_user, nome_evento, valor_com_desconto))

        conexao.commit()

        if pagamento_realizado:
            print("Inscrição paga com sucesso! Valor adicionado ao total arrecadado pelo evento via trigger.")
        else:
            print("Inscrição registrada! Valor será pago no evento e processado pelo trigger.")

    except Exception as e:
        conexao.rollback()
        print(f"Erro ao processar a inscrição: {e}")

    finally:
        cursor.close()
        conexao.close()


def remover_inscricao(usuario):
    listar_eventos_inscritos(usuario)

    conexao = conectardb()
    cursor = conexao.cursor()

    nome_evento = input('Digite o nome do evento que deseja remover sua inscrição: ')

    try:
        email_usuario = usuario[0][0]

        cursor.execute("""
            SELECT id_evento 
            FROM eventos
            WHERE nome_evento = %s
        """, (nome_evento,))
        resultado_evento = cursor.fetchone()

        if not resultado_evento:
            print("O evento com o nome fornecido não existe.")
            return

        evento_id = resultado_evento[0]

        cursor.execute("""
            SELECT email 
            FROM inscritos 
            WHERE evento_id = %s AND email = %s
        """, (evento_id, email_usuario))
        resultado_inscricao = cursor.fetchone()

        if resultado_inscricao:
            print(f"O usuário está inscrito no evento '{nome_evento}'.")

            confirmacao = input("Você deseja realmente remover sua inscrição desse evento? (s/n): ").strip().lower()
            if confirmacao == 's':
                cursor.execute("""
                    DELETE FROM inscritos
                    WHERE evento_id = %s AND email = %s
                """, (evento_id, email_usuario))

                conexao.commit()
                print(f"Inscrição no evento '{nome_evento}' foi removida com sucesso.")
            else:
                print("Operação cancelada pelo usuário.")
        else:
            print(f"O usuário NÃO está inscrito no evento '{nome_evento}'.")

    except Exception as e:
        print(f"Erro ao verificar ou remover inscrição no evento: {e}")

    finally:
        cursor.close()
        conexao.close()


def listar_eventos_inscritos(usuario):
    conexao = conectardb()
    cursor = conexao.cursor()

    try:
        email = usuario[0][0]

        cursor.execute("""
            SELECT evento_id, valor_pago
            FROM inscritos
            WHERE email = %s
        """, (email,))
        inscricoes = cursor.fetchall()

        if not inscricoes:
            print("Você não está inscrito em nenhum evento.")
            return

        print("Eventos nos quais você está inscrito:")
        for inscricao in inscricoes:
            evento_id, valor_pago = inscricao

            cursor.execute("""
                SELECT 
                    id_evento, 
                    nome_evento, 
                    idade_minima
                FROM eventos
                WHERE id_evento = %s
            """, (evento_id,))
            evento = cursor.fetchone()

            if evento:
                id_evento, nome_evento, idade_minima = evento
                status_pagamento = f"Valor Pago: {valor_pago}"
                print(
                    f"- ID: {id_evento}, Nome: {nome_evento}, {status_pagamento}, Idade Mínima: {idade_minima or 'Livre'}")

    except Exception as e:
        print(f"Erro ao listar eventos inscritos: {e}")

    finally:
        cursor.close()
        conexao.close()


def listar_participantes_evento(usuario):
    #  function07

    conexao = conectardb()
    cursor = conexao.cursor()

    try:
        eventos = listar_eventos_criados(usuario)

        if eventos:
            print("\n--- Eventos Criados por Você ---")
            for evento in eventos:
                print(f"- {evento[0]}")

        nome_evento = input("Digite o nome do evento para listar os participantes: ")

        cursor.execute("""
            SELECT id_evento, criador 
            FROM eventos
            WHERE nome_evento = %s
        """, (nome_evento,))
        resultado_evento = cursor.fetchone()

        if not resultado_evento:
            print("O evento com o nome fornecido não existe.")
            return

        id_evento, criador = resultado_evento

        if usuario[0][0] == criador:
            cursor.execute("""
                SELECT nome_participante,
                email,
                pagamento_realizado 
                FROM inscritos
                WHERE evento_id = %s
            """, (id_evento,))
            participantes = cursor.fetchall()

            if not participantes:
                print("Nenhum participante encontrado para este evento.")
                return

            print(f"Participantes do evento '{nome_evento}':")
            for participante in participantes:
                print(f"-------------------------------------------------------------\n"
                      f"- Nome: {participante[0]}\n"
                      f"- Email: {participante[1]}\n"
                      f"- Status Pagamento: {'pago' if participante[2] else 'Pendente'}\n")

        else:
            print("Você não tem permissão para visualizar os participantes desse evento.")

    except Exception as e:
        print(f"Erro ao tentar listar os participantes do evento: {e}")

    finally:
        cursor.close()
        conexao.close()


def exibir_detalhes_evento(usuario):

    conexao = conectardb()
    cursor = conexao.cursor()

    try:
        eventos = listar_eventos_criados(usuario)

        if eventos:
            print("\n--- Eventos Criados por Você ---")
            for evento in eventos:
                print(f"- {evento[0]}")

        nome_evento = input("Digite o nome do evento para visualizar detalhes: ")

        cursor.execute("""
            SELECT *
            FROM eventos
            WHERE nome_evento = %s AND criador = %s
        """, (nome_evento, usuario[0][0]))
        evento = cursor.fetchone()

        if evento:
            print("\n--- Detalhes do Evento ---")
            print(f"Id do Evento: {evento[0]}")
            print(f"Nome do Evento: {evento[1]}")
            print(f"Descrição: {evento[2]}")
            print(f"Data do Evento: {evento[3]}")
            print(f"Local: {evento[4]}")
            print(f"Valor: R$ {evento[5]:.2f}")
            print(f"Cancelável: {'Sim' if evento[6] else 'Não'}")
            print(f"Idade Mínima: {evento[7]} anos")
            print(f"Data de Criação: {evento[8]}")
            print(f"Criador: {evento[9]}")
            print(f"Valor Arrecadado: R$ {evento[10]:.2f}")
            print(f"Valor Pendente: R$ {evento[11]:.2f}")
            print(f"Doações: R$ {evento[12]:.2f}")
            print(f"Capacidade Máxima: {'Não informado' if not evento[13] else f'{evento[13]} pessoas'}")
            print(f"Evento Aberto: {'Sim' if evento[14] else 'Não'}")
            print(f"Código de Inscrição: {evento[15]}")
        else:
            print("Erro: Você não tem permissão para visualizar este evento ou ele não existe.")

    except Exception as e:
        print(f"Erro ao tentar exibir detalhes do evento: {e}")

    finally:
        cursor.close()
        conexao.close()


def adicionar_blacklist(usuario):

    conexao = conectardb()
    cursor = conexao.cursor()

    try:
        eventos = listar_eventos_criados(usuario)

        if eventos:
            print("\n--- Eventos Criados por Você ---")
            for evento in eventos:
                print(f"- {evento[0]}")

        nome_evento = input("Digite o nome do evento que deseja gerenciar a lista de indesejados: ")
        cursor.execute("""
            SELECT id_evento FROM eventos 
            WHERE criador = %s AND nome_evento = %s
        """, (usuario[0][0], nome_evento))
        evento = cursor.fetchone()

        if not evento:
            print("Você não é o criador do evento ou o evento não existe!")
            return

        email_blacklist = input('Insira o email indesejado: ')

        cursor.execute("""
            INSERT INTO blacklist_eventos (id_evento, email)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, (evento[0], email_blacklist))

        conexao.commit()
        print(f"O email '{email_blacklist}' foi adicionado à blacklist do evento {nome_evento} com sucesso!")

    except Exception as e:
        print(f"Erro ao adicionar o email à blacklist: {e}")
    finally:
        cursor.close()
        conexao.close()


def remover_blacklist(usuario):

    conexao = conectardb()
    cursor = conexao.cursor()

    try:
        eventos = listar_eventos_criados(usuario)

        if eventos:
            print("\n--- Eventos Criados por Você ---")
            for evento in eventos:
                print(f"- {evento[0]}")

        nome_evento = input("Digite o nome do evento que deseja gerenciar a lista de indesejados: ")
        cursor.execute("""
            SELECT id_evento FROM eventos 
            WHERE criador = %s AND nome_evento = %s
        """, (usuario[0][0], nome_evento))
        evento = cursor.fetchone()

        if not evento:
            print("Você não é o criador do evento ou o evento não existe!")
            return

        email_blacklist = input('Insira o email que deseja remover da lista de indesejados: ')
        cursor.execute("""
            DELETE FROM blacklist_eventos
            WHERE id_evento = %s AND email = %s
        """, (evento[0], email_blacklist))

        conexao.commit()
        print(f"O email '{email_blacklist}' foi removido da blacklist do evento {nome_evento}com sucesso!")

    except Exception as e:
        print(f"Erro ao remover o email da blacklist: {e}")
    finally:
        cursor.close()
        conexao.close()


def listar_blacklist(usuario):

    conexao = conectardb()
    cursor = conexao.cursor()

    try:
        eventos = listar_eventos_criados(usuario)
        if eventos:
            print("\n--- Eventos Criados por Você ---")
            for evento in eventos:
                print(f"- {evento[0]}")

        nome_evento = input("Digite o nome do evento que deseja ver a lista de indesejados: ")
        cursor.execute("""
                    SELECT id_evento FROM eventos 
                    WHERE criador = %s AND nome_evento = %s
                """, (usuario[0][0], nome_evento))
        evento = cursor.fetchone()

        if not evento:
            print("Você não é o criador do evento ou o evento não existe!")
            return

        cursor.execute("""
            SELECT email FROM blacklist_eventos
            WHERE id_evento = %s
        """, (evento[0],))

        emails = cursor.fetchall()
        if emails:
            print(f"Emails na blacklist do evento '{nome_evento}':")
            for e in emails:
                print(f"- {e[0]}")
        else:
            print("A blacklist está vazia para este evento.")

    except Exception as e:
        print(f"Erro ao listar a blacklist: {e}")
    finally:
        cursor.close()
        conexao.close()
