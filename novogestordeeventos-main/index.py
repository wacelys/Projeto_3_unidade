from auth import *
from menu_usuario import menu_usuario
from dao import *


def menu_login():
    while True:
        print('1-Cadastrar usuário')
        print('2-Login')
        print('0-Sair do programa')

        op = input('Digite a opção desejada: ')
        if op == '1':
            nome = input('Digite seu nome: ')
            email = input('Digite seu e-mail: ')
            while not verificar_email(email):
                print("Certifique-se de digitar um email válido com '@' e '.com'")
                email = input("Digite novamente seu e-mail: ")
            while verificar_user_existente(email):
                email = input('E-mail já cadastrado. Digite novamente seu e-mail: ')
            print("Email válido.")

            senha = input('Digite sua senha: ')
            senha2 = input('Repita sua senha: ')
            while not verificar_senha(senha, senha2):
                print('Senhas diferentes. Tente novamente.')
                senha = input('Digite sua senha: ')
                senha2 = input('Repita sua senha: ')

            idade = int(input('Inisira sua idade: '))
            while idade <= 0:
                idade = int(input('Idade inválida, Insira sua idade: '))

            profissao = input('Insira sua profissão: ')

            estado = input('Insira a sigla do estado em que você vive: ')

            genero = input('Insira seu gênero: (F/M), caso não queira informar digite N: ')
            while genero not in ['F', 'M', 'N']:
                genero = input('Insira seu gênero: (F/M), caso não queira informar digite N.')

            if inserir_usuario(nome, email, senha, idade, profissao, estado, genero):
                print('Usuário cadastrado com sucesso!')
            else:
                print('Erro ao inserir usuario!')

        elif op == '2':
            email = input('Digite o seu email: ')
            while not verificar_email(email):
                email = input("Digite um email válido, com '@' e '.com': ")

            senha = input('Digite a sua senha: ')

            usuario = login_db(email, senha)
            if usuario:
                print(usuario)
                menu_usuario(usuario)
            else:
                print('Login inválido, tente novamente')

        elif op == '0':
            print('_______________________\n'
                  'See you soon\n'
                  '_______________________')
            break
        else:
            print('INSIRA UMA OPÇÃO VÁLIDA')


if __name__ == '__main__':
    menu_login()
