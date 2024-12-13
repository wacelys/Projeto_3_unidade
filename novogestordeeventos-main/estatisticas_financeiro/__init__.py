import random
import string
import json
import plotly.graph_objects as go
import plotly.subplots as sp
import webbrowser
import os
from dao import *
import datetime


def gerar_codigo_cupom():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def adicionar_cupom_antigo(usuario):

    conexao = conectardb()
    cursor = conexao.cursor()

    try:
        eventos = listar_eventos_criados(usuario)

        if eventos:
            print("\n--- Eventos Criados por Você ---")
            for evento in eventos:
                print(f"- {evento[0]}")
        else:
            print("Você ainda não criou nenhum evento.")

        nome_evento = input("\nDigite o nome do evento que deseja adicionar um cupom: ").strip()

        cursor.execute("""
            SELECT id_evento FROM eventos WHERE nome_evento = %s AND criador = %s
        """, (nome_evento, usuario[0][0]))
        evento = cursor.fetchone()

        if evento:
            codigo_cupom = gerar_codigo_cupom()
            # Solicita o valor do cupom
            valor_cupom = float(input("Digite o valor do cupom de desconto (%): ").strip())

            cupom_json = json.dumps({"codigo": codigo_cupom, "valor": valor_cupom})

            cursor.execute("""
                UPDATE eventos
                SET cupom_desconto = %s
                WHERE id_evento = %s
            """, (cupom_json, evento[0]))
            conexao.commit()

            print(
                f"\nCupom de desconto no valor de R${valor_cupom:.2f} adicionado com sucesso ao evento '{nome_evento}'.")
            print(f"Código do cupom gerado: {codigo_cupom}")

        else:
            print("\nErro: Nome do evento inválido ou você não tem permissão para adicionar cupons nesse evento.")

    except Exception as e:
        conexao.rollback()
        print(f"\nErro ao adicionar o cupom: {e}")

    finally:
        cursor.close()
        conexao.close()


def realizar_doacao():

    conexao = conectardb()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT nome_evento
            FROM eventos
            WHERE aberto = TRUE
        """)
        eventos = cursor.fetchall()

        if eventos:
            print("\n--- Eventos Abertos ---")
            for evento in eventos:
                print(f"- {evento[0]}")

            nome_evento_escolhido = input("\nDigite o nome do evento para realizar a doação: ")

            cursor.execute("""
                SELECT id_evento
                FROM eventos
                WHERE nome_evento = %s AND aberto = TRUE
            """, (nome_evento_escolhido,))
            evento = cursor.fetchone()

            if evento:
                while True:
                    try:
                        valor_doacao = float(input("Digite o valor da doação: R$ "))
                        if valor_doacao <= 0:
                            print("O valor da doação deve ser maior que zero.")
                        else:
                            break
                    except ValueError:
                        print("Por favor, insira um valor numérico válido.")

                cursor.execute("""
                    UPDATE eventos
                    SET doacoes = COALESCE(doacoes, 0) + %s
                    WHERE id_evento = %s
                """, (valor_doacao, evento[0]))

                conexao.commit()
                print(f"Doação de R$ {valor_doacao:.2f} realizada com sucesso para o evento '{nome_evento_escolhido}'.")
            else:
                print("Erro: Evento não encontrado ou não está aberto.")
        else:
            print("Não há eventos abertos no momento.")

    except Exception as e:
        conexao.rollback()
        print(f"Erro ao realizar a doação: {e}")

    finally:
        cursor.close()
        conexao.close()


def verificar_valor_arrecadado(usuario):
    conexao = conectardb()
    cursor = conexao.cursor()

    try:
        eventos = listar_eventos_criados(usuario)

        if eventos:
            print("\n--- Eventos Criados por Você ---")
            for evento in eventos:
                print(f"- {evento[0]}")

            nome_evento_escolhido = input("\nDigite o nome do evento para visualizar a arrecadação: ")

            cursor.execute("""
                SELECT valor_arrecadado, valor_pendente, doacoes
                FROM eventos
                WHERE nome_evento = %s AND criador = %s
            """, (nome_evento_escolhido, usuario[0][0]))
            resultado = cursor.fetchone()

            if resultado:
                valor_arrecadado = resultado[0] or 0
                valor_pendente = resultado[1] or 0
                doacoes = resultado[2] or 0

                valor_total_esperado = valor_arrecadado + valor_pendente + doacoes
                valor_arrecadado_atual = valor_arrecadado + doacoes

                print("\n--- Resumo Financeiro do Evento ---")
                print(f"Evento: {nome_evento_escolhido}")
                print(f"Valor Inscrições Pendentes: R$ {valor_pendente:.2f}")
                print(f"Valor Inscrições Pagas: R$ {valor_arrecadado}")
                print(f"Valor Total de Doações: {doacoes:.2f}")
                print(f"Valor Arrecadado Total (Valores já pagos e doações): R$ {valor_arrecadado_atual:.2f}")
                print(f"Valor Total Esperado: R$ {valor_total_esperado:.2f}")

                labels = ['Arrecadado', 'Pendente', 'Doações', 'Receita Atual', 'Receita Total Esperada']
                values = [valor_arrecadado, valor_pendente, doacoes, valor_arrecadado_atual, valor_total_esperado]

                fig = go.Figure(data=[
                    go.Bar(
                        x=labels,
                        y=values,
                        text=[f"R$ {v:.2f}" for v in values],
                        textposition='auto',
                        marker=dict(color=['#4caf50', '#ff9800', '#03a9f4', '#8bc34a', '#9c27b0'])
                    )
                ])

                fig.update_layout(
                    title=f"Estatísticas Financeiras do Evento: {nome_evento_escolhido}",
                    xaxis_title="Categoria",
                    yaxis_title="Valores em R$",
                    template="plotly_white"
                )

                html_file = "grafico_estatisticas.html"
                fig.write_html(html_file)

                webbrowser.open('file://' + os.path.realpath(html_file))
                print(f"Gráfico gerado e salvo em: {html_file}")

            else:
                print("Erro: Não foi possível recuperar os dados financeiros do evento. Verifique se o nome está correto.")
        else:
            print("Você não possui eventos cadastrados.")

    except Exception as e:
        print(f"Erro ao calcular os valores arrecadados: {e}")

    finally:
        cursor.close()
        conexao.close()


def estatisticas_inscritos(usuario):

    conexao = conectardb()
    cursor = conexao.cursor()

    try:
        eventos = listar_eventos_criados(usuario)

        if not eventos:
            print("Você não possui eventos cadastrados.")
            return None

        print("\n--- Eventos Criados por Você ---")
        for evento in eventos:
            print(f"- {evento[0]}")

        nome_evento = input("\nDigite o nome do evento para visualizar as estatísticas: ")

        cursor.execute(
            """
            SELECT id_evento, capacidade_maxima 
            FROM eventos
            WHERE criador = %s AND nome_evento = %s
            """,
            (usuario[0][0], nome_evento),
        )
        evento = cursor.fetchone()

        if not evento:
            print("Você não é o criador do evento ou o evento não existe!")
            return None

        id_evento, capacidade = evento

        capacidade = capacidade if capacidade not in (None, 0) else None

        cursor.execute(
            """
            SELECT 
                COUNT(*) AS total_inscritos,
                SUM(CASE WHEN pagamento_realizado = FALSE THEN 1 ELSE 0 END) AS nao_pagantes
            FROM inscritos
            WHERE evento_id = %s
            """,
            (id_evento,),
        )
        resultado = cursor.fetchone()

        total_inscritos = resultado[0] if resultado[0] is not None else 0
        nao_pagantes = resultado[1] if resultado[1] is not None else 0

        pagantes = total_inscritos - nao_pagantes
        taxa_pagamento = (pagantes / total_inscritos) * 100 if total_inscritos > 0 else 0
        taxa_nao_pagamento = 100 - taxa_pagamento if total_inscritos > 0 else 0

        lotacao = (total_inscritos / capacidade) * 100 if capacidade else None

        print("\n--- Estatísticas do Evento ---")
        print(f"Evento: {nome_evento}")
        print(f"Total de Inscritos: {total_inscritos}")
        print(f"Inscrições Pagas: {pagantes}")
        print(f"Pagamentos Pendentes: {nao_pagantes}")
        print(f"Taxa de Pagamento: {taxa_pagamento:.2f}%")
        print(f"Taxa de Não Pagamento: {taxa_nao_pagamento:.2f}%")
        print(f"Capacidade Máxima: {capacidade if capacidade else 'Não informado'}")
        print(f"Lotação: {lotacao:.2f}%" if lotacao else "Lotação: Não informado")

        categorias = [
            "Total Inscritos",
            "Inscrições Pagas",
            "Pagamentos Pendentes",
            "Taxa de Pagamento (%)",
            "Taxa de Não Pagamento (%)",
            "Lotação (%)",
        ]
        valores = [
            total_inscritos,
            pagantes,
            nao_pagantes,
            taxa_pagamento,
            taxa_nao_pagamento,
            lotacao if lotacao else 0,
        ]

        proporcoes = [1, 1, 1, 0.5, 0.5, 1]
        valores_ajustados = [v * p for v, p in zip(valores, proporcoes)]

        fig = go.Figure(
            data=[
                go.Bar(
                    x=categorias,
                    y=valores_ajustados,
                    text=[f"{v:.2f}" if i >= 3 else int(v) for i, v in enumerate(valores)],
                    textposition='auto',
                    marker=dict(color=["blue", "green", "red", "purple", "orange", "cyan"]),
                )
            ]
        )

        fig.update_layout(
            title=f"Estatísticas do Evento: {nome_evento}",
            xaxis_title="Categoria",
            yaxis_title="Valores (Proporção para taxas)",
            template="plotly_white",
        )

        arquivo_html = f"estatisticas_{nome_evento}.html"
        fig.write_html(arquivo_html)

        webbrowser.open('file://' + os.path.realpath(arquivo_html))
        print(f"Gráfico salvo como {arquivo_html}. Abra no navegador para visualizar.")

    except Exception as e:
        print(f"Erro ao obter estatísticas do evento: {e}")
        return None

    finally:
        cursor.close()
        conexao.close()


def obter_e_gerar_grafico_estatisticas_avancadas(usuario):

    conexao = conectardb()
    cursor = conexao.cursor()

    try:
        eventos = listar_eventos_criados(usuario)

        if not eventos:
            print("Você não possui eventos cadastrados.")
            return None

        print("\n--- Eventos Criados por Você ---")
        for evento in eventos:
            print(f"- {evento[0]}")

        nome_evento = input("\nDigite o nome do evento para visualizar as estatísticas: ")

        cursor.execute(
            """
            SELECT id_evento
            FROM eventos
            WHERE criador = %s AND nome_evento = %s
            """,
            (usuario[0][0], nome_evento),
        )
        evento = cursor.fetchone()

        if not evento:
            print("Você não é o criador do evento ou o evento não existe!")
            return None

        id_evento = evento[0]

        cursor.execute(
            """
            SELECT 
                CASE
                    WHEN u.idade < 18 THEN 'Menor de 18'
                    WHEN u.idade BETWEEN 18 AND 24 THEN '18-24'
                    WHEN u.idade BETWEEN 25 AND 34 THEN '25-34'
                    WHEN u.idade BETWEEN 35 AND 44 THEN '35-44'
                    WHEN u.idade BETWEEN 45 AND 54 THEN '45-54'
                    WHEN u.idade >= 55 THEN '55+' 
                    ELSE 'Não Informada'
                END AS faixa_etaria,
                COUNT(*)
            FROM inscritos i
            JOIN usuarios u ON i.email = u.email
            WHERE i.evento_id = %s
            GROUP BY faixa_etaria
            """,
            (id_evento,),
        )
        distribuicao_etaria = cursor.fetchall()
        faixas_etarias = [item[0] for item in distribuicao_etaria]
        qtd_por_faixa = [item[1] for item in distribuicao_etaria]

        cursor.execute(
            """
            SELECT genero, COUNT(*)
            FROM inscritos i
            JOIN usuarios u ON i.email = u.email
            WHERE i.evento_id = %s
            GROUP BY genero
            """,
            (id_evento,),
        )
        distribuicao_genero = cursor.fetchall()
        generos = [item[0] for item in distribuicao_genero]
        qtd_por_genero = [item[1] for item in distribuicao_genero]

        cursor.execute(
            """
            SELECT estado, COUNT(*)
            FROM inscritos i
            JOIN usuarios u ON i.email = u.email
            WHERE i.evento_id = %s
            GROUP BY estado
            """,
            (id_evento,),
        )
        distribuicao_localidade = cursor.fetchall()
        localidades = [item[0] for item in distribuicao_localidade]
        qtd_por_localidade = [item[1] for item in distribuicao_localidade]

        fig = sp.make_subplots(
            rows=3, cols=1,
            subplot_titles=(
                "Distribuição por Faixa Etária",
                "Percentual de Participantes por Gênero",
                "Participantes por Localidade"
            )
        )

        fig.add_trace(
            go.Bar(
                x=faixas_etarias,
                y=qtd_por_faixa,
                marker=dict(color=["aqua", "green", "chartreuse", "chocolate", "coral", "cornflowerblue",
                                   "cyan", "darkorange", "darkturquoise", "deeppink", "deepskyblue", "fuchsia", "gold",
                                   "goldenrod", "green", "greenyellow", "honeydew", "hotpink", "indianred", "lime",
                                   "limegreen", "mediumaquamarine", "mediumspringgreen", "mediumvioletred", "orange",
                                   ]),
                text=qtd_por_faixa,
                textposition="inside",
                name="Faixa Etária"
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Bar(
                x=generos,
                y=qtd_por_genero,
                marker=dict(color=["chartreuse", "coral", "cyan", "darkorange",
                                   "deeppink", "deepskyblue", "fuchsia", "gold", "green", "greenyellow",
                                   "honeydew", "hotpink", "indianred", "lime", "limegreen", "mediumaquamarine",
                                   "mediumspringgreen", "mediumvioletred", "orange", "orchid", "peachpuff",
                                   ]),
                text=qtd_por_genero,
                textposition="inside",
                name="Gêneros"
            ),
            row=2, col=1
        )

        fig.add_trace(
            go.Bar(
                x=localidades,
                y=qtd_por_localidade,
                marker=dict(color=["orange", "hotpink", "green", "chartreuse",
                                   "blue", "teal", "yellow", "springgreen", "blueviolet", "lime",
                                   "gold", "fuchsia", "red", "deepskyblue", "darkorange", "palegreen",
                                   "lightcyan", "yellowgreen", "mediumspringgreen", "mediumvioletred",
                                  ]),
                text=qtd_por_localidade,
                textposition="inside",
                name="Localidades"
            ),
            row=3, col=1
        )

        fig.update_layout(
            title=f"Estatísticas Avançadas do Evento: {nome_evento}",
            height=900,
            template="plotly_white"
        )

        arquivo_html = f"estatisticas_{nome_evento}.html"
        fig.write_html(arquivo_html)
        webbrowser.open('file://' + os.path.realpath(arquivo_html))
        print(f"Gráficos salvos como {arquivo_html}. Veja no navegador.")

    except Exception as e:
        print(f"Erro ao buscar estatísticas: {e}")
    finally:
        cursor.close()
        conexao.close()


def capturar_infos_cupom(usuario):
    """Captura informações do usuário e adiciona um cupom associado a um evento."""
    try:
        eventos = listar_eventos_criados(usuario)

        if not eventos:
            print("Você não possui eventos cadastrados.")
            return None

        print("\n--- Eventos Criados por Você ---")
        for evento in eventos:
            print(f"- {evento[0]}")

        nome_evento = input("Informe o nome do evento ao qual o cupom será associado: ").strip()
        email_user = usuario[0][0]
        print(email_user)
        if verificar_criador_evento(nome_evento, email_user):
            print('Você é o criador desse evento!')
        else:
            return
        # Captura informações do cupom
        codigo = input("Informe o código do cupom (máximo 20 caracteres, letras e números): ").strip()
        if len(codigo) > 20 or not codigo.isalnum():
            raise ValueError("O código deve ter no máximo 20 caracteres sendo apenas letras e números.")

        valor = float(input("Informe o valor do desconto (apenas números): ").strip())

        # Validação direta do tipo de desconto
        tipo_desconto = input("Informe o tipo de desconto ('fixo' ou 'percentual'): ").strip().lower()
        while tipo_desconto not in ['fixo', 'percentual']:
            print("Tipo de desconto inválido! Insira 'fixo' ou 'percentual'.")
            tipo_desconto = input("Informe o tipo de desconto ('fixo' ou 'percentual'): ").strip().lower()

        data_expiracao = input("Informe a data de expiração (YYYY-MM-DD): ").strip()
        data_expiracao_datetime = datetime.datetime.strptime(data_expiracao, '%d/%m/%Y')
        if data_expiracao_datetime <= datetime.datetime.now():
            raise ValueError("A data de expiração deve ser uma data futura.")

        quantidade_maxima = int(input("Informe a quantidade máxima de usos do cupom (máximo 1000): ").strip())
        if quantidade_maxima > 1000:
            raise ValueError("A quantidade máxima de usos não deve ser maior que 1000.")

        # Confirma os dados inseridos
        print("\nResumo do cupom:")
        print(f"Código: {codigo}")
        print(f"Valor: {valor}")
        print(f"Tipo de Desconto: {tipo_desconto}")
        print(f"Data de Expiração: {data_expiracao}")
        print(f"Quantidade Máxima de Usos: {quantidade_maxima}")
        print(f"Nome do Evento: {nome_evento}")

        confirmacao = input("\nDeseja salvar esse cupom? (s/n): ").strip().lower()
        if confirmacao != 's':
            print("Operação cancelada pelo usuário.")
            return

        # Chama a função que insere o cupom e atualiza o evento
        adicionar_cupom(codigo, valor, tipo_desconto, data_expiracao, quantidade_maxima, nome_evento)

    except ValueError as ve:
        print(f"Erro de valor inválido: {ve}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


def adicionar_cupom(codigo, valor, tipo_desconto, data_expiracao, quantidade_maxima, nome_evento):
    """Chama o DAO para inserir cupom e atualizar evento."""
    try:
        inserir_cupom_e_atualizar_evento(
            codigo=codigo,
            valor=valor,
            tipo_desconto=tipo_desconto,
            data_expiracao=data_expiracao,
            quantidade_maxima=quantidade_maxima,
            nome_evento=nome_evento
        )
    except Exception as e:
        print(f"Erro ao adicionar cupom: {e}")