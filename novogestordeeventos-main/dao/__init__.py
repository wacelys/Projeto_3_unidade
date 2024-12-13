import psycopg2


# conexãoDB


def conectardb():
    conexao = psycopg2.connect(database="gestor_de_eventos",
                               host="localhost",
                               user="postgres",
                               password="Macelo321",
                               port="5432")
    return conexao

# DAO referente ao usuario


def inserir_usuario(nome, email, senha, idade, profissao, estado, genero):
    conexao = conectardb()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha, idade, profissao, estado, genero)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, email, senha, idade, profissao, estado, genero))
        conexao.commit()
        return True
    except Exception as e:
        print(f"Erro ao insersir o usuario:{e}")
        conexao.rollback()
        return False
    finally:
        cursor.close()
        conexao.close()


def login_db(email, senha):
    conexao = conectardb()
    cursor = conexao.cursor()
    cursor.execute(f"SELECT email, senha, nome, idade, profissao, estado, id_usuario, "
                   f"genero FROM usuarios WHERE email = '{email}' and senha='{senha}' ")
    usuario = cursor.fetchall()
    cursor.close()
    conexao.close()
    return usuario


def buscar_usuario(nome):
    conexao = conectardb()
    cursor = conexao.cursor()
    cursor.execute(f"SELECT email, nome FROM usuarios WHERE nome = '{nome}' ")
    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultado


def buscar_usuario_id(id):
    conexao = conectardb()
    cursor = conexao.cursor()
    cursor.execute(f"SELECT email, nome FROM usuarios WHERE id_usuario = '{id}' ")
    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultado


# Listar Todos os Usuários
def listar_usuarios():
    conexao = conectardb()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_usuario, nome, email, idade, profissao, estado FROM usuarios")
    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()
    if resultado:
        return resultado
    else:
        return "Nenhum usuário encontrado."


# Atualizar Usuário
def atualizar_usuario(id, novo_nome, novo_email, nova_senha, nova_idade, nova_profissao, novo_estado):
    conexao = conectardb()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE usuarios
        SET nome = %s, email = %s, senha = %s, idade = %s, profissao = %s, estado = %s
        WHERE id_usuario = %s
    """, (novo_nome, novo_email, nova_senha, nova_idade, nova_profissao, novo_estado, id))
    conexao.commit()
    cursor.close()
    conexao.close()
    return buscar_usuario_id(id)


# Deletar Usuário
def deletar_usuario(id):
    conexao = conectardb()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
    conexao.commit()
    cursor.close()
    conexao.close()


def verificar_criador_evento(nome_evento, email_user):

    conexao = conectardb()
    cursor = conexao.cursor()

    try:

        # Consulta SQL para verificar se o usuário é o criador do evento
        cursor.execute("""
            SELECT criador FROM eventos WHERE nome_evento = %s
        """, (nome_evento,))
        criador = cursor.fetchone()
        print(criador[0])

        if criador[0] == email_user:
            print('1')
            return True
        else:
            print('2')
            return False

    except Exception as e:
        print(f"Erro ao verificar criador do evento: {e}")
        return False
    finally:
        cursor.close()
        conexao.close()


def listar_eventos_criados(usuario):
    conexao = conectardb()
    cursor = conexao.cursor()

    cursor.execute("""
                SELECT nome_evento
                FROM eventos
                WHERE criador = %s
            """, (usuario[0][0],))
    eventos = cursor.fetchall()

    return eventos


# DAO refente aos eventos

def verificar_evento_existe(nome_evento):

    conexao = conectardb()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT 1 FROM eventos WHERE nome_evento = %s", (nome_evento,))
        return cursor.fetchone() is not None
    finally:
        cursor.close()
        conexao.close()


def inserir_evento(dados_evento):

    conexao = conectardb()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO eventos 
            (nome_evento, descricao, data_evento, local, valor, cancelavel, idade_minima,
             data_criacao, criador, aberto, codigo_inscricao)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, dados_evento)
        conexao.commit()
        return True
    except Exception as e:
        conexao.rollback()
        print(f"Erro ao cadastrar o evento: {e}")
        return False
    finally:
        cursor.close()
        conexao.close()


def inserir_cupom_e_atualizar_evento(codigo, valor, tipo_desconto, data_expiracao, quantidade_maxima,  nome_evento):

    conexao = conectardb()
    cursor = conexao.cursor()
    try:
        # Inserir o cupom na tabela `cupons`
        cursor.execute("""
            INSERT INTO cupons (codigo, valor, tipo_desconto, data_expiracao, quantidade_maxima, criado_em, nome_evento)
            VALUES (%s, %s, %s, %s, %s, NOW(), %s)
        """, (codigo, valor, tipo_desconto, data_expiracao, quantidade_maxima, nome_evento))

        # Atualizar o evento com o código do cupom
        cursor.execute("""
            UPDATE eventos
            SET cupom_desconto = %s
            WHERE nome_evento = %s
        """, (codigo, nome_evento))

        # Confirmar as operações
        conexao.commit()
        print(f"Cupom '{codigo}' adicionado e o evento {nome_evento} atualizado com sucesso!")

    except Exception as e:
        # Reverter alterações em caso de erro
        conexao.rollback()
        print(f"Erro ao inserir cupom ou atualizar evento: {e}")
        raise
    finally:
        # Fechar a conexão e o cursor
        cursor.close()
        conexao.close()

