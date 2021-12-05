from PyQt5 import uic, QtWidgets
import sys
import conexao_bd


#Janela Gerenciamento de matriculas
def pesquisar():
    # atualizando todos os registros
    if tela_cadastro.radioButton_5.isChecked():
        tela_cadastro.lineEdit.setText('')
        atualiza_tabela_principal()
        return

    # Verificando se o texto da caixa pesquisa esta vazio
    pesquisa = tela_cadastro.lineEdit.text()
    if pesquisa == '':
        QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'Por favor digite um valor para a pesquisa')
        return
    
    ##Radio button id aluno(validações para poder consultar banco de dados)
    if tela_cadastro.radioButton.isChecked():
        id_aluno = pesquisa
        try:
            id_aluno = int(id_aluno)
        except:
            QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'Por favor digite um valor inteiro para pesquisar por id')
            return
        if id_aluno < 1 or id_aluno > 300:
            QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'Por favor digite um id válido')
            return
        
        # Pesquisa no banco de dados
        rows = conexao_bd.read_one_id(id_aluno)
        if rows == None:
            QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'Valor não encontrado na tabela')
            return

        limpa_tabela(len(rows))
        for i in range(len(rows)): #linha
            for j in range(len(rows[0])): #coluna
                item = QtWidgets.QTableWidgetItem(f"{rows[i][j]}")
                tela_cadastro.tableWidget.setItem(i,j, item)
    ## Fim radio button id aluno

    ## Radio button matricula ativa (Validações para consultar banco de dados)
    if tela_cadastro.radioButton_2.isChecked():
        matricula_ativa = pesquisa
        try:
            matricula_ativa = int(matricula_ativa)
        except:
            QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'Por favor digite um valor inteiro para pesquisar por matricula')
            return
        if matricula_ativa > 1 or matricula_ativa < 0:
            QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'Por favor digite um valor de matrícula válido')
            return

        # Pesquisa no banco de dados
        rows = conexao_bd.read_matricula_ativa(matricula_ativa)
        if rows == None:
            QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'Valor não encontrado na tabela')
            return
        
        limpa_tabela(len(rows))
        for i in range(len(rows)): #linha
            for j in range(len(rows[0])): #coluna
                item = QtWidgets.QTableWidgetItem(f"{rows[i][j]}")
                tela_cadastro.tableWidget.setItem(i,j, item)
        ## Fim radio button matricula ativa

    ## Radio button tipo da matricula (Validações para consultar banco de dados)
    if tela_cadastro.radioButton_3.isChecked():
        tipo_matricula = pesquisa
        try:
            tipo_matricula = int(tipo_matricula)
        except:
            QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'Por favor digite um valor inteiro para pesquisar tipo da matrícula')
            return

        matriculas_validas = [30, 90, 180, 360]
        if tipo_matricula not in matriculas_validas:
            QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'Por favor digite um valor de tipo de matrícula válido')
            return

        # Pesquisa no banco de dados
        rows = conexao_bd.read_tipo_matricula(tipo_matricula)
        if rows == None:
            QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'Valor não encontrado na tabela')
            return
        
        limpa_tabela(len(rows))
        for i in range(len(rows)): #linha
            for j in range(len(rows[0])): #coluna
                item = QtWidgets.QTableWidgetItem(f"{rows[i][j]}")
                tela_cadastro.tableWidget.setItem(i,j, item)
    ## Fim radio button tipo da matricula.

    # Radio button data inicio (validações para consultar banco de dados)
    if tela_cadastro.radioButton_4.isChecked():
        data_inicio = pesquisa.split('-')
        print(data_inicio)
        if len(data_inicio) != 3:
            QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'Formato inválido. Pesquisa a data no formato: aaaa-mm-dd')
            return

        try:
            teste1 = len(data_inicio[0])
            teste2 = len(data_inicio[1])
            teste3 = len(data_inicio[2])
        except:
            QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'Formato inválido. Use apenas números para pesquisar por data de inicio')
            return

        if teste1 != 4:
            QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'O ano precisa ter 4 digitos')
            return
        if teste2 != 2:
            QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'O mês precisa ter 2 digitos')
            return
        if teste3 != 2:
            QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'O dia precisa ter 2 digitos')
            return    

        try:
            ano = int(data_inicio[0])
            mes = int(data_inicio[1])
            dia = int(data_inicio[2])
        except:
            QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'Formato inválido. Use apenas números para pesquisar por data de inicio')
            return

        rows = conexao_bd.read_data_inicio(f'{data_inicio[0]}-{data_inicio[1]}-{data_inicio[2]}')
        if rows == None:
            QtWidgets.QMessageBox.about(tela_cadastro, 'Alerta', 'Valor não encontrado na tabela')
            return
        
        limpa_tabela(len(rows))
        for i in range(len(rows)): #linha
            for j in range(len(rows[0])): #coluna
                item = QtWidgets.QTableWidgetItem(f"{rows[i][j]}")
                tela_cadastro.tableWidget.setItem(i,j, item)

    # Radio button nome do aluno(validações para consulta do banco de dados)
    if tela_cadastro.radioButton_6.isChecked():
        pesquisa = tela_cadastro.lineEdit.text()
        rows = conexao_bd.read_nome_aluno(pesquisa)
        print('chego')
        limpa_tabela(len(rows))
        for i in range(len(rows)): #linha
            for j in range(len(rows[0])): #coluna
                item = QtWidgets.QTableWidgetItem(f"{rows[i][j]}")
                tela_cadastro.tableWidget.setItem(i,j, item)


def limpa_tabela(valor):
    # Valor é o valor de linhas que terá a tabela
    if valor == 1:
        tela_cadastro.tableWidget.setRowCount(1)
        tela_cadastro.tableWidget.setColumnCount(len(conexao_bd.read_all()[0]))
        tela_cadastro.tableWidget.setHorizontalHeaderLabels(["id aluno","nome do aluno", "matricula ativa", "tipo matricula", "data inicio", "data fim"])
    else:
        tela_cadastro.tableWidget.setRowCount(valor)
        tela_cadastro.tableWidget.setColumnCount(len(conexao_bd.read_all()[0]))
        tela_cadastro.tableWidget.setHorizontalHeaderLabels(["id aluno","nome do aluno", "matricula ativa", "tipo matricula", "data inicio", "data fim"])


def voltar():
    tela_inserir_matriculas.close()
    tela_cadastro.close()

def atualiza_tabela_principal():
    # Setando numero de linhas, colunas e nome das colunas
    tela_cadastro.tableWidget.setRowCount(len(conexao_bd.read_all()))
    tela_cadastro.tableWidget.setColumnCount(len(conexao_bd.read_all()[0]))
    tela_cadastro.tableWidget.setHorizontalHeaderLabels(["id aluno","nome do aluno", "matricula ativa", "tipo matricula", "data inicio", "data fim"])

    # Inserindo os dados na tabela
    rows = conexao_bd.read_all()

    for i in range(len(rows)): #linha
        for j in range(len(rows[0])): #coluna
            item = QtWidgets.QTableWidgetItem(f"{rows[i][j]}")
            tela_cadastro.tableWidget.setItem(i,j, item)
# Fim janela janela gerenciamento de matriculas

# Janela inserir
def abrir_janela_inserir():
    tela_inserir_matriculas.show()

def fechar_janela_inserir():
    atualiza_tabela_principal()
    tela_inserir_matriculas.lineEdit.setText('')
    tela_inserir_matriculas.lineEdit_2.setText('')
    tela_inserir_matriculas.lineEdit_3.setText('')
    tela_inserir_matriculas.lineEdit_4.setText('')
    tela_inserir_matriculas.close()

def inserir_dados():
    # Parte de teste para verificar se os dados são válidos
    tipos_de_matriculas = [30, 90, 180, 360]
    numeros = '123456789'
    carcteres_especiais = "!@#$%¨&*()-=+[]"
    try:
        # Resgatando o valor dos campos de texto da janela inserir
        id_aluno = tela_inserir_matriculas.lineEdit.text()
        matricula_ativa = tela_inserir_matriculas.lineEdit_2.text()
        tipo_matricula = tela_inserir_matriculas.lineEdit_3.text()
        nome_aluno = tela_inserir_matriculas.lineEdit_4.text()

        # Verificando se os 3 campos da janela inserir estão vazios
        if matricula_ativa == '' or id_aluno == '' or tipo_matricula == '':
            QtWidgets.QMessageBox.about(tela_inserir_matriculas, 'Erro', 'Por favor preencha todos os campos antes de inserir')
            return

        # Verificando se o id do aluno está entre 1 e 300
        id_aluno = int(id_aluno)
        if id_aluno < 1 or id_aluno > 300:
            QtWidgets.QMessageBox.about(tela_inserir_matriculas, 'Erro', 'Por favor insira um id de aluno válido')
            return

        # Verificando se o valor de matricula ativa é valido
        matricula_ativa = int(matricula_ativa)
        if matricula_ativa > 1 or matricula_ativa < 0:
            QtWidgets.QMessageBox.about(tela_inserir_matriculas, 'Erro', 'Por favor insira um valor válido para o campo matricula ativa')
            return

        # Verificando se o valor pego existe na minha lista com matriculas válidas.
        tipo_matricula = int(tipo_matricula)
        if tipo_matricula not in tipos_de_matriculas:
            QtWidgets.QMessageBox.about(tela_inserir_matriculas, 'Erro', 'Por favor insira um valor válido para o campo tipo matricula')
            return

        
        lista_nome_aluno = []
        for i in nome_aluno:
            lista_nome_aluno.append(i)

        for i in numeros:
            if i in lista_nome_aluno:
                QtWidgets.QMessageBox.about(tela_inserir_matriculas, 'Erro', 'Por favor não insira números para registrar o nome do aluno')
                return
        print(nome_aluno)
        for j in carcteres_especiais:
            if j in nome_aluno:
                QtWidgets.QMessageBox.about(tela_inserir_matriculas, 'Erro', 'Por favor não use carctéres especiais para registrar o nome do aluno')
                return


        
    except Exception:
        QtWidgets.QMessageBox.about(tela_inserir_matriculas, 'Erro', 'Insira apenas números')
        return
    #Fim dos testes

    # Parte da inserção no banco de dados
    resposta = conexao_bd.insert(int(id_aluno), nome_aluno, int(matricula_ativa), int(tipo_matricula))
    atualiza_tabela_principal()
    QtWidgets.QMessageBox.about(tela_inserir_matriculas, 'Conexão banco de dados', resposta)
    
    return  
# Fim janela inserir

# Janela de atualizar dados
def abrir_janela_atualizar():
    tela_atualizar.show()

def fechar_janela_atualizar():
    atualiza_tabela_principal()
    tela_atualizar.lineEdit.setText('')
    tela_atualizar.lineEdit_2.setText('')
    tela_atualizar.lineEdit_3.setText('')
    tela_atualizar.lineEdit_4.setText('')
    tela_atualizar.close()


def atualizar_dados():
    tipos_de_matriculas = [30, 90, 180, 360]
    numeros = '123456789'
    carcteres_especiais = "!@#$%¨&*()-=+[]"
    try:
        # resgatando os valores do campos de texto da tela atualizar
        id_aluno = tela_atualizar.lineEdit.text()
        matricula_ativa = tela_atualizar.lineEdit_2.text()
        tipo_matricula = tela_atualizar.lineEdit_3.text()
        nome_aluno = tela_atualizar.lineEdit_4.text()

        # Verificando se os 3 campos da janela inserir estão vazios
        if matricula_ativa == '' or id_aluno == '' or tipo_matricula == '':
            QtWidgets.QMessageBox.about(tela_atualizar, 'Erro', 'Por favor preencha todos os campos antes de atualizar')
            return

        # Verificando se o id do aluno está entre 1 e 300
        id_aluno = int(id_aluno)
        if id_aluno < 1 or id_aluno > 300:
            QtWidgets.QMessageBox.about(tela_atualizar, 'Erro', 'Por favor insira um id de aluno válido')
            return

        # Verificando se o valor de matricula ativa é valido
        matricula_ativa = int(matricula_ativa)
        if matricula_ativa > 1 or matricula_ativa < 0:
            QtWidgets.QMessageBox.about(tela_atualizar, 'Erro', 'Por favor insira um valor válido para o campo matricula ativa')
            return

        # Verificando se o valor pego existe na minha lista com matriculas válidas.
        tipo_matricula = int(tipo_matricula)
        if tipo_matricula not in tipos_de_matriculas:
            QtWidgets.QMessageBox.about(tela_atualizar, 'Erro', 'Por favor insira um valor válido para o campo tipo matricula')
            return

        
        lista_nome_aluno = []
        for i in nome_aluno:
            lista_nome_aluno.append(i)

        for i in numeros:
            if i in lista_nome_aluno:
                QtWidgets.QMessageBox.about(tela_atualizar, 'Erro', 'Por favor não insira números para atualizar o nome do aluno')
                return
        print(nome_aluno)
        for j in carcteres_especiais:
            if j in nome_aluno:
                QtWidgets.QMessageBox.about(tela_atualizar, 'Erro', 'Por favor não use carctéres especiais para atualizar o nome do aluno')
                return


        
    except Exception:
        QtWidgets.QMessageBox.about(tela_atualizar, 'Erro', 'Insira apenas números')
        return
    #Fim dos testes

    # Parte da inserção no banco de dados
    resposta = conexao_bd.update_table(int(matricula_ativa), nome_aluno,  int(tipo_matricula),int(id_aluno))
    atualiza_tabela_principal()
    QtWidgets.QMessageBox.about(tela_atualizar, 'Conexão banco de dados', 'Atualização feita com sucesso')
    
    return  
#Fim janela atualizar

# Janela excluir
def abrir_janela_excluir():
    tela_excluir.show()

def fechar_janela_excluir():
    atualiza_tabela_principal()
    tela_excluir.lineEdit.setText('')
    tela_excluir.close()

def excluir_dados():
    try:
        id_aluno = tela_excluir.lineEdit.text()
        id_aluno = int(id_aluno)
        if id_aluno < 1 or id_aluno > 300:
            QtWidgets.QMessageBox.about(tela_excluir, 'Erro', 'Por favor insira um id de aluno válido')
            return
        response = conexao_bd.read_one_id(id_aluno)
        if response == None:
            QtWidgets.QMessageBox.about(tela_excluir, 'Erro', 'Falha ao excluir, id inexistente na tabela')
            return

    except Exception:
        QtWidgets.QMessageBox.about(tela_excluir, 'Erro', 'Insira apenas números')
        return

    # Parte da inserção no banco de dados
    resposta = conexao_bd.delete(id_aluno)
    atualiza_tabela_principal()
    QtWidgets.QMessageBox.about(tela_excluir, 'Conexão banco de dados', 'Registro excluido com sucesso')
    
    return  



# Carregando minhas janelas que serão usadas
app = QtWidgets.QApplication(sys.argv)
tela_cadastro = uic.loadUi('tela_cadastro.ui')
tela_inserir_matriculas = uic.loadUi('inserir_dados.ui')
tela_atualizar = uic.loadUi('atualizar_dados.ui')
tela_excluir = uic.loadUi('tela_excluir.ui')



# Conectando os botoes da janela principal as funções da janela principal
tela_cadastro.pushButton_2.clicked.connect(abrir_janela_inserir)
tela_cadastro.pushButton_7.clicked.connect(pesquisar)
tela_cadastro.pushButton_3.clicked.connect(abrir_janela_atualizar)
tela_cadastro.pushButton_5.clicked.connect(voltar)
tela_cadastro.pushButton_4.clicked.connect(abrir_janela_excluir)

# Conectando os botões da janela de inserir as funções da janela de inserir
tela_inserir_matriculas.pushButton_2.clicked.connect(fechar_janela_inserir)
tela_inserir_matriculas.pushButton.clicked.connect(inserir_dados)

# Conectando os botões da jenala atualizar as funções da janela atualizar
tela_atualizar.pushButton_2.clicked.connect(fechar_janela_atualizar)
tela_atualizar.pushButton.clicked.connect(atualizar_dados)

# Conectando os botões da janela excluir as funções da janela excluir
tela_excluir.pushButton_2.clicked.connect(fechar_janela_excluir)
tela_excluir.pushButton.clicked.connect(excluir_dados)

atualiza_tabela_principal()

