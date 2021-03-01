from tkinter import *
import time

class Janela:
    def __init__(self, master=None):
        self.id = 1
        self.contas = {}
        self.master = master
    
        self.container1 = Frame(self.master).grid()

        # Parte do Cadastro
        self.lb_nome = Label(self.container1, text='Apelido: ')
        self.lb_nome.grid(column='0', row='0')

        self.nome_entry = Entry(self.container1)
        self.nome_entry.grid(column='1', row='0')

        self.lb_email = Label(self.container1, text='Email: ' )
        self.lb_email.grid(column='0', row='2')

        self.email_entry = Entry(self.container1)
        self.email_entry.grid(column='1', row='2')

        self.lb_senha = Label(self.container1, text='Senha: ')
        self.lb_senha.grid(column='0', row='3')
        
        self.senha_entry = Entry(self.container1)
        self.senha_entry['show'] = '*'
        self.senha_entry.grid(column='1', row='3')

        self.botao_nome = Button(self.container1, text='Confirmar')
        self.botao_nome['command'] = self.salva_nome
        self.botao_nome.grid(column='1', row='4')

        self.lb_mensagem = Label(self.container1, text='')
        self.lb_mensagem.grid(column='1', row='5')
        
        #Parte do login
        self.lb_login = Label(self.container1, text='Login')
        self.lb_login['font'] = ('Arial', '10', 'bold')
        self.lb_login.grid(column='1', row='6')

        self.login_nome = Label(self.container1, text='Nome: ')
        self.login_nome.grid(column='0', row='7')

        self.login_entry = Entry(self.container1)
        self.login_entry.grid(column='1', row='7')

        self.login_senha = Label(self.container1, text='Senha: ')
        self.login_senha.grid(column='0', row='8')

        self.senha_entry_login = Entry(self.container1)
        self.senha_entry_login['show'] = '*'
        self.senha_entry_login.grid(column='1', row='8')

        self.botao_login = Button(self.container1, text='Conectar')
        self.botao_login['command'] = self.verifica_usuario
        self.botao_login.grid(column='1', row='9')

        self.lb_sucess = Label(self.container1, text='')
        self.lb_sucess.grid(column='1', row='10')

    # Método responsável por pegar campos digitados após click no botão e valida-los.
    def salva_nome(self):
        letras_permitidas = 'abcdefghijklmnopqrstuvwxyz1234567890'
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        # Verificações do campo nome
        if nome == '':
            self.lb_mensagem['text'] = 'Informe um apelido'
            self.lb_mensagem['fg'] = 'red'
            return
        if len(nome) < 6 or len(nome) > 25:
            self.lb_mensagem['text'] = 'Apelido precisa ter entre 8 e 25 caracteres'
            self.lb_mensagem['fg'] = 'red'
            return
        
        for i in nome:
            if not (i in letras_permitidas):
                self.lb_mensagem['text'] = 'Use apenas letras e números no apelido'
                self.lb_mensagem['fg'] = 'red'
                return

        for i in self.contas.values():
            if nome == i[0]:
                self.lb_mensagem['text'] = 'Este usuário já existe'
                self.lb_mensagem['fg'] = 'red'
                return

        # Verificações do campo email
        if email == '':
            self.lb_mensagem['text'] = 'Informe um Email'
            self.lb_mensagem['fg'] = 'red'
            return
        if not('@' in email):
            self.lb_mensagem['text'] = 'Informe um Email válido'
            self.lb_mensagem['fg'] = 'red'
            return

        arroba = 0
    
        for i in email:
            if i == '@':
                arroba += 1

        if arroba > 1 or arroba < 1:
            self.lb_mensagem['text'] = 'Informe um Email válido'
            self.lb_mensagem['fg'] = 'red'
            return

        index_arroba = email.index('@')
        dominio = email[index_arroba+1::]
        ponto = 0
        print(dominio)
        for i in dominio:
            if i == '.':
                ponto += 1
        if ponto > 2 or ponto < 1:
            self.lb_mensagem['text'] = 'Informe um Email válido'
            self.lb_mensagem['fg'] = 'red'
            return

        # Verificações do campo senha
        if senha == '':
            self.lb_mensagem['text'] = 'Informe uma senha'
            self.lb_mensagem['fg'] = 'red'
            return

        tem_numerico = False
        tem_caractere_especial = False
        for i in senha:
            if i in '1234567890':
                tem_numerico = True
            if i in '!@#$%&*':
                tem_caractere_especial = True

        if not(tem_numerico and tem_caractere_especial):
            self.lb_mensagem['text'] = 'senha precisa conter números e simbolos(!@#$%&*)'
            self.lb_mensagem['fg'] = 'red'
            return  

        if len(senha) < 8:
            self.lb_mensagem['text'] = 'senha precisa ter 8 caracteres'
            self.lb_mensagem['fg'] = 'red'
            return

        self.contas[self.id] = [nome, email, senha]
        self.id += 1
        for i in self.contas:
            print(self.contas[i])
        
        self.nome_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.senha_entry.delete(0, 'end')
        self.lb_mensagem['fg'] = 'green'
        self.lb_mensagem['text'] = 'Conta criada as: '
        self.horario_log()

    def verifica_usuario(self):
        login = self.login_entry.get()
        senha = self.senha_entry_login.get()

        for i in self.contas:
            if (self.contas[i][0] == login) and (self.contas[i][2] == senha):
                self.lb_sucess['text'] = 'Você está logado'
                self.lb_sucess['fg'] = 'green'
            elif (self.contas[i][0] == login):
                self.lb_sucess['text'] = 'Senha incorreta'
                self.lb_sucess['fg'] = 'red'
            else:
                self.lb_sucess['text'] = 'Usuario inexistente'
                self.lb_sucess['fg'] = 'red'
                
    # Método que diz o horário da conta  criada.
    def horario_log(self):
        hora = time.strftime("%H")
        minuto = time.strftime("%M")
        segundo = time.strftime("%S")
        self.lb_mensagem.config(text=self.lb_mensagem['text'] + f'{hora}:{minuto}:{segundo}')
    

janela = Tk()
janela.title('Cadastro')
janela.geometry('450x300+800+300')
Janela(janela)
janela.mainloop()