################################################################################
##
## Feito por: FiveTech
## PROJETO FEITO COM: Qt Designer e PyQt5
## LIBS USADAS:  MatplotLib, bcrypt, PyQt5, API google, Threding
## V: 1.0.0
## Compilação deste executavel:  *     Seu path até a pasta Novteste            *
## pyinstaller --onefile --paths C:\Users\ITGREEN\Desktop\repofacul\FiveTech-OPE\Novteste\env\Lib\site-packages main.py
##
################################################################################

import threading
import sys
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QColor, QKeyEvent, QRegExpValidator
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDateTime, QRegExp, QEvent, QThread, Qt
from src.utils import compara_datas2, formato_iso_para_br, formato_br_para_iso, compara_datas, advinha_tipo_arquivo
from src.estilo import DISABLED_INPUT, ENABLED_INPUT, ESTILO_DATA, ESTILO_DATA2, ESTILO_LINEEDIT, ESTILO_COMBOBOX \
,FAILED_LOGIN, HTML_PLACEHOLDER, SUCESS_LOGIN, MENSAGEM_SUCESSO
import src.Resources_qrc
import matplotlib.pyplot
import google
import src.database as db
import bcrypt
import src.envia_email as google
import os
import requests as rq
import src.custom_erros as erros
import src.validacoes as validacoes
import string
import validate_email
import time
import datetime as dt
import re
from src.fabrica_pdf import PDF
#from src.loadspinner import Loadspinner
from src.texteditor import *
from copy import copy
from random import choice

## ==> GLOBALS
counter = 0
conectado_ao_google = 0  #0 para desconectado e 1 para conectado
conta_google = None
tabela_alunos = [()]
tabela_avfisica = [()]  
tabela_matriculas = [()]
tabela_estoque = [()]
tabela_despesas = [()]


## CLASSES ##
class JanelaPrincipal(QMainWindow):
    anexos = {}
    confirmacao_do_anexo = {}
    def __init__(self):
        super().__init__()
        ### CONFIGURANDO JANELA E CRIANDO OBJETOS DE OUTRAS JANELAS ###
        self.janela_principal = uic.loadUi('src\\telas\\telas_principais\\tela_principal.ui')
        self.confirmacao_do_email = uic.loadUi('src\\telas\\telas_principais\\confirma_email.ui')
        self.confirmacao_do_anexo = uic.loadUi('src\\telas\\telas_principais\\confirma_anexo.ui')
        self.pesquisa_alunos = uic.loadUi('src\\telas\\telas_principais\\pesquisar_alunos_email.ui')
        self.tela_sobre = uic.loadUi('src\\telas\\telas_principais\\sobre_gerenciador2.ui')
        self.tela_login = JanelaLogin()
        self.tela_login.janela_login.show()
        #self.janela_principal.show()
        self.tela_matriculas = JanelaMatriculas()
        self.tela_alunos = JanelaAlunos()
        self.tela_estoque = JanelaEstoque()
        self.tela_despesas = JanelaDespesas()
        #self.spinner = Loadspinner()
        ### TELA DE ANEXOS ###
        self.programa = uic.loadUi('src\\telas\\telas_principais\\tela_anexo_email.ui')
        self.janela_principal.btnAnexarArquivo.clicked.connect(lambda: self.programa.show())
        self.programa.pushButton.clicked.connect(lambda: self.programa.close())
        self.programa.escolher_arquivo.clicked.connect(lambda: self.seleciona_arquivo())
        self.qtd_anexos = 0

        self.fontSizeBox = QSpinBox()

        toolbar = self.create_tool_bar()
        vbox = QHBoxLayout()
       # vbox.addStretch(1)
        vbox.addWidget(toolbar)
        self.janela_principal.frame_botoes.setLayout(vbox)
        
        ### MANIPULANDO O CARREGAMENTO DAS TABELAS COM O THREADING ###
        self.starta_threads()

        ### CARREGANDO OS DADOS DAS JANELAS ###
        self.janela_principal.botao_matriculas.clicked.connect(lambda: self.abre_janela_matriculas(tabela_matriculas))
        self.janela_principal.botao_alunos.clicked.connect(lambda: self.abre_janela_alunos(tabela_alunos))
        self.janela_principal.botao_estoque.clicked.connect(lambda:self.abre_janela_estoque(tabela_estoque))
        self.janela_principal.botao_orcamento.clicked.connect(lambda: self.abre_janela_despesas(tabela_despesas))
        self.janela_principal.pushButton_9.clicked.connect(lambda:self.tela_sobre.show())
        self.tela_sobre.pushButton_2.clicked.connect(lambda:self.tela_sobre.close())
        self.tela_sobre.pushButton.clicked.connect(lambda:self.tela_sobre.stackedWidget.setCurrentIndex(0))
        self.tela_sobre.pushButton_5.clicked.connect(lambda:self.tela_sobre.stackedWidget.setCurrentIndex(1))
        self.tela_sobre.pushButton_6.clicked.connect(lambda:self.tela_sobre.stackedWidget.setCurrentIndex(3))

        ### MANIPULANDO OUTROS EVENTOS ###
        self.janela_principal.btn_google.clicked.connect(self.conecta_conta_google)
        self.janela_principal.destroyed.connect(lambda: self.destroi_arquivo_pikle())
        self.janela_principal.pushButton_8.clicked.connect(self.tela_enviar_email)
        self.janela_principal.botaoAtt.clicked.connect(lambda: self.gera_graficos(tabela_alunos, tabela_matriculas,
        tabela_avfisica, tabela_estoque, tabela_despesas))
        #self.abre_graficos()

        ###TESTE DO STACKEDWIDGET ###
        #self.janela_principal.pushButton_9.clicked.connect(lambda: self.slideInNext())
        self.janela_principal.btn_volta.clicked.connect(lambda: self.slideInPrev())
        self.m_direction = QtCore.Qt.Horizontal
        self.m_speed = 1000
        self.m_animationtype = QtCore.QEasingCurve.OutCubic
        self.m_now = 0
        self.m_next = 0
        self.m_wrap = False
        self.m_pnow = QtCore.QPoint(0, 0)
        self.m_active = False

        ### GERANDO E ATUALIZANDO GRAFICOS###
        if tabela_alunos != [()] or tabela_matriculas != [()] or tabela_avfisica != [()]:
            if tabela_estoque != [()] or tabela_despesas != [()]:
                self.gera_graficos(tabela_alunos, tabela_matriculas,
                            tabela_avfisica, tabela_estoque, tabela_despesas)
 
        self.janela_principal.frame_6.setStyleSheet(f"background-image: url('dados_gerais.png');\
                                background-color: rgb(39, 39, 39); background-repeat: no-repeat;")
        self.abre_widget() 


        self.janela_principal.tab_dashboard.currentChanged.connect(self.coloca_grafico_na_tela)
        
        ## WIDGETS JANELA PRINCIPAL ##
        self.janela_principal.tab_dashboard.setTabText(0, 'Geral')
        self.janela_principal.tab_dashboard.setTabText(1, 'Despesas')
        self.janela_principal.tab_dashboard.setTabText(2, 'Estoque')
        self.janela_principal.tab_dashboard.setTabText(3, 'Matrículas')
        self.janela_principal.tab_dashboard.setTabText(4, 'Alunos')
        self.janela_principal.tab_dashboard.setCurrentIndex(0)
        threading.Thread(target=self.abre_graficos()).start()

        ### ENVIAR EMAIL ###
        self.janela_principal.enviarEmailBtn.clicked.connect(lambda: self.envia_email_confirmacao())
        self.janela_principal.cancelarEmailBtn.clicked.connect(lambda: self.cancela_envio_email())
        self.janela_principal.btnPesquisarAlunos.clicked.connect(lambda: self.abrir_janela_pesquisar_alunos())
        self.pesquisa_alunos.btn_fechar.clicked.connect(lambda: self.pesquisa_alunos.close())
        self.pesquisa_alunos.btn_selecionar.clicked.connect(lambda: self.selecionar_emails_dos_alunos())

        self.confirmacao_do_email.closeEvent = self.destroi_janela_confirm_email
        self.confirmacao_do_email.btnCancelarConfirmacao.clicked.connect(lambda: self.destroi_janela_confirm_email())
        self.confirmacao_do_email.btnEnviarConfirmacao.clicked.connect(lambda: self.envia_email())
        self.confirmacao_do_email.pushButton.clicked.connect(lambda: self.confirmacao_do_anexo.show())
        self.confirmacao_do_anexo.pushButton.clicked.connect(lambda: self.confirmacao_do_anexo.close())
        

        ### MENU HAMBURGUER ###
        self.janela_principal.botao_menu.clicked.connect(self.ativa_menu_hamburguer)
        self.janela_principal.relatorio1.clicked.connect(self.gerador_de_pdf_matricula)
        self.janela_principal.relatorio2.clicked.connect(self.gerador_de_pdf_aluno)
        self.janela_principal.relatorio3.clicked.connect(self.gerador_de_pdf_estoque)
        self.janela_principal.relatorio4.clicked.connect(self.gerador_de_pdf_despesas)

    #### MÉTODO DA JENALA DE PESQUISAR ALUNOS ####
    def abrir_janela_pesquisar_alunos(self):
        global tabela_alunos
        tabela = tabela_alunos
        self.pesquisa_alunos.show()
        self.pesquisa_alunos.tabelaAlunos.setRowCount(len(tabela))
        self.pesquisa_alunos.tabelaAlunos.setColumnCount(len(tabela[0])-1)
        self.pesquisa_alunos.tabelaAlunos.setHorizontalHeaderLabels(["Nome", "Idade", "Cpf", "Telefone", "Email"])
        self.pesquisa_alunos.tabelaAlunos.resizeRowsToContents()
        for i in range(len(tabela)): #linha
            for j in range(len(tabela[0])): #coluna
                if j == 5: break
                item = QtWidgets.QTableWidgetItem(f"{tabela[i][j+1]}")

                self.pesquisa_alunos.tabelaAlunos.setItem(i,j, item)
        ## Reajustando o tamnho das células(colunoas) de acordo com o contúdo delas
        header = self.pesquisa_alunos.tabelaAlunos.horizontalHeader()           # Colunas abaixo  
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)# Nome
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)# Cpf
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)# Número tel
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)# Email

    def selecionar_emails_dos_alunos(self):
        dados = set(index.row() for index in self.pesquisa_alunos.tabelaAlunos.selectedIndexes())
        emails = []
        for i in dados:
            emails.append((self.pesquisa_alunos.tabelaAlunos.item(i, 4).text()))
        print(emails)
        string = ""
        for email in emails:
            string += email + ";"
        self.janela_principal.destinatario.setText(string)
        self.pesquisa_alunos.close()

    #### MÉTODOS DA JANELA DE ANEXOS ####
    def seleciona_arquivo(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        diretorio, _ = QFileDialog.getOpenFileName(self,"Selecione o arquivo que será anexado",
        "","All Files (*);;Python Files (*.py)", options=options)
        # if fileName:
        #     print(fileName)
        # diretorio = QFileDialog.getExistingDirectory(self,
        # 'Selecione o arquivo que será enviado como anexo', 'C:\\', QFileDialog.ShowDirsOnly)
        if not diretorio:
            return
        print(diretorio)
        print(diretorio.split("/")[-1])
        nome_arquivo = diretorio.split("/")[-1]
        tipo_arquivo = advinha_tipo_arquivo(diretorio)
        print(tipo_arquivo)
        
        self.gera_anexo_widget(tipo_arquivo, nome_arquivo, diretorio)
        #print(JanelaPrincipal.anexos)

    def gera_anexo_widget(self, tipo_arquivo, nome_arquivo, path_arquivo):
        ### tela anexo ###
        frame_3 = QFrame()
        frame_3.setObjectName(u"frame_3")
        frame_3.setMinimumSize(QSize(0, 137))
        frame_3.setMaximumSize(QSize(16777215, 137))
        frame_3.setStyleSheet(u"background-color: rgb(20, 20, 20);")
        frame_3.setFrameShape(QFrame.StyledPanel)
        frame_3.setFrameShadow(QFrame.Raised)
        horizontalLayout_2 = QHBoxLayout(frame_3)
        horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        foto_anexo = QLabel(frame_3)
        foto_anexo.setObjectName(u"foto_anexo")
        foto_anexo.setMaximumSize(QSize(100, 16777215))
        foto_anexo.setStyleSheet(u"\n"
                                    "color: rgb(217, 217, 217);\n"
                                    "font-size:18px;")
        if tipo_arquivo == "python":
            foto_anexo.setPixmap(QPixmap(u"src/Icons/28884.png"))
        if tipo_arquivo == "excel":
            foto_anexo.setPixmap(QPixmap(u"src/Icons/excel.png"))
        if tipo_arquivo == "pdf":
            foto_anexo.setPixmap(QPixmap(u"src/Icons/pdf.png"))
        if tipo_arquivo == "text":
            foto_anexo.setPixmap(QPixmap(u"src/Icons/txt.png"))
        if tipo_arquivo == "image":
            foto_anexo.setPixmap(QPixmap(u"src/Icons/image.png"))
        if tipo_arquivo == "audio":
            foto_anexo.setPixmap(QPixmap(u"src/Icons/audio.png"))
        if tipo_arquivo == "arquivo":
            foto_anexo.setPixmap(QPixmap(u"src/Icons/file.png"))
        foto_anexo.setScaledContents(True)
        horizontalLayout_2.addWidget(foto_anexo)

        img_anexo = QLabel(frame_3)
        img_anexo.setObjectName(u"img_anexo")
        img_anexo.setStyleSheet(u"\n"
                                        "color: rgb(217, 217, 217);\n"
                                        "font-size:18px;")
        img_anexo.setAlignment(Qt.AlignCenter)
        img_anexo.setText(str(nome_arquivo))

        horizontalLayout_2.addWidget(img_anexo)

        

        excluir_anexo = QPushButton(frame_3)
        excluir_anexo.setObjectName(u"excluir_anexo")
        excluir_anexo.setMaximumSize(QSize(150, 80))
        excluir_anexo.setStyleSheet(u"""
                                QPushButton{
                                background-color: 
                                qlineargradient(spread:pad, x1:0, y1:0.017, x2:1, y2:1, stop:0.113636 rgba(0, 129, 0, 255), stop:1 rgba(66, 138, 60, 255));
                                border-radius:10px;
                                text-align: center;
                                color: #ffffff;
                                font-size:20px;
                                font-weight:bold;
                                }
                                QPushButton:hover{
                                background-color: rgb(36, 199, 31);
                                }
                                QPushButton:pressed{
                                background-color: #3e8e41;
                                }""")
        icon1 = QIcon()
        icon1.addFile(u"src/Icons/white_versions/output-onlinepngtools (10)", QSize(), QIcon.Normal, QIcon.Off)
        excluir_anexo.setIcon(icon1)
        excluir_anexo.setIconSize(QSize(20, 20))
        excluir_anexo.setText("Excluir")

        horizontalLayout_2.addWidget(excluir_anexo)

        ### tela confirmação anexo ###
        frame_4 = QFrame()
        frame_4.setObjectName(u"frame_3")
        frame_4.setMinimumSize(QSize(0, 137))
        frame_4.setMaximumSize(QSize(16777215, 137))
        frame_4.setStyleSheet(u"background-color: rgb(20, 20, 20);")
        frame_4.setFrameShape(QFrame.StyledPanel)
        frame_4.setFrameShadow(QFrame.Raised)
        horizontalLayout_3 = QHBoxLayout(frame_4)
        horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        foto_anexo_2 = QLabel(frame_4)
        foto_anexo_2.setObjectName(u"foto_anexo_2")
        foto_anexo_2.setMaximumSize(QSize(100, 16777215))
        foto_anexo_2.setStyleSheet(u"\n"
                                    "color: rgb(217, 217, 217);\n"
                                    "font-size:18px;")
        if tipo_arquivo == "python":
            foto_anexo_2.setPixmap(QPixmap(u"src/Icons/28884.png"))
        if tipo_arquivo == "excel":
            foto_anexo_2.setPixmap(QPixmap(u"src/Icons/excel.png"))
        if tipo_arquivo == "pdf":
            foto_anexo_2.setPixmap(QPixmap(u"src/Icons/pdf.png"))
        if tipo_arquivo == "text":
            foto_anexo_2.setPixmap(QPixmap(u"src/Icons/txt.png"))
        if tipo_arquivo == "image":
            foto_anexo_2.setPixmap(QPixmap(u"src/Icons/image.png"))
        if tipo_arquivo == "audio":
            foto_anexo_2.setPixmap(QPixmap(u"src/Icons/audio.png"))
        if tipo_arquivo == "arquivo":
            foto_anexo_2.setPixmap(QPixmap(u"src/Icons/file.png"))
        foto_anexo_2.setScaledContents(True)
        horizontalLayout_3.addWidget(foto_anexo_2)

        img_anexo_2 = QLabel(frame_4)
        img_anexo_2.setObjectName(u"img_anexo")
        img_anexo_2.setStyleSheet(u"\n"
                                        "color: rgb(217, 217, 217);\n"
                                        "font-size:18px;")
        img_anexo_2.setAlignment(Qt.AlignCenter)
        img_anexo_2.setText(str(nome_arquivo))

        horizontalLayout_3.addWidget(img_anexo_2)
        
        

        self.confirmacao_do_anexo.verticalLayout_3.addWidget(frame_4)
        self.programa.verticalLayout_3.addWidget(frame_3)
        excluir_anexo.clicked.connect(lambda: self.deleta_widget(frame_3, frame_4))
        JanelaPrincipal.anexos[self.qtd_anexos] = [frame_3]
        JanelaPrincipal.anexos[self.qtd_anexos].append(path_arquivo)
        JanelaPrincipal.confirmacao_do_anexo[self.qtd_anexos] = [frame_4]
        self.qtd_anexos += 1
        self.programa.label_3.setText(str(self.qtd_anexos))
        self.confirmacao_do_anexo.label_3.setText(str(self.qtd_anexos))
        self.janela_principal.label_42.setText(f'Anexos ({self.qtd_anexos})')

    def popula_confirmar_anexo(self):
        qtd_de_anexos = len(JanelaPrincipal.anexos)
        self.confirmacao_do_email.label.setText(f"Anexos ({qtd_de_anexos})")
        if qtd_de_anexos == 0:
            self.confirmacao_do_email.pushButton.setEnabled(False)
        for anexo in JanelaPrincipal.anexos:
            nome_arquivo = JanelaPrincipal.anexos[anexo][1].split("/")[-1]
            tipo_arquivo = advinha_tipo_arquivo(JanelaPrincipal.anexos[anexo][1])

            frame_3 = QFrame(self.confirmacao_do_anexo.scrollAreaWidgetContents)
            frame_3.setObjectName(u"frame_3")
            frame_3.setMinimumSize(QSize(0, 137))
            frame_3.setMaximumSize(QSize(16777215, 137))
            frame_3.setStyleSheet(u"background-color: rgb(50, 50, 50);")
            frame_3.setFrameShape(QFrame.StyledPanel)
            frame_3.setFrameShadow(QFrame.Raised)
            horizontalLayout_2 = QHBoxLayout(frame_3)
            horizontalLayout_2.setObjectName(u"horizontalLayout_2")
            foto_anexo = QLabel(frame_3)
            foto_anexo.setObjectName(u"foto_anexo")
            foto_anexo.setMaximumSize(QSize(100, 16777215))
            foto_anexo.setStyleSheet(u"\n"
                                        "color: rgb(217, 217, 217);\n"
                                        "font-size:18px;")
            if tipo_arquivo == "python":
                foto_anexo.setPixmap(QPixmap(u"src/Icons/28884.png"))
            if tipo_arquivo == "excel":
                foto_anexo.setPixmap(QPixmap(u"src/Icons/excel.png"))
            if tipo_arquivo == "pdf":
                foto_anexo.setPixmap(QPixmap(u"src/Icons/pdf.png"))
            if tipo_arquivo == "text":
                foto_anexo.setPixmap(QPixmap(u"src/Icons/txt.png"))
            if tipo_arquivo == "image":
                foto_anexo.setPixmap(QPixmap(u"src/Icons/image.png"))
            if tipo_arquivo == "audio":
                foto_anexo.setPixmap(QPixmap(u"src/Icons/audio.png"))
            if tipo_arquivo == "arquivo":
                foto_anexo.setPixmap(QPixmap(u"src/Icons/file.png"))


            foto_anexo.setScaledContents(True)

            horizontalLayout_2.addWidget(foto_anexo)

            img_anexo = QLabel(frame_3)
            img_anexo.setObjectName(u"img_anexo")
            img_anexo.setStyleSheet(u"\n"
                                            "color: rgb(217, 217, 217);\n"
                                            "font-size:18px;")
            img_anexo.setAlignment(Qt.AlignCenter)
            img_anexo.setText(str(nome_arquivo))

            horizontalLayout_2.addWidget(img_anexo)

            self.confirmacao_do_anexo.verticalLayout_3.addWidget(frame_3)
            self.confirmacao_do_anexo.label_3.setText(str(len(JanelaPrincipal.anexos)))


    def deleta_widget(self, frame, frame_4):
        frame.deleteLater()
        frame_4.deleteLater()
        self.qtd_anexos -= 1
        self.programa.label_3.setText(str(self.qtd_anexos))
        self.confirmacao_do_anexo.label_3.setText(str(self.qtd_anexos))
        self.janela_principal.label_42.setText(f'Anexos ({self.qtd_anexos})')
        for i in JanelaPrincipal.anexos:
            if JanelaPrincipal.anexos[i][0] is frame:
                print("é")
                del JanelaPrincipal.anexos[i]
                break
        for i in JanelaPrincipal.confirmacao_do_anexo:
            if JanelaPrincipal.confirmacao_do_anexo[i][0] is frame_4:
                print("é")
                del JanelaPrincipal.confirmacao_do_anexo[i]
                break
        print(JanelaPrincipal.anexos)


    #### MÉTODOS E FUNCIONALIDADES DA JANELA PRINCIPAL ####
    def create_tool_bar(self):
        toolbar = QToolBar()
        
        
        undoBtn = QAction(QIcon('src/icons/undo.png'), 'undo', self)
        undoBtn.triggered.connect(self.janela_principal.editor.undo)
        toolbar.addAction(undoBtn)
        
        redoBtn = QAction(QIcon('src/icons/redo.png'), 'redo', self)
        redoBtn.triggered.connect(self.janela_principal.editor.redo)
        toolbar.addAction(redoBtn)
        
        copyBtn = QAction(QIcon('src/icons/copy.png'), 'copy', self)
        copyBtn.triggered.connect(self.janela_principal.editor.copy)
        toolbar.addAction(copyBtn)
        
        cutBtn = QAction(QIcon('src/icons/cut.png'), 'cut', self)
        cutBtn.triggered.connect(self.janela_principal.editor.cut)
        toolbar.addAction(cutBtn)
        
        pasteBtn = QAction(QIcon('src/icons/paste.png'), 'paste', self)
        pasteBtn.triggered.connect(self.janela_principal.editor.paste)
        toolbar.addAction(pasteBtn)
        
        
        self.fontBox = QComboBox(self)
        self.fontBox.addItems(["Courier Std", "Hellentic Typewriter Regular", "Helvetica", "Arial", "SansSerif", "Helvetica", "Times", "Monospace"])
        self.fontBox.activated.connect(self.setFont)
        toolbar.addWidget(self.fontBox)
        
        self.fontSizeBox.setValue(24)
        self.fontSizeBox.valueChanged.connect(self.setFontSize)
        toolbar.addWidget(self.fontSizeBox)
        
        rightAllign = QAction(QIcon('src/icons/right-align.png'), 'Right Allign', self)
        rightAllign.triggered.connect(lambda : self.janela_principal.editor.setAlignment(Qt.AlignRight))
        toolbar.addAction(rightAllign)
        
        leftAllign = QAction(QIcon('src/icons/left-align.png'), 'left Allign', self)
        leftAllign.triggered.connect(lambda : self.janela_principal.editor.setAlignment(Qt.AlignLeft))
        toolbar.addAction(leftAllign)
        
        centerAllign = QAction(QIcon('src/icons/center-align.png'), 'Center Allign', self)
        centerAllign.triggered.connect(lambda : self.janela_principal.editor.setAlignment(Qt.AlignCenter))
        toolbar.addAction(centerAllign)
        
        toolbar.addSeparator()
        
        boldBtn = QAction(QIcon('src/icons/bold.png'), 'Bold', self)
        boldBtn.triggered.connect(self.boldText)
        toolbar.addAction(boldBtn)
        
        underlineBtn = QAction(QIcon('src/icons/underline.png'), 'underline', self)
        underlineBtn.triggered.connect(self.underlineText)
        toolbar.addAction(underlineBtn)
        
        italicBtn = QAction(QIcon('src/icons/italic.png'), 'italic', self)
        italicBtn.triggered.connect(self.italicText)
        toolbar.addAction(italicBtn)
        
        return toolbar  

    def setFontSize(self):
        value = self.fontSizeBox.value()
        self.janela_principal.editor.setFontPointSize(value)
        
    def setFont(self):
        font = self.fontBox.currentText()
        self.janela_principal.editor.setCurrentFont(QFont(font))    
        
    def italicText(self):
        state = self.janela_principal.editor.fontItalic()
        self.janela_principal.editor.setFontItalic(not(state)) 
    
    def underlineText(self):
        state = self.janela_principal.editor.fontUnderline()
        self.janela_principal.editor.setFontUnderline(not(state))   
        
    def boldText(self):
        print(self.janela_principal.editor.toHtml())
        if self.janela_principal.editor.fontWeight != QFont.Bold:
            self.janela_principal.editor.setFontWeight(QFont.Bold)
            return
        self.janela_principal.editor.setFontWeight(QFont.Normal)        

    def setDirection(self, direction):
        self.m_direction = direction

    def setSpeed(self, speed):
        self.m_speed = speed

    def setAnimation(self, animationtype):
        self.m_animationtype = animationtype

    def setWrap(self, wrap):
        self.m_wrap = wrap

    @QtCore.pyqtSlot()
    def slideInPrev(self):
        now = self.janela_principal.pages.currentIndex()
        if self.m_wrap or now > 0:
            self.slideInIdx(now - 1)

    @QtCore.pyqtSlot()
    def slideInNext(self):
        now = self.janela_principal.pages.currentIndex()
        if self.m_wrap or now < (self.janela_principal.pages.count() - 1):
            self.slideInIdx(now + 1)

    def slideInIdx(self, idx):
        if idx > (self.janela_principal.pages.count() - 1):
            idx = idx % self.janela_principal.pages.count()
        elif idx < 0:
            idx = (idx + self.janela_principal.pages.count()) % self.janela_principal.pages.count()
        self.slideInWgt(self.janela_principal.pages.widget(idx))

    def slideInWgt(self, newwidget):
        if self.m_active:
            return

        self.m_active = True

        _now = self.janela_principal.pages.currentIndex()
        _next = self.janela_principal.pages.indexOf(newwidget)

        if _now == _next:
            self.m_active = False
            return

        offsetx, offsety = self.janela_principal.pages.frameRect().width(), self.janela_principal.pages.frameRect().height()
        self.janela_principal.pages.widget(_next).setGeometry(self.janela_principal.pages.frameRect())

        if not self.m_direction == QtCore.Qt.Horizontal:
            if _now < _next:
                offsetx, offsety = 0, -offsety
            else:
                offsetx = 0
        else:
            if _now < _next:
                offsetx, offsety = -offsetx, 0
            else:
                offsety = 0

        pnext = self.janela_principal.pages.widget(_next).pos()
        pnow = self.janela_principal.pages.widget(_now).pos()
        self.m_pnow = pnow

        offset = QtCore.QPoint(offsetx, offsety)
        self.janela_principal.pages.widget(_next).move(pnext - offset)
        self.janela_principal.pages.widget(_next).show()
        self.janela_principal.pages.widget(_next).raise_()

        anim_group = QtCore.QParallelAnimationGroup(
            self, finished=self.animationDoneSlot
        )

        for index, start, end in zip(
            (_now, _next), (pnow, pnext - offset), (pnow + offset, pnext)
        ):
            animation = QtCore.QPropertyAnimation(
                self.janela_principal.pages.widget(index),
                b"pos",
                duration=self.m_speed,
                easingCurve=self.m_animationtype,
                startValue=start,
                endValue=end,
            )
            anim_group.addAnimation(animation)

        self.m_next = _next
        self.m_now = _now
        self.m_active = True
        anim_group.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

    @QtCore.pyqtSlot()
    def animationDoneSlot(self):
        self.janela_principal.pages.setCurrentIndex(self.m_next)
        self.janela_principal.pages.widget(self.m_now).hide()
        self.janela_principal.pages.widget(self.m_now).move(self.m_pnow)
        self.m_active = False

    def abre_janela_estoque(self, tabela_estoque):
        threading.Thread(target=carrega_tabela_estoque).start()
        self.tela_estoque.abrir_janela(tabela_estoque)

    def abre_janela_alunos(self, tabela_alunos):
        threading.Thread(target=carrega_tabela_alunos).start()
        self.tela_alunos.abrir_janela(tabela_alunos)

    def abre_janela_matriculas(self, tabela_matriculas):
        threading.Thread(target=carrega_tabela_matricula).start()
        self.tela_matriculas.abrir_janela(tabela_matriculas)
    
    def abre_janela_despesas(self, tabela_despesas):
        threading.Thread(target=carrega_tabela_despesa).start()
        self.tela_despesas.abrir_janela(tabela_despesas)

    def starta_threads(self):
        threading.Thread(target=carrega_tabela_alunos).start()
        threading.Thread(target=carrega_tabela_avfisica).start()
        threading.Thread(target=carrega_tabela_matricula).start()
        threading.Thread(target=carrega_tabela_estoque).start()
        threading.Thread(target=carrega_tabela_despesa).start()

    def ativa_menu_hamburguer(self):
        ## CALCULO DO TAMANHO DO MENU ##
        width = self.janela_principal.frame_4.width()
        if width == 50: newWidth = 210
        else: newWidth = 50

        ## ANIMAÇÃO DO MENU ABRINDO/FECHANDO ##    
        self.animation = QtCore.QPropertyAnimation(self.janela_principal.frame_4, b'minimumWidth')
        self.animation.setDuration(700) # 250
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.OutSine)
        self.animation.start()


    def gerador_de_pdf_aluno(self):
        global tabela_alunos
        global tabela_matriculas
        
        diretorio = QFileDialog.getExistingDirectory(self,
        'Selecione a pasta onde será salvo o PDF:', 'C:\\', QFileDialog.ShowDirsOnly)
        print(diretorio)
        ### CRIANDO NOME DO ARQUIVO ###
        nome_arquivo = dt.datetime.now().strftime("relatorio_alunos_%d_%m_%Y_%H%M%S.pdf")
        print(os.path.join(diretorio, nome_arquivo))
        if not diretorio:
            return
        if diretorio.upper() == "C:/":
            QtWidgets.QMessageBox.about(self.janela_principal,
             'Erro', 'Não é permitido salvar arquivos do diretório "C:/", por favor escolha outro diretório.')
            return
        #### INICIANDO LOAD SPINNER #####
        #threading.Thread(target=self.spinner.startAnimation()).start()

        ### CONFIGURANDO PDF ###
        pdf = PDF("P", "mm", "Letter", "Relatório de alunos")
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.alias_nb_pages()
        pdf.add_page()
        ### Carregando imagem principal ###
        pdf.carrega_imagem("dados_alunos_black.png")
        ### TABELA ALUNO ###
        headers =  (0, "Nome do aluno", "Idade", "Cpf", "Telefone", "E-mail")
        pdf.montador_de_tabela_alunos(tabela_alunos, headers,'Alunos cadastrados')
        ### TABELA DE ALUNOS QUE NÃO FIZERAM AV.FISICA ###
        aluno_obj = db.DadosAlunos()
        tabela_alunos_sem_avfisica =  aluno_obj.alunos_sem_av_fisicas()
        pdf.montador_de_tabela_alunos(tabela_alunos_sem_avfisica, headers,
        'Alunos que ainda não realizaram avaliação física')
        ### TABELA DE ALUNOS QUE FIZERAM AV.FISICA ###
        tabela_alunos_com_avfisica = aluno_obj.alunos_com_av_fisicas()
        pdf.montador_de_tabela_alunos(tabela_alunos_com_avfisica, headers,
        'Alunos que já realizaram avaliação física')

        id_matricula_ativa = []
        for linha in tabela_matriculas:
            if linha[2] == 1:
                id_matricula_ativa.append(linha[0])

        alunos_com_matricula_ativa = []
        alunos_com_matricula_inativa = []
        for linha in tabela_alunos:
            for id in id_matricula_ativa:
                if id == linha[0]:
                    alunos_com_matricula_ativa.append(linha)

        ids_matricula_ativa = [item[0] for item in alunos_com_matricula_ativa]
      

        for i in tabela_alunos:
            if i[0] not in ids_matricula_ativa:
                alunos_com_matricula_inativa.append(i)

        pdf.montador_de_tabela_alunos(alunos_com_matricula_ativa, headers,
        'Alunos que possuem a matrícula ativa')

        pdf.montador_de_tabela_alunos(alunos_com_matricula_inativa, headers,
        'Alunos que ainda não estão matriculados (inativa)')

        pdf.output(os.path.join(diretorio, nome_arquivo), "F")
        #self.spinner.stopAnimation()
        QtWidgets.QMessageBox.about(self.janela_principal,
             'Sucesso', 'Relatório de dados dos alunos gerado com sucesso!')


    def gerador_de_pdf_matricula(self):
        global tabela_alunos
        global tabela_matriculas
        print(tabela_matriculas)
        diretorio = QFileDialog.getExistingDirectory(self,
        'Selecione a pasta onde será salvo o PDF:', 'C:\\', QFileDialog.ShowDirsOnly)
        ### CRIANDO NOME DO ARQUIVO ###
        nome_arquivo = dt.datetime.now().strftime("relatorio_matriculas_%d_%m_%Y_%H%M%S.pdf")
        print(os.path.join(diretorio, nome_arquivo))
        print(diretorio)
        if not diretorio:
            return
        if diretorio.upper() == "C:/":
            QtWidgets.QMessageBox.about(self.janela_principal,
             'Erro', 'Não é permitido salvar arquivos do diretório "C:/", por favor escolha outro diretório.')
            return

        ### CONFIGURANDO PDF ###
        pdf = PDF("P", "mm", "Letter", "Relatório de matrículas")
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.alias_nb_pages()
        pdf.add_page()
        ### Carregando imagem principal ###
        pdf.carrega_imagem("dados_matriculas_black.png")
        ### TABELA MATRICULAS ###
        # Listas de IDS dos alunos
        alunos_30 = []
        alunos_90 = []
        alunos_180 = []
        alunos_360 = []
        for dado in tabela_matriculas:
            if dado[3] == 30 and dado[2] == 1:
                alunos_30.append(dado[0])
            if dado[3] == 90 and dado[2] == 1:
                alunos_90.append(dado[0])
            if dado[3] == 180 and dado[2] == 1:
                alunos_180.append(dado[0])
            if dado[3] == 360 and dado[2] == 1:
                alunos_360.append(dado[0])

        tabela_alunos_mensal = []
        tabela_alunos_trimestral = []
        tabela_alunos_semestral = []
        tabela_alunos_anual = []
        for aluno in tabela_alunos:
            if aluno[0] in alunos_30:
                tabela_alunos_mensal.append(aluno)
            if aluno[0] in alunos_90:
                tabela_alunos_trimestral.append(aluno)
            if aluno[0] in alunos_180:
                tabela_alunos_semestral.append(aluno)
            if aluno[0] in alunos_360:
                tabela_alunos_anual.append(aluno)



        headers =  (0, "Nome do aluno", "Idade", "Cpf", "Telefone", "E-mail")
        pdf.montador_de_tabela_alunos(tabela_alunos_mensal, headers,'Alunos com matrícula mensal (30 dias)')
        pdf.montador_de_tabela_alunos(tabela_alunos_trimestral, headers,'Alunos com matrícula trimestral (90 dias)')
        pdf.montador_de_tabela_alunos(tabela_alunos_semestral, headers,'Alunos com matrícula semestral (180 dias)')
        pdf.montador_de_tabela_alunos(tabela_alunos_anual, headers,'Alunos com matrícula anual (360 dias)')

        pdf.output(os.path.join(diretorio, nome_arquivo), "F")
        QtWidgets.QMessageBox.about(self.janela_principal,
             'Sucesso', 'Relatório de matrículas gerado com sucesso!')

    def gerador_de_pdf_estoque(self):
        global tabela_estoque
        
        
        diretorio = QFileDialog.getExistingDirectory(self,
        'Selecione a pasta onde será salvo o PDF:', 'C:\\', QFileDialog.ShowDirsOnly)
        ### CRIANDO NOME DO ARQUIVO ###
        nome_arquivo = dt.datetime.now().strftime("relatorio_estoque_%d_%m_%Y_%H%M%S.pdf")
        print(os.path.join(diretorio, nome_arquivo))
        print(diretorio)
        if not diretorio:
            return
        if diretorio.upper() == "C:/":
            QtWidgets.QMessageBox.about(self.janela_principal,
             'Erro', 'Não é permitido salvar arquivos do diretório "C:/", por favor escolha outro diretório.')
            return

        ### CONFIGURANDO PDF ###
        pdf = PDF("P", "mm", "Letter", "Relatório do estoque")
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.alias_nb_pages()
        pdf.add_page()
        ### Carregando imagem principal ###
        pdf.carrega_imagem("dados_estoque_black.png")
        
        headers =  (0, "Nome do produto", "Quantidade", "Observações")

        pdf.montador_de_tabela_estoque(tabela_estoque, headers,'Produtos cadastrados')

        pdf.output(os.path.join(diretorio, nome_arquivo), "F")
        QtWidgets.QMessageBox.about(self.janela_principal,
             'Sucesso', 'Relatório de estoque gerado com sucesso!')
        
    
    def gerador_de_pdf_despesas(self):
        global tabela_despesas
        
        
        diretorio = QFileDialog.getExistingDirectory(self,
        'Selecione a pasta onde será salvo o PDF:', 'C:\\', QFileDialog.ShowDirsOnly)
        ### CRIANDO NOME DO ARQUIVO ###
        nome_arquivo = dt.datetime.now().strftime("relatorio_despesas_%d_%m_%Y_%H%M%S.pdf")
        print(os.path.join(diretorio, nome_arquivo))
        print(diretorio)
        if not diretorio:
            return
        if diretorio.upper() == "C:/":
            QtWidgets.QMessageBox.about(self.janela_principal,
             'Erro', 'Não é permitido salvar arquivos do diretório "C:/", por favor escolha outro diretório.')
            return

        ### CONFIGURANDO PDF ###
        pdf = PDF("P", "mm", "Letter", "Relatório do despesas")
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.alias_nb_pages()
        pdf.add_page()
        ### Carregando imagem principal ###
        pdf.carrega_imagem("dados_despesas_black.png")
        
        headers =  (0, "Nome da despesa", "Valor","Data de vencimento","Observações")

        tabela_todas_despesas = []

        for registro in tabela_despesas:
            tabela_todas_despesas.append((registro[0],registro[1],registro[2],formato_iso_para_br(registro[3]),registro[4]))
        pdf.montador_de_tabela_despesas(tabela_todas_despesas, headers,'Despesas cadastradas')

        despesas_vencidas = []
        despesas_nao_vencidas = []
        hoje = formato_iso_para_br((str(dt.datetime.now().date())))
        for produto in tabela_despesas:
            try:
                esta_vencida = compara_datas(hoje, formato_iso_para_br(produto[3]))
                if esta_vencida:
                    despesas_vencidas.append(produto)
                else:
                    despesas_nao_vencidas.append(produto)
            except: 
                pass

        pdf.montador_de_tabela_despesas(despesas_vencidas, headers,'Despesas vencidas')
        pdf.montador_de_tabela_despesas(despesas_nao_vencidas, headers,'Despesas não vencidas')

        pdf.output(os.path.join(diretorio, nome_arquivo), "F")
        QtWidgets.QMessageBox.about(self.janela_principal,
             'Sucesso', 'Relatório de despesas gerado com sucesso!')
        

    def abre_graficos(self):
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(3000, loop.quit)
        loop.exec_()
        if tabela_despesas != [()]:
            self.gera_graficos(tabela_alunos, tabela_matriculas,
            tabela_avfisica, tabela_estoque, tabela_despesas)
    
    def gera_graficos_contornos_pretos(self, courses, values, title, archive_name):
        fig = matplotlib.pyplot.figure(figsize = (5, 3))
        
        ax = fig.add_subplot(111)

        ax.set_title(title, color="#000000")
        ax.bar(courses, values, color="green", width = 0.4, edgecolor="#000000")
        ax.set_ylabel("Quantidade")

        matplotlib.pyplot.savefig(archive_name, transparent=True)
        

    def gera_graficos(self, alunos=[], matriculas=[], avfis=[], estoque=[], desp=[]):
        ### GRAFICO DADOS GERAIS ###
        # creating the dataset
        qtd_alunos = len(alunos)
        qtd_matriculas = len(matriculas)
        qtd_produtos = len(estoque)
        qtd_despesas = len(desp)
        data = {'Alunos': qtd_alunos, 'Matriculas':qtd_matriculas, 'Produtos':qtd_produtos,
                'Despesas':qtd_despesas}
        courses = list(data.keys())
        values = list(data.values())
        
        fig = matplotlib.pyplot.figure(figsize = (5, 3))
        
        ax = fig.add_subplot(111)


        ax.set_title("Dados gerais", color="#ffffff")
        ax.bar(courses, values, color="green", width = 0.4, edgecolor="#000000")

        ax.set_ylabel("Quantidade")

        ### Contornos ###
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')

        ## Eixo X ##
        ax.xaxis.label.set_color('white')
        ax.tick_params(axis='x', colors='white')

        ##Eixo Y##
        ax.yaxis.label.set_color('white')
        ax.tick_params(axis='y', colors='white')

        #plt.show()
        matplotlib.pyplot.savefig('dados_gerais.png',transparent=True)
        self.janela_principal.total_alunos.setText(str(qtd_alunos))
        self.janela_principal.total_matriculas.setText(str(qtd_matriculas))
        self.janela_principal.total_estoque.setText(str(qtd_produtos))
        self.janela_principal.total_despesas.setText(str(qtd_despesas))

        ### GRAFICO DESPESAS ###
        desp_minima = min([i[2] for i in desp ])
        total_despesas = sum([i[2] for i in desp ])

        data = {'Despesa Minima':desp_minima, 'Valor total Despesas':total_despesas}
        courses = list(data.keys())
        values = list(data.values())
        self.gera_graficos_contornos_pretos(courses, values, "Dados despesas", 'dados_despesas_black.png')
        fig = matplotlib.pyplot.figure(figsize = (5, 3))
        # creating the bar plot
        ax = fig.add_subplot(111)

        ax.set_title("Dados despesas", color="#ffffff")


        ax.bar(courses, values, color="green", width = 0.4, edgecolor="#000000")

        ax.set_ylabel("Quantidade")


        ### Contornos ###
        ax.spines['bottom'].set_color('#ffffff')
        ax.spines['top'].set_color('#ffffff')
        ax.spines['right'].set_color('#ffffff')
        ax.spines['left'].set_color('#ffffff')

        ## Eixo X ##
        ax.xaxis.label.set_color('#ffffff')
        ax.tick_params(axis='x', colors='#ffffff')

        ##Eixo Y##
        ax.yaxis.label.set_color('#ffffff')
        ax.tick_params(axis='y', colors='#ffffff')

        #plt.show()
        matplotlib.pyplot.savefig('dados_despesas.png',transparent=True)
        self.janela_principal.qtd_dividas.setText(str(desp_minima))
        self.janela_principal.valor_despesas.setText(str(total_despesas))

        ### GRAFICO ESTOQUE ###

        maxqtd_produto = max([i[2] for i in estoque])
        data = {'Produtos':qtd_produtos, 'Prod. maior Qtd':maxqtd_produto}
        courses = list(data.keys())
        values = list(data.values())
        self.gera_graficos_contornos_pretos(courses, values, "Dados estoque", 'dados_estoque_black.png')
        fig = matplotlib.pyplot.figure(figsize = (5, 3))
        # creating the bar plot
        ax = fig.add_subplot(111)

        ax.set_title("Dados estoque", color="#ffffff")


        ax.bar(courses, values, color="green", width = 0.4, edgecolor="#000000")

        ax.set_ylabel("Quantidade")


        ### Contornos ###
        ax.spines['bottom'].set_color('#ffffff')
        ax.spines['top'].set_color('#ffffff')
        ax.spines['right'].set_color('#ffffff')
        ax.spines['left'].set_color('#ffffff')

        ## Eixo X ##
        ax.xaxis.label.set_color('#ffffff')
        ax.tick_params(axis='x', colors='#ffffff')

        ##Eixo Y##
        ax.yaxis.label.set_color('#ffffff')
        ax.tick_params(axis='y', colors='#ffffff')

        #plt.show()
        matplotlib.pyplot.savefig('dados_estoque.png',transparent=True)
        self.janela_principal.total_produto.setText(str(qtd_produtos))
        self.janela_principal.prod_maior_qtd.setText(str(maxqtd_produto))

        ### GRAFICO MATRICULAS ###
        trinta = noventa = centoeoitenta = trezentosesessenta = 0
        for i in matriculas:
            if i[3] == 30: trinta += 1
            elif i[3] == 90: noventa += 1
            elif i[3] == 180: centoeoitenta += 1
            elif i[3] == 360: trezentosesessenta += 1

        data = {'30 dias':trinta, '90 dias':noventa,'180 dias':centoeoitenta, '360 dias': trezentosesessenta}
        courses = list(data.keys())
        values = list(data.values())
        self.gera_graficos_contornos_pretos(courses, values, "Dados matrículas", 'dados_matriculas_black.png')
        fig = matplotlib.pyplot.figure(figsize = (5, 3))
        # creating the bar plot
        ax = fig.add_subplot(111)

        ax.set_title("Dados matrículas", color="#ffffff")


        ax.bar(courses, values, color="green", width = 0.4, edgecolor="#000000")

        ax.set_ylabel("Quantidade")


        ### Contornos ###
        ax.spines['bottom'].set_color('#ffffff')
        ax.spines['top'].set_color('#ffffff')
        ax.spines['right'].set_color('#ffffff')
        ax.spines['left'].set_color('#ffffff')

        ## Eixo X ##
        ax.xaxis.label.set_color('#ffffff')
        ax.tick_params(axis='x', colors='#ffffff')

        ##Eixo Y##
        ax.yaxis.label.set_color('#ffffff')
        ax.tick_params(axis='y', colors='#ffffff')

        #plt.show()
        matplotlib.pyplot.savefig('dados_matriculas.png',transparent=True)
        self.janela_principal.label_24.setText(str(trinta))
        self.janela_principal.label_22.setText(str(noventa))
        self.janela_principal.label_25.setText(str(centoeoitenta))
        self.janela_principal.label_26.setText(str(trezentosesessenta))

        ### GRAFICO ALUNOS ###
        avfisicas_naofeitas = 0
 
        for linha in avfis:
            esta_vazia = 0
            for i, item in enumerate(linha):
                if i > 1:
                    if int(item) == 0:
                        esta_vazia += 1
            if esta_vazia == 7:
                avfisicas_naofeitas += 1
            esta_vazia = 0

        qtd_avfisicas = len(avfis) - avfisicas_naofeitas
        ativa = inativa = 0
        for i in matriculas:
            if i[2] == 0: inativa += 1
            elif i[2] is not None: ativa += 1

        data = {'Alunos':qtd_alunos, 'M. ativa':ativa,'M. inativa':inativa, 'Av. fisicas': qtd_avfisicas}
        courses = list(data.keys())
        values = list(data.values())
        self.gera_graficos_contornos_pretos(courses, values, "Dados alunos", 'dados_alunos_black.png')
        fig = matplotlib.pyplot.figure(figsize = (5, 3))
        # creating the bar plot
        ax = fig.add_subplot(111)

        ax.set_title("Dados alunos", color="#ffffff")


        ax.bar(courses, values, color="green", width = 0.4, edgecolor="#000000")

        ax.set_ylabel("Quantidade")


        ### Contornos ###
        ax.spines['bottom'].set_color('#ffffff')
        ax.spines['top'].set_color('#ffffff')
        ax.spines['right'].set_color('#ffffff')
        ax.spines['left'].set_color('#ffffff')

        ## Eixo X ##
        ax.xaxis.label.set_color('#ffffff')
        ax.tick_params(axis='x', colors='#ffffff')

        ##Eixo Y##
        ax.yaxis.label.set_color('#ffffff')
        ax.tick_params(axis='y', colors='#ffffff')

        #plt.show()
        matplotlib.pyplot.savefig('dados_alunos.png',transparent=True)
        self.janela_principal.label_32.setText(str(qtd_alunos))
        self.janela_principal.label_35.setText(str(ativa))
        self.janela_principal.label_33.setText(str(inativa))
        self.janela_principal.label_34.setText(str(qtd_avfisicas))
 
    def coloca_grafico_na_tela(self):
        self.abre_widget()
        if self.janela_principal.tab_dashboard.currentIndex() == 0:
            self.janela_principal.frame_6.setStyleSheet("background-image: url('dados_gerais.png');\
                                background-color: rgb(39, 39, 39); background-repeat: no-repeat;")
        
        if self.janela_principal.tab_dashboard.currentIndex() == 1:
            self.janela_principal.frame_6.setStyleSheet("background-image: url('dados_despesas.png');\
                                background-color: rgb(39, 39, 39); background-repeat: no-repeat;")
        
        if self.janela_principal.tab_dashboard.currentIndex() == 2:
            self.janela_principal.frame_6.setStyleSheet("background-image: url('dados_estoque.png');\
                                background-color: rgb(39, 39, 39); background-repeat: no-repeat;")
         
        if self.janela_principal.tab_dashboard.currentIndex() == 3:
            self.janela_principal.frame_6.setStyleSheet("background-image: url('dados_matriculas.png');\
                                background-color: rgb(39, 39, 39); background-repeat: no-repeat;")
      
        if self.janela_principal.tab_dashboard.currentIndex() == 4:
            self.janela_principal.frame_6.setStyleSheet("background-image: url('dados_alunos.png');\
                                background-color: rgb(39, 39, 39); background-repeat: no-repeat;")
         
    def abre_widget(self):        
        self.animation = QtCore.QPropertyAnimation(self.janela_principal.frame_6, b'minimumWidth')
        self.animation.setDuration(1500) # 250
        self.animation.setStartValue(50)
        self.animation.setEndValue(700)
        self.animation.setEasingCurve(QtCore.QEasingCurve.OutSine)
        self.animation.start()

    def destroi_janela_confirm_email(self, *args):
        del self.confirmacao_do_email
        self.confirmacao_do_email = 0
        self.janela_principal.cancelarEmailBtn.setEnabled(True)

        # del self.confirmacao_do_anexo
        # self.confirmacao_do_anexo = 0
 

    def cancela_envio_email(self, pular=False):
        if not pular:
            res = QMessageBox.question(self.janela_principal,'Cancelar Email', "Tem certeza que deseja cancelar o Email?", QMessageBox.Yes | QMessageBox.No)
            if res == QMessageBox.Yes:
                self.janela_principal.editor.setText("")
                self.janela_principal.editor.setHtml(HTML_PLACEHOLDER)
                self.janela_principal.destinatario.setText("")
                self.janela_principal.assunto.setText("")
        else:
            self.janela_principal.editor.setText("")
            self.janela_principal.editor.setHtml(HTML_PLACEHOLDER)
            self.janela_principal.destinatario.setText("")
            self.janela_principal.assunto.setText("")
        
        for anexo in JanelaPrincipal.anexos:
            JanelaPrincipal.anexos[anexo][0].deleteLater()
        JanelaPrincipal.anexos = {}
        for anexo in JanelaPrincipal.confirmacao_do_anexo:
            JanelaPrincipal.confirmacao_do_anexo[anexo][0].deleteLater()
        JanelaPrincipal.confirmacao_do_anexo = {}
        self.qtd_anexos = 0
        self.janela_principal.label_42.setText(f"Anexos ({self.qtd_anexos})")
        self.programa.label_3.setText(f"{self.qtd_anexos}")
        self.confirmacao_do_anexo.label_3.setText(f"{self.qtd_anexos}")
        return


    def envia_email(self):
        try:
            global conta_google
            servico = conta_google
            ### PEGANDO OS VALORES PRA CRIAR O EMAIL ###
            emails = self.janela_principal.destinatario.text()
            html = self.janela_principal.editor.toHtml()
            plain = self.janela_principal.editor.toPlainText()
            assunto = self.janela_principal.assunto.text()
            destinatarios = ""
            emails = emails.split(";")
            for email in emails:
                destinatarios += email + ";"
            enviado_por = 'me'
            para = destinatarios
            assunto = assunto
            mensagem = html
            if self.qtd_anexos > 0:
                anexos = []
                for files in JanelaPrincipal.anexos:
                    anexos.append(JanelaPrincipal.anexos[files][1])
                print(anexos)
                message = google.SendMessage(service=1,
                sender=enviado_por, to=para, subject=assunto, msgHtml=mensagem, msgPlain=plain, attachmentFile=anexos)
            else:
                message = google.create_message(enviado_por, para, assunto, mensagem)
            google.send_message(servico, 'me', message)
            QtWidgets.QMessageBox.about(self.janela_principal,
            'Alerta', 'Email enviado com sucesso!')
            self.cancela_envio_email(pular=True)
            self.destroi_janela_confirm_email()
        except Exception as e:
            QtWidgets.QMessageBox.about(self.janela_principal,
            'Alerta', 'Ocorreu algum erro ao enviar o email. Tente novamente mais tarde.')
            print("Deu pal", e)

    def envia_email_confirmacao(self):
        try:
            if self.confirmacao_do_email == 0:
                ### TELA DE CONFIRMAÇÃO DO EMAIL ###
                self.confirmacao_do_email = uic.loadUi('src\\telas\\telas_principais\\confirma_email.ui')
                self.confirmacao_do_email.closeEvent = self.destroi_janela_confirm_email
                self.confirmacao_do_email.btnCancelarConfirmacao.clicked.connect(lambda: self.destroi_janela_confirm_email())
                self.confirmacao_do_email.btnEnviarConfirmacao.clicked.connect(lambda: self.envia_email())
                self.confirmacao_do_email.pushButton.clicked.connect(lambda: self.confirmacao_do_anexo.show())

                # ### TELA DE CONFIRMAÇÃO DO ANEXO ###
                # self.confirmacao_do_anexo = uic.loadUi('src\\telas\\telas_principais\\confirma_anexo.ui')
                
                # self.confirmacao_do_anexo.pushButton.clicked.connect(lambda: self.confirmacao_do_anexo.close())
            global conta_google
            
            self.confirmacao_do_email.editorConfirmacao.setEnabled(False)
            servico = conta_google
            meu_user = servico.users().getProfile(userId='me').execute()
            print(meu_user["emailAddress"])
            emails = self.janela_principal.destinatario.text()
            emails = emails.split(";")
            print(emails)
            if len(emails) == 1 and emails[0] == '':
                QtWidgets.QMessageBox.about(self.janela_principal,
             'Alerta', 'Para enviar um email, insira ao menos 1 destinatário.')
                return
            
            for email in emails:
                if email == "":
                    continue
                if not validacoes.valida_email_sintaxe(email):
                    QtWidgets.QMessageBox.about(self.janela_principal,
                    'Alerta', f'Destinatário "{email}" inválido.')
                    return
            
            
            qtd_str_vazia = emails.count("")
            print("string vazias", qtd_str_vazia)

            if qtd_str_vazia > 0:
                for i in range(qtd_str_vazia):
                    emails.remove("")

            html = self.janela_principal.editor.toHtml()
            self.confirmacao_do_email.editorConfirmacao.setHtml(html)
            assunto = self.janela_principal.assunto.text()
            self.confirmacao_do_email.assuntoConfirmacao.setText(assunto)
            

            self.confirmacao_do_email.scrollAreaDestinatarios.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.confirmacao_do_email.scrollAreaDestinatarios.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.confirmacao_do_email.scrollAreaDestinatarios.setWidgetResizable(True)
            widget = QtWidgets.QWidget()
            self.confirmacao_do_email.scrollAreaDestinatarios.setWidget(widget)
            vbox2 = QVBoxLayout()
            widget.setLayout(vbox2)

            self.confirmacao_do_email.label_40.setTextFormat(Qt.RichText)
            self.confirmacao_do_email.label_40.setText(f"""<html><head/><body><p><span style=" font-size:16pt; font-weight:600;">Destinatários ({len(emails)})</span></p></body></html>""")
            for email in emails:
                label = QtWidgets.QLabel()
                

                label.setText(email)
                label.setStyleSheet("""background-color: rgb(150, 150, 150);\nborder-radius:9px;\nfont-size: 16px;\nfont-weight:bold;\ncolor: rgb(0, 0, 0); """)
                vbox2.addWidget(label)
            self.confirmacao_do_email.label.setText(str(f'Anexos: ({len(JanelaPrincipal.anexos)})'))
            self.janela_principal.cancelarEmailBtn.setEnabled(False)
            if self.qtd_anexos <= 0:
                self.confirmacao_do_email.pushButton.setEnabled(False)
            self.confirmacao_do_email.show()

        except Exception as err:
            QtWidgets.QMessageBox.about(self.janela_principal,
             'Alerta', 'Ocorreu um erro ao tentar enviar o E-mail, certifique-se de estar logado e tente novamente mais tarde.')
            print(err)


    def conecta_conta_google(self):
        try:
            global conectado_ao_google
            global conta_google
            if conectado_ao_google == 0:
                usuario = None
                CLIENT_SECRET_FILE = 'src\\credentials.json'
                API_NAME = 'gmail'
                API_VERSION = 'v1'
                SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

                
                servico = google.Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        
           

                usuario = servico.users().getProfile(userId='me').execute()
                print(usuario)
            
                if not usuario:
                    #### CASO O USUARIO NÃO CONSIGA SE CONECTAR AO GOOGLE ###
                    self.janela_principal.label_36.setText('Não foi possível conectar ao google')
                else:
                    #### CASO O USUARIO CONSIGA SE CONECTAR AO GOOGLE ###
                    self.janela_principal.label_36.setText('Logado em: '+ usuario['emailAddress'])
                    self.janela_principal.btn_google.setText('Desconectar')
                    conta_google = servico
                    conectado_ao_google = 1
                    
            else:
                if os.path.isfile('token_gmail_v1.pickle'):
                    os.remove('token_gmail_v1.pickle')
                ### VOLTANDO PARA OS LAYOUTS DE DESCONECTADO ##
                self.janela_principal.label_36.setText('Desconectado')
                self.janela_principal.btn_google.setText('Conectar conta Google')
                conectado_ao_google = 0
                conta_google = None
        except Exception as err:
            if os.path.isfile('token_gmail_v1.pickle'):
                    os.remove('token_gmail_v1.pickle')
            print(err)

    def destroi_arquivo_pikle(self):
        try:
            if os.path.isfile('token_gmail_v1.pickle'):
                    os.remove('token_gmail_v1.pickle')
        except:
            pass

    def tela_enviar_email(self):
        if conectado_ao_google == 0:
            QtWidgets.QMessageBox.about(self.janela_principal,
             'Alerta', 'Para enviar um email, certifique-se de estar logado em uma conta Google')
        else:
            self.slideInNext()


class JanelaLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        ### CARREGANDO JANELA DE LOGIN E SPLASHSCREEN ###
        self.janela_login = uic.loadUi('src\\telas\\telas_principais\\login.ui')
        self.splashscreen = uic.loadUi('src\\telas\\telas_principais\\splash_screen.ui')
        try:
            with open("src/save_user", "r") as arquivo:
                login = arquivo.read()
            if not login:
                self.janela_login.checkBox_salvar.setChecked(False)
            else:
                self.janela_login.checkBox_salvar.setChecked(True)
                self.janela_login.line_usuario.setText(str(login))
        except:
            pass

        ## BOTÕES DA TELA DE LOGIN ##
        self.janela_login.frame_erro.hide()
        self.janela_login.botao_entrar.clicked.connect(self.logar)
        self.janela_login.botao_erro.clicked.connect(lambda: self.janela_login.frame_erro.hide())
        self.janela_login.destroyed.connect(lambda: self.closeEvent())
    
    def closeEvent(self):
        pass

    def logar(self):
        ### SETANDO CORES PARA O SUCESSO NO LOGIN ###
        stylesheet_sucesso = SUCESS_LOGIN
        mensagem_sucesso = MENSAGEM_SUCESSO
        ### SETANDO CORES PARA O FRACASSO NO LOGIN ###
        stylesheet_fracasso = FAILED_LOGIN
        
        ### LIMPA OS CAMPOS DE LOGIN E SENHA E FAZ A QUERY ###
        login = self.janela_login.line_usuario.text()
        senha = self.janela_login.line_senha.text()
        senha = senha.encode("utf-8")
        print(login, senha)
        query = db.LoginVerification()
        resposta = query.verifica_login(login)
        ### PROVIDENCIAS CASO O USUARIO NÃO ESTEJA NO BANCO ###
        if resposta == None:
            self.janela_login.frame_erro.show()
            self.janela_login.line_usuario.setText('')
            self.janela_login.line_senha.setText('')
            self.janela_login.line_usuario.setStyleSheet(stylesheet_fracasso)
            #self.janela_login.line_senha.setStyleSheet(stylesheet_fracasso)
            self.janela_login.label_erro.setText('Usuario não existe')
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(3000, loop.quit)
            loop.exec_()
            self.janela_login.frame_erro.hide()
            return

        ### PROVIDENCIAS CASO A SENHA E O USUARIO ESTEJAM CORRETOS ###
        hash_no_banco = resposta[1].encode("utf-8")
        if bcrypt.checkpw(senha, hash_no_banco):
            self.janela_login.line_usuario.setStyleSheet(stylesheet_sucesso)
            self.janela_login.line_senha.setStyleSheet(stylesheet_sucesso)
            self.janela_login.frame_erro.setStyleSheet(mensagem_sucesso)
            self.janela_login.frame_erro.show()
            self.janela_login.label_erro.setText('Seja bem vindo!')
            try:
                if self.janela_login.checkBox_salvar.isChecked():
                    with open("src/save_user", "w") as arquivo:
                        arquivo.write(str(login))
                else:
                    with open("src/save_user", "w") as arquivo:
                        arquivo.write("")
            except:
                pass
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(2000, loop.quit)
            loop.exec_()
            self.chama_splash_screen()
        else:
            ### CASO A SENHA NÃO ESTEJA CORRETA ###
            self.janela_login.frame_erro.show()
            self.janela_login.line_senha.setText('')
            #self.janela_login.line_usuario.setStyleSheet(stylesheet_fracasso)
            self.janela_login.line_senha.setStyleSheet(stylesheet_fracasso)
            self.janela_login.label_erro.setText('Senha incorreta')
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(3000, loop.quit)
            loop.exec_()
            self.janela_login.frame_erro.hide()
            return



    def chama_splash_screen(self):
        ##Removendo o title bar
        self.splashscreen.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.splashscreen.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        ##Drop shadow Effect
        shadow = QtWidgets.QGraphicsDropShadowEffect(self.splashscreen)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.splashscreen.DropShadowFrame.setGraphicsEffect(shadow)

        ##TIMER
        self.splashscreen.timer = QtCore.QTimer()
        self.splashscreen.timer.timeout.connect(self.progressbar)

        ## Timer em milissegundos
        self.splashscreen.timer.start(35)

        ## Muda os textos de carregamento
        QtCore.QTimer.singleShot(0, lambda: self.splashscreen.label_description.setText("\
        <strong>Bem vindo(a)</strong> ao sistema de gerenciamento"))
        QtCore.QTimer.singleShot(1500, lambda: self.splashscreen.label_description.setText("\
        <strong>CARREGANDO</strong> banco de dados"))
        QtCore.QTimer.singleShot(3000, lambda: self.splashscreen.label_description.setText("\
        <strong>CARREGANDO</strong> interface"))

        self.splashscreen.show()
        self.janela_login.close()

    def progressbar(self):
        global counter
        self.splashscreen.progressBar.setValue(counter)
        if counter > 100:
            self.splashscreen.timer.stop()
            main_screen.janela_principal.show()
            self.splashscreen.close()

        counter += 1


class JanelaMatriculas(QMainWindow):
    def __init__(self):
        super().__init__()
        
        ## CARREGANDO JANELAS QUE SERÃO USADAS NESTE MODULO
        self.janela_matriculas = uic.loadUi('src\\telas\\telas_matricula\\tela_matriculas.ui')
        self.janela_matriculas_atualizar = uic.loadUi('src\\telas\\telas_matricula\\atualizar_matriculas.ui')

        ### ABRINDO JANELA PARA INSERIR OS DADOS###
        self.janela_matriculas.btn_abreJanelaAtualizar.clicked.connect(lambda: self.abrir_janela_atualizar_matriculas())
        self.janela_matriculas_atualizar.btn_sairJanelaAtualizar.clicked.connect(lambda: self.janela_matriculas_atualizar.close())
        self.janela_matriculas_atualizar.btn_atualizarDados.clicked.connect(self.atualizar_dados)

        ### ATIVANDO FUNÇÃO PESQUISAR NA TELA DAS MATRICULAS ###
        self.janela_matriculas.btn_pesquisar.clicked.connect(self.pesquisar)
        self.janela_matriculas.inputBuscar.returnPressed.connect(self.pesquisar)
        self.resultados_pesquisa = []

        ###BOTÃO QUE FECHA A JANELA MATRICULAS###
        self.janela_matriculas.btn_fechar.clicked.connect(lambda: self.janela_matriculas.close())

    ### MÉTODOS / FUNCIONALIDADES ###
    def starta_thread(self):
        threading.Thread(target=self.chama_mostrar_avfisica).start()

    def chama_mostrar_avfisica(self):
        time.sleep(1)
        global tabela_matriculas
        self.mostrar_matriculas_tela(tabela_matriculas)

    def fechar_janela_atualizar(self):
        self.starta_thread()
        self.resultados_pesquisa = []
        self.destroi_janela_atualizar()

    def destroi_janela_atualizar(self, *args):
        global tabela_matriculas
        self.lista_objetos_linedit = []
        self.dados_antigos_atualizar = []
        self.registros_com_id = []
        self.resultados_pesquisa = []
        self.mostrar_matriculas_tela(tabela_matriculas)
        self.janela_matriculas_atualizar.close()
    
    def pesquisar(self):
        global tabela_matriculas

        pesquisa = self.janela_matriculas.inputBuscar.text()
        self.resultados_pesquisa = []
        if self.janela_matriculas.radioNomeAluno.isChecked():
            nome_buscado = pesquisa.upper()
            for aluno in tabela_matriculas:
                if nome_buscado in aluno[1].upper():
                    self.resultados_pesquisa.append(aluno)
            if self.resultados_pesquisa:
                self.mostrar_matriculas_tela(self.resultados_pesquisa)
            else:
                QtWidgets.QMessageBox.about(self.janela_matriculas,
             'Gerenciador de alunos', f'Aluno "{nome_buscado}" não encontrado.')
            return
        if self.janela_matriculas.radioMatriculaAtiva.isChecked():
            nome_buscado = pesquisa.upper()
            if nome_buscado in "ativa".upper():
                nome_buscado = 1
            elif nome_buscado in "inativa".upper():
                nome_buscado = 0
            elif nome_buscado in "Não possui".upper() or nome_buscado in "nao possui".upper():
                nome_buscado = "NONE"
            for aluno in tabela_matriculas:
                if str(nome_buscado) in str(aluno[2]).upper():
                    self.resultados_pesquisa.append(aluno)
            if self.resultados_pesquisa:
                self.mostrar_matriculas_tela(self.resultados_pesquisa)
            else:
                QtWidgets.QMessageBox.about(self.janela_matriculas,
             'Gerenciador de alunos', f'Matricula ativa "{nome_buscado}" não encontrada.')
            return
        if self.janela_matriculas.radioTipoMatricula.isChecked():
            nome_buscado = pesquisa.upper()
            if nome_buscado in "mensal".upper():
                nome_buscado = 30
            elif nome_buscado in "bimestral".upper():
                nome_buscado = 60
            elif nome_buscado in "trimestral".upper():
                nome_buscado = 90
            elif nome_buscado in "semestral".upper():
                nome_buscado = 180
            elif nome_buscado in "anual".upper():
                nome_buscado = 360
            elif nome_buscado in "Não possui".upper() or nome_buscado in "nao possui".upper():
                nome_buscado = "NONE"
            for aluno in tabela_matriculas:
                if str(nome_buscado) in str(aluno[3]).upper():
                    self.resultados_pesquisa.append(aluno)
            if self.resultados_pesquisa:
                self.mostrar_matriculas_tela(self.resultados_pesquisa)
            else:
                QtWidgets.QMessageBox.about(self.janela_matriculas,
             'Gerenciador de alunos', f'Tipo de matrícula "{nome_buscado}" não encontrada.')
            return
        if self.janela_matriculas.radioDataInicio.isChecked():
            nome_buscado = pesquisa.upper()
            palavras_data = ["sem data".upper(), "não possui".upper(), "nao possui".upper(),
            "nao".upper(), "não".upper(), "-"]
            if nome_buscado in palavras_data:
                nome_buscado = "NONE"
            for aluno in tabela_matriculas:
                if str(nome_buscado) in str(aluno[4]).upper():
                    self.resultados_pesquisa.append(aluno)
                elif str(nome_buscado) in formato_iso_para_br(str(aluno[4]).upper()):
                    self.resultados_pesquisa.append(aluno)
                elif str(nome_buscado) in formato_br_para_iso(str(aluno[4]).upper()):
                    self.resultados_pesquisa.append(aluno)
            if self.resultados_pesquisa:
                self.mostrar_matriculas_tela(self.resultados_pesquisa)
            else:
                QtWidgets.QMessageBox.about(self.janela_matriculas,
             'Gerenciador de alunos', f'Matricula com data inicio "{nome_buscado}" não encontrada.')
            return
        if self.janela_matriculas.radioDataFim.isChecked():
            nome_buscado = pesquisa.upper() 
            palavras_data = ["sem data".upper(), "não possui".upper(), "nao possui".upper(),
            "nao".upper(), "não".upper(), "-"]
            if nome_buscado in palavras_data:
                nome_buscado = "NONE"
            for aluno in tabela_matriculas:
                if str(nome_buscado) in str(aluno[5]).upper():
                    self.resultados_pesquisa.append(aluno)
                elif str(nome_buscado) in formato_iso_para_br(str(aluno[5]).upper()):
                    self.resultados_pesquisa.append(aluno)
                elif str(nome_buscado) in formato_br_para_iso(str(aluno[5]).upper()):
                    self.resultados_pesquisa.append(aluno)
            if self.resultados_pesquisa:
                self.mostrar_matriculas_tela(self.resultados_pesquisa)
            else:
                QtWidgets.QMessageBox.about(self.janela_matriculas,
             'Gerenciador de alunos', f'Matricula com data fim "{nome_buscado}" não encontrada.')
            return
        if self.janela_matriculas.radioTodosRegistros.isChecked():
            self.resultados_pesquisa = []
            self.mostrar_matriculas_tela(tabela_matriculas)
            self.janela_matriculas.inputBuscar.setText("")
        return


    def atualizar_dados(self):
        global tabela_avfisica
        #print(tabela_avfisica)
       
        dados_update = []
        update = False
        lista_aux = []
        lista_aux2 = []
        lista_objetos = []


        for item in self.lista_objetos_linedit:
            if isinstance(item[0], QtWidgets.QLineEdit):
                lista_objetos.append(item[0].text())
            if isinstance(item[0], QtWidgets.QComboBox):
                lista_objetos.append(str(item[0].currentText()))
            if isinstance(item[0], QtWidgets.QDateEdit):
                lista_objetos.append(dt.datetime.strftime(item[0].date().toPyDate(), format="%Y-%m-%d"))
        self.lista_objetos_linedit = lista_objetos
        #print(self.lista_objetos_linedit)
        #self.lista_objetos_linedit = [item[0].text() for item in self.lista_objetos_linedit]
        lista = []
        lista_oficial = []
        i = 0
        for item in self.lista_objetos_linedit:
            lista.append(item)
            if i != 4:
                i += 1
            else:
                lista.insert(0, 0)
                lista_oficial.append(tuple(lista))
                lista = []
                i = 0
        
        self.lista_objetos_linedit = lista_oficial
        

        #print(self.lista_objetos_linedit)
        #print(self.registros_com_id)###Terminar essas coisas aqui. A questão de pegar a lista sem id e a com id, e mandar pro banco só a que tem o id

        dados_antigos = []
        cont = 0
        for j, registros_com_id in enumerate(self.registros_com_id):
            for i in range(len(registros_com_id)):
                if i == 0: continue
                if registros_com_id[i] != self.lista_objetos_linedit[j][i]:
                    print(type(registros_com_id[i]) , type(self.lista_objetos_linedit[j][i]))
                    print(registros_com_id[i] , self.lista_objetos_linedit[j][i])
                    update = True
                lista_aux.append(self.lista_objetos_linedit[j][i])  
                lista_aux2.append(registros_com_id[i])
                if update and cont == 4:
                    lista_aux.insert(0, registros_com_id[0])
                    lista_aux2.insert(0, registros_com_id[0])
                    dados_update.append(tuple(lista_aux))
                    dados_antigos.append(tuple(lista_aux2))
                    cont = -1
                    update = False
                    lista_aux = []
                    lista_aux2 = []
                elif not update and cont == 4:
                    lista_aux = []
                    lista_aux2 = []
                    cont = -1
                cont += 1

        ###Aqui comecaria um load spinner
        print(dados_update)
        dados_update2 = []
        for i in range(len(dados_update)):
            data_inicio = dados_update[i][4]
            data_fim = dados_update[i][5]
            data_min_permitida = dt.datetime.strptime("2020-01-01", "%Y-%m-%d")
            data_max_permitida = dt.datetime.strptime("2050-01-01", "%Y-%m-%d")
            data_inicio = dt.datetime.strptime(data_inicio, "%Y-%m-%d")
            data_fim = dt.datetime.strptime(data_fim, "%Y-%m-%d")
            if not (data_min_permitida <= data_inicio <= data_max_permitida):
                QtWidgets.QMessageBox.about(self.janela_matriculas_atualizar,
             'Gerenciador de alunos', f'Erro ao atualizar data de inicio, por favor insira uma data de no\
             minimo 2020 e no máximo 2050')
                self.abrir_janela_atualizar_matriculas()
                return
            if not (data_min_permitida <= data_fim <= data_max_permitida):
                QtWidgets.QMessageBox.about(self.janela_matriculas_atualizar,
             'Gerenciador de alunos', f'Erro ao atualizar data de finalização, por favor insira uma data de no\
             minimo 2020 e no máximo 2050')
                self.abrir_janela_atualizar_matriculas()
                return
            if data_fim <= data_inicio:
                QtWidgets.QMessageBox.about(self.janela_matriculas_atualizar,
             'Gerenciador de alunos', f'Erro ao atualizar, a data de finalização é menor que a data de inicio')
                self.abrir_janela_atualizar_matriculas()
                return
            dados_update2.append(list(dados_update[i]))
            
            if dados_update[i][2] == "Não possui":
                dados_update2[i][2] = None
            if dados_update[i][2] == "Ativa":
                dados_update2[i][2] = 1
            if dados_update[i][2] == "Inativa":
                dados_update2[i][2] = 0
            if dados_update[i][3] == "Não possui":
                dados_update2[i][3] = None
            if dados_update[i][3] == "Mensal":
                dados_update2[i][3] = 30
            if dados_update[i][3] == "Bimestral":
                dados_update2[i][3] = 60
            if dados_update[i][3] == "Trimestral":
                dados_update2[i][3] = 90
            if dados_update[i][3] == "Semestral":
                dados_update2[i][3] = 180
            if dados_update[i][3] == "Anual":
                dados_update2[i][3] = 360
        print(dados_update2)
        if dados_update2:
            atualizar = db.Matricula()
            for dado in dados_update2:
                retorno = atualizar.atualizar_matricula(dado[0], dado[2], dado[3], dado[4],
                dado[5])
                if retorno == "Erro":
                    QtWidgets.QMessageBox.about(self.janela_matriculas_atualizar,
                'Gerenciador de avaliações físicas', 'Ocorreu um erro ao atualizar a matricula.')
                    self.destroi_janela_atualizar()
        threading.Thread(target=carrega_tabela_matricula).start()
        QtWidgets.QMessageBox.about(self.janela_matriculas_atualizar,
             'Gerenciador de alunos', 'Dados atualizados com Sucesso!')
        self.registros_com_id = []
        self.lista_objetos_linedit = []
        self.dados_antigos_atualizar = []
        self.fechar_janela_atualizar()

    
    def abrir_janela(self, tabela):
        ## erro caso o usuario tente acessar os dados antes das tabelas carregarem ##
        if tabela == [()]:
            QtWidgets.QMessageBox.about(self.janela_matriculas,
             'Gerenciador de alunos', 'Ocorreu um erro ao acessar o banco de dados,\nVerifique sua conexão.')
            return

        self.janela_matriculas.show()
        self.mostrar_matriculas_tela(tabela)



    def mostrar_matriculas_tela(self, tabela):
        self.janela_matriculas.tabelaMatriculas.setRowCount(len(tabela))
        self.janela_matriculas.tabelaMatriculas.setColumnCount(len(tabela[0])-1)
        self.janela_matriculas.tabelaMatriculas.setHorizontalHeaderLabels(["Nome Aluno", "Matricula Ativa", "Tipo matricula",
         "Data inicio", "Data fim"])
        self.janela_matriculas.tabelaMatriculas.resizeRowsToContents()
        for i in range(len(tabela)): #linha
            for j in range(len(tabela[0])): #coluna
                if j == 0:
                    item = QtWidgets.QTableWidgetItem(f"{tabela[i][j+1]}")
                if j == 1:
                    if str(tabela[i][j+1]) == "None":
                        item = "Não possui" 
                        item = QtWidgets.QTableWidgetItem(item)
                    elif str(tabela[i][j+1]) == "0":
                        item = QtWidgets.QTableWidgetItem("Inativa")
                    elif str(tabela[i][j+1]) == "1":
                        item = QtWidgets.QTableWidgetItem("Ativa")
                if j == 2:
                    if str(tabela[i][j+1]) == "None":
                        item = "Não possui" 
                        item = QtWidgets.QTableWidgetItem(item)
                    elif str(tabela[i][j+1]) == "30":
                        item = QtWidgets.QTableWidgetItem("Mensal")
                    elif str(tabela[i][j+1]) == "60":
                        item = QtWidgets.QTableWidgetItem("Bimestral")
                    elif str(tabela[i][j+1]) == "90":
                        item = QtWidgets.QTableWidgetItem("Trimestral")
                    elif str(tabela[i][j+1]) == "180":
                        item = QtWidgets.QTableWidgetItem("Semestral")
                    elif str(tabela[i][j+1]) == "360":
                        item = QtWidgets.QTableWidgetItem("Anual")
                if j == 3 or j == 4:
                    item = QtWidgets.QTableWidgetItem(f"{formato_iso_para_br(str(tabela[i][j+1]))}")
                    if str(tabela[i][j+1]) == "None":
                        item = QtWidgets.QTableWidgetItem("-")

                self.janela_matriculas.tabelaMatriculas.setItem(i,j, item)
        ## Reajustando o tamnho das células(colunoas) de acordo com o contúdo delas
        header = self.janela_matriculas.tabelaMatriculas.horizontalHeader()           # Colunas abaixo  
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

    def abrir_janela_atualizar_matriculas(self):
        global tabela_matriculas
        dados = set(index.row() for index in self.janela_matriculas.tabelaMatriculas.selectedIndexes())
        if len(dados) < 1:
            QtWidgets.QMessageBox.about(self.janela_matriculas,
             'Gerenciador de avaliações físicas', 'Para atualizar, é necessario selecionar ao menos 1 registro.')
            return
        lista_de_dados = []
        self.registros_com_id = []
        if len(self.resultados_pesquisa) > 0:
            for i in dados:
                self.registros_com_id.append(self.resultados_pesquisa[i])
        else:
            for i in dados:
                self.registros_com_id.append(tabela_matriculas[i])
        self.resultados_pesquisa = []

        for i, j in enumerate(self.registros_com_id):
            j = list(j)
            for cont, dado in enumerate(j):
                if cont == 2:
                    if dado == None:
                        j[cont] = "Não possui"
                    if dado == 1:
                        j[cont] = "Ativa"
                    if dado == 0:
                        j[cont] = "Inativa"
                if cont == 3:
                    if dado == None:
                        j[cont] = "Não possui"
                    if dado == 30:
                        j[cont] = "Mensal"
                    if dado == 60:
                        j[cont] = "Bimestral"
                    if dado == 90:
                        j[cont] = "Trimestral"
                    if dado == 180:
                        j[cont] = "Semestral"
                    if dado == 360:
                        j[cont] = "Anual"
                if cont == 4 or cont == 5:
                    try:
                        j[cont] = dt.datetime.strftime(dado, format="%Y-%m-%d")
                    except:
                        pass
            self.registros_com_id[i] = tuple(j)
        for i in dados:
            lista_de_dados.append((self.janela_matriculas.tabelaMatriculas.item(i, 0).text(),
            self.janela_matriculas.tabelaMatriculas.item(i, 1).text(),
            self.janela_matriculas.tabelaMatriculas.item(i, 2).text(),
            self.janela_matriculas.tabelaMatriculas.item(i, 3).text(),
            self.janela_matriculas.tabelaMatriculas.item(i, 4).text()))


        self.janela_matriculas_atualizar.tabelaAtualizar.setRowCount(len(lista_de_dados))
        self.janela_matriculas_atualizar.tabelaAtualizar.setColumnCount(len(lista_de_dados[0]))
        self.janela_matriculas_atualizar.tabelaAtualizar.setHorizontalHeaderLabels(["Nome Aluno", "Matricula Ativa",
        "Tipo matricula",
        "Data inicio", "Data fim"])
        self.dados_antigos_atualizar = lista_de_dados
        
        self.lista_objetos_linedit = []
        style = ESTILO_LINEEDIT
        style2 = ESTILO_DATA
        style3 = ESTILO_COMBOBOX

        for i in range(len(lista_de_dados)): #linha
            for j in range(len(lista_de_dados[0])): #coluna
                item = None
                lista_temp = []
                if j == 0:
                    inputnormal = QLineEdit(self.janela_matriculas_atualizar.tabelaAtualizar)
                    inputnormal.setStyleSheet(style)
                    item = inputnormal.setText(str(lista_de_dados[i][j]))
                    lista_temp.append(inputnormal)
                    inputnormal.setEnabled(False)
                    self.janela_matriculas_atualizar.tabelaAtualizar.setCellWidget(i, j, inputnormal) 
                if j == 1:
                    matricula_ativa = str(lista_de_dados[i][j])
                    inputnormal = QComboBox(self.janela_matriculas_atualizar.tabelaAtualizar)     
                    inputnormal.addItem("Não possui")
                    inputnormal.addItem("Ativa")
                    inputnormal.addItem("Inativa")
                    if matricula_ativa == "Não possui":
                        inputnormal.setCurrentIndex(0)
                    elif matricula_ativa == "Ativa":
                        inputnormal.setCurrentIndex(1)
                    elif matricula_ativa == "Inativa":
                        inputnormal.setCurrentIndex(2)
                    inputnormal.setStyleSheet(style3)
                    lista_temp.append(inputnormal)
                    self.janela_matriculas_atualizar.tabelaAtualizar.setCellWidget(i, j, inputnormal) 
                if j == 2:
                    tipo_matricula = str(lista_de_dados[i][j])
                    inputnormal = QComboBox(self.janela_matriculas_atualizar.tabelaAtualizar)     
                    inputnormal.addItem("Não possui")
                    inputnormal.addItem("Mensal")
                    #inputnormal.addItem("Bimestral")
                    inputnormal.addItem("Trimestral")
                    inputnormal.addItem("Semestral")
                    inputnormal.addItem("Anual")
                    if tipo_matricula == "Não possui":
                        inputnormal.setCurrentIndex(0)
                    elif tipo_matricula == "Mensal":
                        inputnormal.setCurrentIndex(1)
                   # elif tipo_matricula == "Bimestral":
                #    inputnormal.setCurrentIndex(2)
                    elif tipo_matricula == "Trimestral":
                        inputnormal.setCurrentIndex(2)
                    elif tipo_matricula == "Semestral":
                        inputnormal.setCurrentIndex(3)
                    elif tipo_matricula == "Anual":
                        inputnormal.setCurrentIndex(4)
                    inputnormal.setStyleSheet(style3)
                    #item = inputnormal.setText(str(lista_de_dados[i][j]))
                    lista_temp.append(inputnormal)
                    self.janela_matriculas_atualizar.tabelaAtualizar.setCellWidget(i, j, inputnormal) 
                if j == 3: 
                    try:
                        inputnormal = QDateEdit(self.janela_matriculas_atualizar.tabelaAtualizar,calendarPopup=True)
                        inputnormal.setStyleSheet(style2)
                        date = None
                        date = dt.datetime.strptime(str(lista_de_dados[i][j]), '%d/%m/%Y')
                        inputnormal.setDateTime(date)
                    except:
                        date = dt.datetime.strptime("01/01/2000", '%d/%m/%Y')
                        inputnormal.setDateTime(date)
                    finally:
                        lista_temp.append(inputnormal)
                        self.janela_matriculas_atualizar.tabelaAtualizar.setCellWidget(i, j, inputnormal) 

                if j == 4:
                    try:
                        inputnormal = QDateEdit(self.janela_matriculas_atualizar.tabelaAtualizar,calendarPopup=True)
                        inputnormal.setStyleSheet(style2)
                        date = None
                        date = dt.datetime.strptime(str(lista_de_dados[i][j]), '%d/%m/%Y')
                        inputnormal.setDateTime(date)
                    except:
                        date = dt.datetime.strptime("01/01/2000", '%d/%m/%Y')
                        inputnormal.setDateTime(date) #QtCore.QDateTime.currentDateTime() <- pega data atual
                    finally:
                        lista_temp.append(inputnormal)
                        self.janela_matriculas_atualizar.tabelaAtualizar.setCellWidget(i, j, inputnormal) 

                self.lista_objetos_linedit.append(lista_temp)
                
                
        self.janela_matriculas_atualizar.show()


class AvaliacaoFisica(QMainWindow):
    def __init__(self):
        super().__init__()
        ### CARREGANDO TELAS QUE SERÃO USADAS ###
        self.janela_de_av_fisicas = uic.loadUi('src\\telas\\telas_alunos\\tela_bioimpendancia.ui')
        self.janela_atualizar_avFisicas = uic.loadUi('src\\telas\\telas_alunos\\atualizar_avFisica.ui')
        self.janela_de_av_fisicas.btn_fechar.clicked.connect(lambda: self.janela_de_av_fisicas.close())
        #self.load_spinner = Loadspinner()

        self.janela_de_av_fisicas.btn_abreJanelaAtualizar.clicked.connect(lambda: self.abrir_janela_atualizar_avFisica())
        self.janela_atualizar_avFisicas.btn_atualizarDados.clicked.connect(lambda: self.atualizar_dados())
        self.janela_atualizar_avFisicas.btn_sairJanelaAtualizar.clicked.connect(lambda: self.fechar_janela_atualizar())

        ###Sobrescrevendo evento de fechar janela de atualizar ##
        self.janela_atualizar_avFisicas.closeEvent = self.destroi_janela_atualizar

        ###botão de pesquisa ###
        self.janela_de_av_fisicas.btn_pesquisar.clicked.connect(lambda: self.pesquisar())
        self.janela_de_av_fisicas.inputBuscar.returnPressed.connect(self.pesquisar)

        ##atualizar##
        self.resultados_pesquisa = []
        

    ### MÉTODOS/FUNCIONALIDADES DA JANELA DE AV. FISICA###
    def starta_thread(self):
        threading.Thread(target=self.chama_mostrar_avfisica).start()

    def chama_mostrar_avfisica(self):
        time.sleep(1)
        global tabela_avfisica
        self.mostrar_avfisicas_tela(tabela_avfisica)

    def fechar_janela_atualizar(self):
        self.starta_thread()
        self.destroi_janela_atualizar()
        self.resultados_pesquisa = []

    def destroi_janela_atualizar(self, *args):
        global tabela_avfisica
        self.lista_objetos_linedit = []
        self.dados_antigos_atualizar = []
        self.registros_com_id = []
        self.resultados_pesquisa = []
        self.mostrar_avfisicas_tela(tabela_avfisica)
        self.janela_atualizar_avFisicas.close()

    def abrir_janela_avfisica(self, tabela):
        ## erro caso o usuario tente acessar os dados antes das tabelas carregarem ##
        if tabela == [()]:
            QtWidgets.QMessageBox.about(self.janela_de_av_fisicas,
             'Gerenciador de alunos', 'Ocorreu um erro ao acessar o banco de dados,\nVerifique sua conexão.')
            return

        self.janela_de_av_fisicas.show()
        self.mostrar_avfisicas_tela(tabela)

    def mostrar_avfisicas_tela(self, tabela):
    
        self.janela_de_av_fisicas.tabelaAvaliacoes.setRowCount(len(tabela))
        self.janela_de_av_fisicas.tabelaAvaliacoes.setColumnCount(len(tabela[0])-1)
        self.janela_de_av_fisicas.tabelaAvaliacoes.setHorizontalHeaderLabels(["Nome Aluno", "Massa gorda", "Massa magra", "Massa muscular",
         "Hidratação", "Densidade ossea", "Gordura Visceral", "Metabolismo Basal"])
        self.janela_de_av_fisicas.tabelaAvaliacoes.resizeRowsToContents()
        for i in range(len(tabela)): #linha
            for j in range(len(tabela[0])): #coluna
                if j == 8: break
                item = QtWidgets.QTableWidgetItem(f"{tabela[i][j+1]}")

                self.janela_de_av_fisicas.tabelaAvaliacoes.setItem(i,j, item)
        ## Reajustando o tamnho das células(colunoas) de acordo com o contúdo delas
        header = self.janela_de_av_fisicas.tabelaAvaliacoes.horizontalHeader()           # Colunas abaixo  
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)

    ### JANELA ATUALIZAR AVALIAÇÕES FÍSICAS ###
    def abrir_janela_atualizar_avFisica(self):
        global tabela_avfisica
        print(tabela_avfisica)
        dados = set(index.row() for index in self.janela_de_av_fisicas.tabelaAvaliacoes.selectedIndexes())
        if len(dados) < 1:
            QtWidgets.QMessageBox.about(self.janela_de_av_fisicas,
             'Gerenciador de avaliações físicas', 'Para atualizar, é necessario selecionar ao menos 1 registro.')
            return
        print(dados)
        lista_de_dados = []
        self.registros_com_id = []
        if len(self.resultados_pesquisa) > 0:
            for i in dados:
                self.registros_com_id.append(self.resultados_pesquisa[i])
        else:
            for i in dados:
                self.registros_com_id.append(tabela_avfisica[i])
        self.resultados_pesquisa = []

        for i, j in enumerate(self.registros_com_id):
            self.registros_com_id[i] = tuple(j)
        for i in dados:
            lista_de_dados.append((self.janela_de_av_fisicas.tabelaAvaliacoes.item(i, 0).text(),
            self.janela_de_av_fisicas.tabelaAvaliacoes.item(i, 1).text(),
            self.janela_de_av_fisicas.tabelaAvaliacoes.item(i, 2).text(),
            self.janela_de_av_fisicas.tabelaAvaliacoes.item(i, 3).text(),
            self.janela_de_av_fisicas.tabelaAvaliacoes.item(i, 4).text(),
            self.janela_de_av_fisicas.tabelaAvaliacoes.item(i, 5).text(),
            self.janela_de_av_fisicas.tabelaAvaliacoes.item(i, 6).text(),
            self.janela_de_av_fisicas.tabelaAvaliacoes.item(i, 7).text()))

        self.janela_atualizar_avFisicas.tabelaAtualizar.setRowCount(len(lista_de_dados))
        self.janela_atualizar_avFisicas.tabelaAtualizar.setColumnCount(len(lista_de_dados[0]))
        self.janela_atualizar_avFisicas.tabelaAtualizar.setHorizontalHeaderLabels(["Nome Aluno", "Massa gorda",
        "Massa magra", "Massa muscular",
        "Hidratação", "Densidade ossea", "Gordura Visceral", "Metabolismo Basal"])
        self.dados_antigos_atualizar = lista_de_dados
        
        self.lista_objetos_linedit = []
        style = "QLineEdit{font-size: 14px;\
                text-align: center;\
                color: white;\
                }"
        for i in range(len(lista_de_dados)): #linha
            for j in range(len(lista_de_dados[0])): #coluna
                item = None
                lista_temp = []
                if j == 0:
                    inputnormal = QLineEdit(self.janela_atualizar_avFisicas.tabelaAtualizar)
                    inputnormal.setStyleSheet(style)
                    item = inputnormal.setText(str(lista_de_dados[i][j]))
                    lista_temp.append(inputnormal)
                    inputnormal.setEnabled(False)
                    self.janela_atualizar_avFisicas.tabelaAtualizar.setCellWidget(i, j, inputnormal) 
                if j == 1:
                    inputnormal = QLineEdit(self.janela_atualizar_avFisicas.tabelaAtualizar)
                    inputnormal.setStyleSheet(style)
                    inputnormal.setInputMask('99')
                    inputnormal.setText(str(lista_de_dados[i][j]))
                    lista_temp.append(inputnormal)
                    self.janela_atualizar_avFisicas.tabelaAtualizar.setCellWidget(i, j, inputnormal) 
                if j == 2:
                    inputnormal = QLineEdit(self.janela_atualizar_avFisicas.tabelaAtualizar)
                    inputnormal.setStyleSheet(style)
                    inputnormal.setInputMask('99')
                    item = inputnormal.setText(str(lista_de_dados[i][j]))
                    lista_temp.append(inputnormal)
                    self.janela_atualizar_avFisicas.tabelaAtualizar.setCellWidget(i, j, inputnormal) 
                if j == 3:
                    inputnormal = QLineEdit(self.janela_atualizar_avFisicas.tabelaAtualizar)
                    inputnormal.setStyleSheet(style)
                    inputnormal.setInputMask('99')
                    item = inputnormal.setText(str(lista_de_dados[i][j]))
                    lista_temp.append(inputnormal)
                    self.janela_atualizar_avFisicas.tabelaAtualizar.setCellWidget(i, j, inputnormal) 
                if j == 4:
                    inputnormal = QLineEdit(self.janela_atualizar_avFisicas.tabelaAtualizar)
                    inputnormal.setStyleSheet(style)
                    inputnormal.setInputMask('99')
                    item = inputnormal.setText(str(lista_de_dados[i][j]))
                    lista_temp.append(inputnormal)
                    self.janela_atualizar_avFisicas.tabelaAtualizar.setCellWidget(i, j, inputnormal) 
                if j == 5:
                    inputnormal = QLineEdit(self.janela_atualizar_avFisicas.tabelaAtualizar)
                    inputnormal.setStyleSheet(style)
                    inputnormal.setInputMask('99')
                    item = inputnormal.setText(str(lista_de_dados[i][j]))
                    lista_temp.append(inputnormal)
                    self.janela_atualizar_avFisicas.tabelaAtualizar.setCellWidget(i, j, inputnormal) 
                if j == 6:
                    inputnormal = QLineEdit(self.janela_atualizar_avFisicas.tabelaAtualizar)
                    inputnormal.setStyleSheet(style)
                    inputnormal.setInputMask('99')
                    item = inputnormal.setText(str(lista_de_dados[i][j]))
                    lista_temp.append(inputnormal)
                    self.janela_atualizar_avFisicas.tabelaAtualizar.setCellWidget(i, j, inputnormal) 
                if j == 7:
                    inputnormal = QLineEdit(self.janela_atualizar_avFisicas.tabelaAtualizar)
                    inputnormal.setStyleSheet(style)
                    inputnormal.setInputMask('9999')
                    item = inputnormal.setText(str(lista_de_dados[i][j]))
                    lista_temp.append(inputnormal)
                    self.janela_atualizar_avFisicas.tabelaAtualizar.setCellWidget(i, j, inputnormal) 
                self.lista_objetos_linedit.append(lista_temp)
                
        print(self.registros_com_id)
        self.janela_atualizar_avFisicas.show()

    def atualizar_dados(self):
        global tabela_avfisica
        print(tabela_avfisica)
       
        dados_update = []
        update = False
        lista_aux = []
        lista_aux2 = []
        lista_objetos = []

        self.lista_objetos_linedit = [item[0].text() for item in self.lista_objetos_linedit]
        lista = []
        lista_oficial = []
        i = 0
        for item in self.lista_objetos_linedit:
            lista.append(item)
            if i != 7:
                i += 1
            else:
                lista.insert(0, 0)
                lista_oficial.append(tuple(lista))
                lista = []
                i = 0
        
        self.lista_objetos_linedit = lista_oficial
        

        #print(self.lista_objetos_linedit)
        #print(self.registros_com_id)###Terminar essas coisas aqui. A questão de pegar a lista sem id e a com id, e mandar pro banco só a que tem o id

        dados_antigos = []
        cont = 0
        for j, registros_com_id in enumerate(self.registros_com_id):
            for i in range(len(registros_com_id)):
                if i == 0: continue
                if str(registros_com_id[i]) != self.lista_objetos_linedit[j][i]:
                    # print(type(registros_com_id[i]) , type(self.lista_objetos_linedit[j][i]))
                    # print(registros_com_id[i] , self.lista_objetos_linedit[j][i])
                    update = True
                lista_aux.append(self.lista_objetos_linedit[j][i])  
                lista_aux2.append(registros_com_id[i])
                if update and cont == 7:
                    lista_aux.insert(0, registros_com_id[0])
                    lista_aux2.insert(0, registros_com_id[0])
                    dados_update.append(tuple(lista_aux))
                    dados_antigos.append(tuple(lista_aux2))
                    cont = -1
                    update = False
                    lista_aux = []
                    lista_aux2 = []
                elif not update and cont == 7:
                    lista_aux = []
                    lista_aux2 = []
                    cont = -1
                cont += 1

        ###Aqui comecaria um load spinner


        if dados_update:
            atualizar = db.AvFisica()

            for dado in dados_update:
                resposta = atualizar.atualizar_avFisica(id_aluno=dado[0], massaGorda=dado[2],massaMagra=dado[3],
                massaMuscular=dado[4], hidratacao=dado[5],densidadeOssea=dado[6],gorduraVisceral=dado[7], metabolismoBasal=dado[8])
                if resposta == "Erro":
                    QtWidgets.QMessageBox.about(self.janela_atualizar_avFisicas,
                    'Gerenciador de av.fisicas', 'Ocorreu um erro ao atualizar os dados.')
                    self.destroi_janela_atualizar()
                    return

        
        threading.Thread(target=carrega_tabela_avfisica).start()
        QtWidgets.QMessageBox.about(self.janela_atualizar_avFisicas,
        'Gerenciador de av.fisicas', 'Dados atualizados com Sucesso!')
        self.registros_com_id = []
        self.lista_objetos_linedit = []
        self.dados_antigos_atualizar = []
        self.fechar_janela_atualizar()
    
    def pesquisar(self):
        global tabela_avfisica

        pesquisa = self.janela_de_av_fisicas.inputBuscar.text()
        self.resultados_pesquisa = []
        if self.janela_de_av_fisicas.radioNomeAluno.isChecked():
            nome_buscado = pesquisa.upper()
            for aluno in tabela_avfisica:
                if nome_buscado in aluno[1].upper():
                    self.resultados_pesquisa.append(aluno)
            self.janela_de_av_fisicas.inputBuscar.setText("")
            if self.resultados_pesquisa:
                self.mostrar_avfisicas_tela(self.resultados_pesquisa)
            else:
                QtWidgets.QMessageBox.about(self.janela_de_av_fisicas,
             'Gerenciador de alunos', f'Aluno "{nome_buscado}" não encontrado.')
            return
        if self.janela_de_av_fisicas.radioTodosRegistros.isChecked():
            self.resultados_pesquisa = []
            self.mostrar_avfisicas_tela(tabela_avfisica)
        return


class JanelaAlunos(QMainWindow):
    def __init__(self):
        super().__init__()

        ### CARREGANDO TELAS QUE SERÃO USADAS ###
        self.janela_alunos = uic.loadUi('src\\telas\\telas_alunos\\tela_alunos.ui')
        self.janela_alunos_inserir = uic.loadUi('src\\telas\\telas_alunos\\inserir_alunos.ui')
        self.janela_alunos_atualizar = uic.loadUi('src\\telas\\telas_alunos\\atualizar_alunos.ui')
        self.janela_de_av_fisicas = AvaliacaoFisica()
        self.janela_excluir = uic.loadUi('src\\telas\\telas_alunos\\excluir_alunos.ui')

        ### FECHAR A JANELA ###
        self.janela_alunos.closeEvent = self.destroi_janela_alunos
        self.janela_alunos.btn_fechar.clicked.connect(lambda: self.destroi_janela_alunos())

        ### PESQUISAR ###
        self.janela_alunos.btn_pesquisar.clicked.connect(self.pesquisar)
        self.janela_alunos.input_buscar.returnPressed.connect(self.pesquisar)
        
        ### ABRIR E FECHAR JANELA INSERIR ###
        self.janela_alunos.btn_abreJanelaInserir.clicked.connect(lambda: self.janela_alunos_inserir.show())
        self.janela_alunos_inserir.closeEvent = self.destroi_janela_inserir
        self.janela_alunos_inserir.btn_fecharJanelaInserir.clicked.connect(lambda: self.fechar_janela_inserir_alunos())


        ### ABRIR E FECHAR JANELA EXCLUIR ###
        self.janela_excluir.btn_sairJanelaExcluir.clicked.connect(lambda: self.fechar_janela_excluir())

        self.janela_excluir.btn_excluirDados.clicked.connect(lambda: self.excluir_dados())
        self.janela_excluir.closeEvent = self.destroi_janela_excluir
    
        
        self.janela_alunos_inserir.btn_iserirDados.clicked.connect(self.inserir_dados)

        ### INSTALANDO EVENT FILTERS NOS INPUTS ##
        self.janela_alunos_inserir.cpfAluno.installEventFilter(self)
        self.janela_alunos_inserir.idadeAluno.installEventFilter(self)
        self.janela_alunos_inserir.nomeAluno.installEventFilter(self)
        self.janela_alunos_inserir.telefoneAluno.installEventFilter(self)
        self.janela_alunos_inserir.emailAluno.installEventFilter(self)

        ### ABRIR E FECHAR JANELA ATUALIZAR ###
        self.janela_alunos.btn_abreJanelaAtualizar.clicked.connect(lambda: self.abrir_janela_atualizar_alunos())
    
        self.janela_alunos_atualizar.btn_sairJanelaAtualizar.clicked.connect(lambda: self.fechar_janela_atualizar())
        self.janela_alunos_atualizar.btn_atualizarDados.clicked.connect(self.atualizar_dados)
        self.janela_alunos_atualizar.closeEvent = self.destroi_janela_atualizar
        
        ### BOTÃO EXCLUIR DADOS ###
        self.janela_alunos.btn_excluirRegistro.clicked.connect(self.abrir_janela_excluir)

        ### ABRIR JANELA E FECHAR TELA DE AV. FISICAS ###
        self.janela_alunos.btn_telaAvFisica.clicked.connect(lambda: self.janela_de_av_fisicas.abrir_janela_avfisica(tabela_avfisica))
        
    
    ### MÉTODOS AUXILIARES PARA LIDAR COM EVENTOS ###
    def starta_thread(self):
        threading.Thread(target=self.chama_mostrar_alunos).start()

    def chama_mostrar_alunos(self):
        time.sleep(1)
        global tabela_alunos
        self.mostrar_alunos_tela(tabela_alunos)

    def destroi_janela_atualizar(self, *args):
        global tabela_alunos
        self.mostrar_alunos_tela(tabela_alunos)
        self.lista_objetos_linedit = []
        self.dados_antigos_atualizar = []
        self.janela_alunos_atualizar.close()

    def destroi_janela_alunos(self, *args):
        threading.Thread(target=carrega_tabela_alunos).start()
        self.janela_alunos.close()

    def destroi_janela_inserir(self, *args):
        global tabela_alunos
        self.mostrar_alunos_tela(tabela_alunos)
        self.janela_alunos_inserir.close()

    def destroi_janela_excluir(self, *args):
        global tabela_alunos
        self.mostrar_alunos_tela(tabela_alunos)
        self.lista_dados_excluir = []
        self.janela_excluir.close()

    def fechar_janela_atualizar(self):
        self.starta_thread()
        self.lista_objetos_linedit = []
        self.dados_antigos_atualizar = []
        self.destroi_janela_atualizar()

    def fechar_janela_excluir(self):
            self.starta_thread()
            self.destroi_janela_excluir()

    def fechar_janela_inserir_alunos(self):
        self.starta_thread()
        self.janela_alunos_inserir.nomeAluno.setText('')
        self.janela_alunos_inserir.emailAluno.setText('')
        self.janela_alunos_inserir.idadeAluno.setText('')
        self.janela_alunos_inserir.cpfAluno.setText('')
        self.janela_alunos_inserir.telefoneAluno.setText('')
        self.janela_alunos_inserir.idadeAluno.setInputMask('')
        self.janela_alunos_inserir.cpfAluno.setInputMask('')
        self.janela_alunos_inserir.telefoneAluno.setInputMask('')
        self.destroi_janela_inserir()

    def abrir_janela_atualizar_alunos(self):

        dados = set(index.row() for index in self.janela_alunos.tabelaAlunos.selectedIndexes())
        if len(dados) < 1:
            QtWidgets.QMessageBox.about(self.janela_alunos,
             'Gerenciador de alunos', 'Para atualizar, é necessario selecionar ao menos 1 registro.')
            return
        lista_de_dados = []
        for i in dados:
            lista_de_dados.append((self.janela_alunos.tabelaAlunos.item(i, 0).text(),self.janela_alunos.tabelaAlunos.item(i, 1).text(),
            self.janela_alunos.tabelaAlunos.item(i, 2).text(), self.janela_alunos.tabelaAlunos.item(i, 3).text(),
            self.janela_alunos.tabelaAlunos.item(i, 4).text()))


        self.janela_alunos_atualizar.tabelaAtualizar.setRowCount(len(lista_de_dados))
        self.janela_alunos_atualizar.tabelaAtualizar.setColumnCount(len(lista_de_dados[0]))
        self.janela_alunos_atualizar.tabelaAtualizar.setHorizontalHeaderLabels(["Nome Aluno", "Idade aluno", "CPF aluno",
        "Telefone aluno", "Email aluno"])
        self.dados_antigos_atualizar = lista_de_dados
        
        self.lista_objetos_linedit = []
        style = "QLineEdit{font-size: 14px;\
                text-align: center;\
                color: white;\
                }"
        for i in range(len(lista_de_dados)): #linha
            for j in range(len(lista_de_dados[0])): #coluna
                item = None
                lista_temp = []
                if j == 0:
                    inputnormal = QLineEdit(self.janela_alunos.tabelaAlunos)
                    inputnormal.setStyleSheet(style)
                    item = inputnormal.setText(str(lista_de_dados[i][j]))
                    lista_temp.append(inputnormal)
                    self.janela_alunos_atualizar.tabelaAtualizar.setCellWidget(i, j, inputnormal) 
                if j == 1:
                    inputidade = QLineEdit(self.janela_alunos.tabelaAlunos)
                    inputidade.setStyleSheet(style)
                    inputidade.setInputMask('99')
                    inputidade.setText(str(lista_de_dados[i][j]))
                    lista_temp.append(inputidade)
                    self.janela_alunos_atualizar.tabelaAtualizar.setCellWidget(i, j, inputidade) 
                if j == 2:
                    inputcpf = QLineEdit(self.janela_alunos.tabelaAlunos)
                    inputcpf.setStyleSheet(style)
                    inputcpf.setInputMask('999.999.999-99')
                    item = inputcpf.setText(str(lista_de_dados[i][j]))
                    lista_temp.append(inputcpf)
                    self.janela_alunos_atualizar.tabelaAtualizar.setCellWidget(i, j, inputcpf) 
                if j == 3:
                    inputtelefone = QLineEdit(self.janela_alunos.tabelaAlunos)
                    inputtelefone.setStyleSheet(style)
                    inputtelefone.setInputMask('(99)09999-9999')
                    item = inputtelefone.setText(str(lista_de_dados[i][j]))
                    lista_temp.append(inputtelefone)
                    self.janela_alunos_atualizar.tabelaAtualizar.setCellWidget(i, j, inputtelefone) 
                if j == 4:
                    inputnormal = QLineEdit(self.janela_alunos.tabelaAlunos)
                    inputnormal.setStyleSheet(style)
                    item = inputnormal.setText(str(lista_de_dados[i][j]))
                    lista_temp.append(inputnormal)
                    self.janela_alunos_atualizar.tabelaAtualizar.setCellWidget(i, j, inputnormal) 
                
                self.lista_objetos_linedit.append(lista_temp)
                
                
        self.janela_alunos_atualizar.show()

    def eventFilter(self, source, event):
        """  Este trecho de código é um filtro de evento, quando se é clicado em cima de um input
            automaticamente é detectado este evento e é posicionado o cursor para o inicio do input
        """
        if source == self.janela_alunos_inserir.cpfAluno and event.type() == QtCore.QEvent.MouseButtonPress \
        or source == self.janela_alunos_inserir.idadeAluno and (event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab):
            self.janela_alunos_inserir.cpfAluno.setInputMask('999.999.999-99')
            self.janela_alunos_inserir.cpfAluno.setFocus(QtCore.Qt.MouseFocusReason)
            self.janela_alunos_inserir.cpfAluno.setCursorPosition(0)
            return True
        if source == self.janela_alunos_inserir.idadeAluno and event.type() == QtCore.QEvent.MouseButtonPress\
        or source == self.janela_alunos_inserir.nomeAluno and (event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab):
            self.janela_alunos_inserir.idadeAluno.setInputMask('99')
            self.janela_alunos_inserir.idadeAluno.setFocus(QtCore.Qt.MouseFocusReason)
            self.janela_alunos_inserir.idadeAluno.setCursorPosition(0)
            return True
        if source == self.janela_alunos_inserir.telefoneAluno and event.type() == QtCore.QEvent.MouseButtonPress\
        or source == self.janela_alunos_inserir.cpfAluno and (event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab):
            self.janela_alunos_inserir.telefoneAluno.setInputMask('(99)09999-9999')
            self.janela_alunos_inserir.telefoneAluno.setFocus(QtCore.Qt.MouseFocusReason)
            self.janela_alunos_inserir.telefoneAluno.setCursorPosition(0)
            return True
        return super().eventFilter(source, event)
    
    ### MÉTODOS/FUNCIONALIDADES DA JANELA DE ALUNOS###
    def abrir_janela(self, tabela):
        ## erro caso o usuario tente acessar os dados antes das tabelas carregarem ##
        if tabela == [()]:
            QtWidgets.QMessageBox.about(self.janela_alunos,
             'Gerenciador de alunos', 'Ocorreu um erro ao acessar o banco de dados,\nVerifique sua conexão.')
            return

        self.janela_alunos.show()
        self.mostrar_alunos_tela(tabela)

    def mostrar_alunos_tela(self, tabela):
        self.janela_alunos.tabelaAlunos.setRowCount(len(tabela))
        self.janela_alunos.tabelaAlunos.setColumnCount(len(tabela[0])-1)
        self.janela_alunos.tabelaAlunos.setHorizontalHeaderLabels(["Nome", "Idade", "Cpf", "Telefone", "Email"])
        self.janela_alunos.tabelaAlunos.resizeRowsToContents()
        for i in range(len(tabela)): #linha
            for j in range(len(tabela[0])): #coluna
                if j == 5: break
                item = QtWidgets.QTableWidgetItem(f"{tabela[i][j+1]}")

                self.janela_alunos.tabelaAlunos.setItem(i,j, item)
        ## Reajustando o tamnho das células(colunoas) de acordo com o contúdo delas
        header = self.janela_alunos.tabelaAlunos.horizontalHeader()           # Colunas abaixo  
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)# Nome
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)# Cpf
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)# Número tel
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)# Email

    def pesquisar(self):
        global tabela_alunos
        pesquisa = self.janela_alunos.input_buscar.text()
        resultados_pesquisa = []
        if self.janela_alunos.radioButtonNomeAluno.isChecked():
            nome_buscado = pesquisa.upper()
            for aluno in tabela_alunos:
                if nome_buscado in aluno[1].upper():
                    resultados_pesquisa.append(aluno)
            self.janela_alunos.input_buscar.setText("")
            if resultados_pesquisa:
                self.mostrar_alunos_tela(resultados_pesquisa)
            else:
                QtWidgets.QMessageBox.about(self.janela_alunos,
             'Gerenciador de alunos', f'Aluno "{nome_buscado}" não encontrado.')
            return
        if self.janela_alunos.radioButtonIdadeAluno.isChecked():
            idade_buscada = pesquisa
            if self.janela_alunos.radioButtonIdadeAluno.isChecked():
                for aluno in tabela_alunos:
                    if idade_buscada == aluno[2]:
                        resultados_pesquisa.append(aluno)
                self.janela_alunos.input_buscar.setText("")
                if resultados_pesquisa:
                    self.mostrar_alunos_tela(resultados_pesquisa)
                else:
                    QtWidgets.QMessageBox.about(self.janela_alunos,
             'Gerenciador de alunos', f'Aluno com idade "{idade_buscada}" não encontrado.')
                return
        if self.janela_alunos.radioButtonCpfAluno.isChecked():
            cpf_buscado = pesquisa
            for aluno in tabela_alunos:
                cpf = aluno[3]
                cpf = cpf.replace(".", "").replace("-", "")
                if cpf_buscado in aluno[3] or cpf_buscado in cpf:
                    resultados_pesquisa.append(aluno)
            print(resultados_pesquisa)
            self.janela_alunos.input_buscar.setText("")
            if resultados_pesquisa:
                self.mostrar_alunos_tela(resultados_pesquisa)
            else:
                QtWidgets.QMessageBox.about(self.janela_alunos,
             'Gerenciador de alunos', f'Aluno com cpf "{cpf_buscado}" não encontrado.')
            return
        if self.janela_alunos.radioButtonTelefoneAluno.isChecked():
            telefone_buscado = pesquisa
            for aluno in tabela_alunos:
                telefone = aluno[4]
                telefone = telefone.replace("(", "").replace(")", "").replace("-", "")
                if telefone_buscado in aluno[4] or telefone_buscado in telefone:
                    resultados_pesquisa.append(aluno)
            self.janela_alunos.input_buscar.setText("")
            if resultados_pesquisa:
                self.mostrar_alunos_tela(resultados_pesquisa)
            else:
                QtWidgets.QMessageBox.about(self.janela_alunos,
             'Gerenciador de alunos', f'Aluno com telefone "{telefone_buscado}" não encontrado.')
            return
            
        if self.janela_alunos.radioButtonEmailAluno.isChecked():
            email_buscado = pesquisa
            for aluno in tabela_alunos:
                if email_buscado in aluno[5]:
                    resultados_pesquisa.append(aluno)
            self.janela_alunos.input_buscar.setText("")
            if resultados_pesquisa:
                self.mostrar_alunos_tela(resultados_pesquisa)
            else:
                QtWidgets.QMessageBox.about(self.janela_alunos,
             'Gerenciador de alunos', f'Aluno com email "{email_buscado}" não encontrado.')
            return
        if self.janela_alunos.radioButtonTodosAlunos.isChecked():
            self.mostrar_alunos_tela(tabela_alunos)

    def abrir_janela_excluir(self):
        dados = set(index.row() for index in self.janela_alunos.tabelaAlunos.selectedIndexes())
        if len(dados) < 1:
            QtWidgets.QMessageBox.about(self.janela_alunos,
             'Gerenciador de alunos', 'Para Excluir um aluno, é necessario selecionar ao menos 1 registro.')
            return
        lista_de_dados = []
        for i in dados:
            lista_de_dados.append((self.janela_alunos.tabelaAlunos.item(i, 0).text(),self.janela_alunos.tabelaAlunos.item(i, 1).text(),
            self.janela_alunos.tabelaAlunos.item(i, 2).text(), self.janela_alunos.tabelaAlunos.item(i, 3).text(),
            self.janela_alunos.tabelaAlunos.item(i, 4).text()))


        self.janela_excluir.tabelaExcluir.setRowCount(len(lista_de_dados))
        self.janela_excluir.tabelaExcluir.setColumnCount(len(lista_de_dados[0]))
        self.janela_excluir.tabelaExcluir.setHorizontalHeaderLabels(["Nome Aluno", "Idade aluno", "CPF aluno",
        "Telefone aluno", "Email aluno"])
        
        
        for i in range(len(lista_de_dados)): #linha
            for j in range(len(lista_de_dados[0])): #coluna
                item = QtWidgets.QTableWidgetItem(f"{lista_de_dados[i][j]}")
                self.janela_excluir.tabelaExcluir.setItem(i,j, item)
        self.lista_dados_excluir = lista_de_dados

        header = self.janela_excluir.tabelaExcluir.horizontalHeader()           # Colunas abaixo  
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.janela_excluir.show()

    def inserir_dados(self):
        ### PEGANDO OS DADOS DOS CAMPOS DE ENTRADA ###
        nomeAluno = self.janela_alunos_inserir.nomeAluno.text()
        idadeAluno = self.janela_alunos_inserir.idadeAluno.text()
        cpfAluno = self.janela_alunos_inserir.cpfAluno.text()
        telefoneAluno = self.janela_alunos_inserir.telefoneAluno.text()
        emailAluno = self.janela_alunos_inserir.emailAluno.text()
        global tabela_alunos

        ### FAZENDO TODAS AS VERIFICAÇÕES PARA INSERIR NO BD ###
       
        ##verificação do nome do aluno##
        try:
            validacoes.valida_campo_vazio(nomeAluno)
            validacoes.valida_nome(nomeAluno)
        except erros.CaractereInvalido:
            QtWidgets.QMessageBox.about(self.janela_alunos_inserir,
                'Gerenciador de alunos', 'Caractere inválido usado no nome do aluno. Por favor use apenas\n\
                    letras maiusculas, minusculas e acentuação simples.')
            return
        except erros.CampoVazio:
            QtWidgets.QMessageBox.about(self.janela_alunos_inserir,
                'Gerenciador de alunos', 'Digite um nome antes de inserir.')
            return
        except erros.NomeCurto:
            QtWidgets.QMessageBox.about(self.janela_alunos_inserir,
                'Gerenciador de alunos', 'O nome precisa ter no mínimo 6 caracteres.')
            return
        ##Verificação da idade do aluno##
        try:
            validacoes.valida_campo_vazio(idadeAluno)
            idadeAluno = int(idadeAluno)
            validacoes.valida_idade(idadeAluno) 
        except erros.IdadeInvalida:
            QtWidgets.QMessageBox.about(self.janela_alunos_inserir,
                'Gerenciador de alunos', 'A idade precisar ser entre 12 e 90 anos. ')
            return
        except erros.CampoVazio:
            QtWidgets.QMessageBox.about(self.janela_alunos_inserir,
                'Gerenciador de alunos', 'Digite uma idade antes de inserir.')
            return

        ##Verificação do cpf do aluno##
        try:
            validacoes.valida_campo_vazio(cpfAluno)
            isvalid = validacoes.valida_cpf(cpfAluno)
            validacoes.valida_cpf_ja_existente(cpfAluno, tabela_alunos)
            if not isvalid:
                raise erros.CaractereInvalido
        except erros.CampoVazio:
            QtWidgets.QMessageBox.about(self.janela_alunos_inserir,
                'Gerenciador de alunos', 'Digite um cpf antes de inserir.')
            return
        except erros.CaractereInvalido:
            QtWidgets.QMessageBox.about(self.janela_alunos_inserir,
                'Gerenciador de alunos', 'Cpf inválido.')
            return
        except erros.CpfJaExistente:
            QtWidgets.QMessageBox.about(self.janela_alunos_inserir,
                'Gerenciador de alunos', 'Cpf já existe na tabela de alunos.')
            return
        ##Verificação do telefone do aluno ##
        try:
            validacoes.valida_campo_vazio(telefoneAluno)
            validacoes.valida_telefone(telefoneAluno)
        except erros.CampoVazio:
            QtWidgets.QMessageBox.about(self.janela_alunos_inserir,
                'Gerenciador de alunos', 'Digite um telefone antes de inserir.')
            return
        except erros.TelefoneInexistente:
            QtWidgets.QMessageBox.about(self.janela_alunos_inserir,
                'Gerenciador de alunos', f'O telefone "{telefoneAluno}"" é inválido.')
            return

        ## Verificação do email do aluno ##
        try:
            validacoes.valida_campo_vazio(emailAluno)
            if not validacoes.valida_email_sintaxe(emailAluno):
                QtWidgets.QMessageBox.about(self.janela_alunos_inserir,
                'Gerenciador de alunos', 'Por favor insira um email válido.')
                return
        except erros.CampoVazio:
            QtWidgets.QMessageBox.about(self.janela_alunos_inserir,
                'Gerenciador de alunos', 'Digite um Email antes de inserir.')
            return
        print("Aluno inserido com sucesso")
        senha = ''
        for i in range(8):
            senha += choice(string.ascii_lowercase + string.digits)
        senha_hasheada = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())
        try:
            usuario = nomeAluno.split(' ')[0][0:2:] + nomeAluno.split(' ')[1]
        except:
            usuario = nomeAluno.split(' ')[0][0:2:] + cpfAluno[0:2:]
        inserir = db.DadosAlunos()
        inserir.inserir_dados_sem_id(nomeAluno, idadeAluno, cpfAluno, telefoneAluno, emailAluno, usuario, senha_hasheada.decode("utf-8"))
        threading.Thread(target=carrega_tabela_alunos).start()
        threading.Thread(target=carrega_tabela_avfisica).start()      
        threading.Thread(target=carrega_tabela_matricula).start()  
        self.starta_thread()
        threading.Thread(target=google.envia_email_credenciais_mobile, args=(usuario, senha, emailAluno)).start()
        QtWidgets.QMessageBox.about(self.janela_alunos_inserir,
                'Sucesso!', "Aluno inserido com sucesso! Email com credenciais do aplicativo móvel enviado.")
        self.janela_alunos_inserir.cpfAluno.setInputMask('')
        self.janela_alunos_inserir.telefoneAluno.setInputMask('')
        self.janela_alunos_inserir.idadeAluno.setInputMask('')
        self.janela_alunos_inserir.nomeAluno.setText("")
        self.janela_alunos_inserir.idadeAluno.setText("")
        self.janela_alunos_inserir.cpfAluno.setText("")
        self.janela_alunos_inserir.telefoneAluno.setText("")
        self.janela_alunos_inserir.emailAluno.setText("")

    def excluir_dados(self):
        dados_delete = []
        for i in self.lista_dados_excluir:
            lista_aux = []
            for j in i:
                lista_aux.append(j)
            dados_delete.append(tuple(lista_aux))
        self.lista_dados_excluir = []
        print(dados_delete)

        ## Load spinner aqui
        excluir = db.DadosAlunos()
        for i in range(len(dados_delete)):
            retorno = excluir.excluir_aluno(dados_delete[i][0], dados_delete[i][1],
            dados_delete[i][2], dados_delete[i][3], dados_delete[i][4])
            if retorno == "Erro":
                QtWidgets.QMessageBox.about(self.janela_excluir,
             'Gerenciador de alunos', 'Ocorreu um erro ao excluir os dados.')
                self.fechar_janela_excluir()

        ## Fim load spinner aqui
        threading.Thread(target=carrega_tabela_alunos).start()
        threading.Thread(target=carrega_tabela_avfisica).start()
        threading.Thread(target=carrega_tabela_matricula).start() 
        QtWidgets.QMessageBox.about(self.janela_excluir,
             'Gerenciador de alunos', 'Dados Excluidos com Sucesso!')

        self.fechar_janela_excluir()

    def atualizar_dados(self):
        dados_update = []
        update = False
        lista_aux = []
        lista_aux2 = []

        self.lista_objetos_linedit = [item[0].text() for item in self.lista_objetos_linedit]
        lista = []
        for i in range(len(self.dados_antigos_atualizar)):
            for j in range(len(self.dados_antigos_atualizar[i])):
               lista.append(self.dados_antigos_atualizar[i][j])
     
        dados_antigos = []
        cont = 0
        for i in range(len(self.lista_objetos_linedit)):
            if lista[i] != self.lista_objetos_linedit[i]:
                update = True
            lista_aux.append(self.lista_objetos_linedit[i])  
            lista_aux2.append(lista[i])  
            if update and cont == 4:
                dados_update.append(tuple(lista_aux))
                dados_antigos.append(tuple(lista_aux2))
                cont = -1
                update = False
                lista_aux = []
                lista_aux2 = []
            elif not update and cont == 4:
                lista_aux = []
                lista_aux2 = []
                cont = -1

            cont += 1
        ###Aqui comecaria um load spinner
        atualizar = db.DadosAlunos()
        for i in range(len(dados_update)):
             ##verificação do nome do aluno##
            try:
                validacoes.valida_campo_vazio(dados_update[i][0])
                validacoes.valida_nome(dados_update[i][0])
            except erros.CaractereInvalido:
                QtWidgets.QMessageBox.about(self.janela_alunos_atualizar,
                    'Gerenciador de alunos', f'Caractere inválido usado no nome "{dados_update[i][0]}". Por favor use apenas\n\
                        letras maiusculas, minusculas e acentuação simples.')
                self.abrir_janela_atualizar_alunos()
                return
            except erros.CampoVazio:
                QtWidgets.QMessageBox.about(self.janela_alunos_atualizar,
                    'Gerenciador de alunos', 'Digite um nome em todos os campos de nome antes de atualizar os dados.')
                self.abrir_janela_atualizar_alunos()
                return
            except erros.NomeCurto:
                QtWidgets.QMessageBox.about(self.janela_alunos_atualizar,
                    'Gerenciador de alunos', f'O nome "{dados_update[i][0]}" precisa ter no mínimo 6 caracteres.')
                self.abrir_janela_atualizar_alunos()
                return
            ##Verificação da idade do aluno##
            try:
                validacoes.valida_campo_vazio(dados_update[i][1])
                idadeAluno = int(dados_update[i][1])
                validacoes.valida_idade(idadeAluno) 
            except erros.IdadeInvalida:
                QtWidgets.QMessageBox.about(self.janela_alunos_atualizar,
                    'Gerenciador de alunos', f'A idade do aluno "{dados_update[i][0]}" precisa estar entre 12 e 90 anos. ')
                self.abrir_janela_atualizar_alunos()
                return
            except erros.CampoVazio:
                QtWidgets.QMessageBox.about(self.janela_alunos_atualizar,
                    'Gerenciador de alunos', f'Digite uma idade para o aluno "{dados_update[i][0]}" antes de atualizar os dados.')
                self.abrir_janela_atualizar_alunos()
                return

            ##Verificação do cpf do aluno##
            try:
                validacoes.valida_campo_vazio(dados_update[i][2])
                isvalid = validacoes.valida_cpf(dados_update[i][2])
                if not isvalid:
                    raise erros.CaractereInvalido
            except erros.CampoVazio:
                QtWidgets.QMessageBox.about(self.janela_alunos_atualizar,
                    'Gerenciador de alunos', f'Digite um cpf para o aluno "{dados_update[i][0]}" antes de atualizar os dados.')
                self.abrir_janela_atualizar_alunos()
                return
            except erros.CaractereInvalido:
                QtWidgets.QMessageBox.about(self.janela_alunos_atualizar,
                    'Gerenciador de alunos', f'Cpf "{dados_update[i][2]}" do aluno "{dados_update[i][0]}" é inválido.')
                self.abrir_janela_atualizar_alunos()
                return

            ##Verificação do telefone do aluno ##
            try:
                validacoes.valida_campo_vazio(dados_update[i][3])
                validacoes.valida_telefone(dados_update[i][3])
            except erros.CampoVazio:
                QtWidgets.QMessageBox.about(self.janela_alunos_atualizar,
                    'Gerenciador de alunos', f'Digite um telefone para o aluno "{dados_update[i][0]}" antes de atualizar os dados.')
                self.abrir_janela_atualizar_alunos()
                return
            except erros.TelefoneInexistente:
                QtWidgets.QMessageBox.about(self.janela_alunos_atualizar,
                    'Gerenciador de alunos', f'O telefone "{dados_update[i][3]}" do aluno "{dados_update[i][0]}" é inválido.')
                self.abrir_janela_atualizar_alunos()
                return

            ## Verificação do email do aluno ##
            try:
                validacoes.valida_campo_vazio(dados_update[i][4])
                if not validacoes.valida_email_sintaxe(dados_update[i][4]):
                    QtWidgets.QMessageBox.about(self.janela_alunos_atualizar,
                    'Gerenciador de alunos', f'Email "{dados_update[i][4]}" do aluno "{dados_update[i][0]}" inválido')
                    self.abrir_janela_atualizar_alunos()
                    return
            except erros.CampoVazio:
                QtWidgets.QMessageBox.about(self.janela_alunos_atualizar,
                    'Gerenciador de alunos', f'Digite um Email para o aluno "{dados_update[i][0]}" antes de atualizar os dados.')
                self.abrir_janela_atualizar_alunos()
                return
            retorno = atualizar.atualizar_aluno(dados_update[i][0], dados_update[i][1], dados_update[i][2],
            dados_update[i][3], dados_update[i][4], dados_antigos[i][0], dados_antigos[i][1], dados_antigos[i][2],
            dados_antigos[i][3], dados_antigos[i][4])
            if retorno == "Erro":
                QtWidgets.QMessageBox.about(self.janela_alunos_atualizar,
             'Gerenciador de alunos', 'Ocorreu um erro ao atualizar os alunos.')
                self.fechar_janela_atualizar()
        threading.Thread(target=carrega_tabela_alunos).start()
        ### Aqui acabaria o loadspinner
        QtWidgets.QMessageBox.about(self.janela_alunos_atualizar,
             'Gerenciador de alunos', 'Dados atualizados com Sucesso!')

        self.lista_objetos_linedit = []
        self.dados_antigos_atualizar = []
        self.fechar_janela_atualizar()


class JanelaEstoque(QMainWindow):
    def __init__(self):
        super().__init__()

        ### CARREGANDO TELAS QUE SERÃO USADAS ###
        self.janela_estoque = uic.loadUi('src\\telas\\telas_estoque\\tela_estoque.ui')
        self.janela_estoque_inserir = uic.loadUi('src\\telas\\telas_estoque\\inserir_produto.ui')
        self.janela_estoque_atualizar = uic.loadUi('src\\telas\\telas_estoque\\atualizar_produto.ui')
        self.janela_estoque_excluir = uic.loadUi('src\\telas\\telas_estoque\\excluir_produto.ui')

        ### FECHAR A JANELA ###
        self.janela_estoque.btn_fechar.clicked.connect(lambda: self.janela_estoque.close())

        ### PESQUISAR ###
        self.janela_estoque.btn_pesquisar.clicked.connect(self.pesquisar)
        self.janela_estoque.input_buscar.returnPressed.connect(self.pesquisar)
        self.resultados_pesquisa = []
        
        ### ABRIR E FECHAR JANELA INSERIR ###
        self.janela_estoque.btn_abreJanelaInserir.clicked.connect(lambda: self.janela_estoque_inserir.show())

        self.janela_estoque_inserir.btn_iserirDados.clicked.connect(self.inserir_dados)
        self.janela_estoque_inserir.closeEvent = self.destroi_janela_inserir
        self.janela_estoque_inserir.btn_fecharJanelaInserir.clicked.connect(lambda: self.fechar_janela_inserir())

        ### ABRIR E FECHAR JANELA ATUALIZAR ###
        self.janela_estoque.btn_abreJanelaAtualizar.clicked.connect(lambda: self.abrir_janela_atualizar_estoque())
        self.janela_estoque_atualizar.btn_sairJanelaAtualizar.clicked.connect(lambda: self.fechar_janela_atualizar())
        self.janela_estoque_atualizar.btn_atualizarDados.clicked.connect(lambda: self.atualizar_dados())
        self.janela_estoque_atualizar.closeEvent = self.destroi_janela_atualizar

        ### ABRIR E FECCHAR JANELA EXCLUIR ###
        self.janela_estoque.btn_excluirRegistro.clicked.connect(lambda: self.abrir_janela_excluir())
        self.janela_estoque_excluir.btn_sairJanelaExcluir.clicked.connect(lambda: self.janela_estoque_excluir.close())
        self.janela_estoque_excluir.btn_excluirDados.clicked.connect(lambda: 0)
        self.janela_estoque_excluir.closeEvent = self.destroi_janela_excluir

        ### BOTÃO EXCLUIR DADOS ###
        self.janela_estoque_excluir.btn_excluirDados.clicked.connect(lambda: self.excluir_dados())


    ### MÉTODOS/FUNCIONALIDADES###
    def starta_thread(self):
        threading.Thread(target=self.chama_mostrar_estoque).start()

    def chama_mostrar_estoque(self):
        global tabela_estoque
        time.sleep(1)
        self.mostrar_estoque_tela(tabela_estoque)

    def destroi_janela_inserir(self, *args):
        global tabela_estoque
        self.mostrar_estoque_tela(tabela_estoque)
        self.janela_estoque_inserir.close()

    def fechar_janela_inserir(self):
        self.starta_thread()
        self.janela_estoque_inserir.nomeProduto.setText("")
        self.janela_estoque_inserir.qtdProduto.setValue(1)
        self.janela_estoque_inserir.obsProduto.setText("")
        self.destroi_janela_inserir()

    def destroi_janela_atualizar(self, *args):
        global tabela_estoque
        self.lista_objetos_linedit = []
        self.dados_antigos_atualizar = []
        self.registros_com_id = []
        self.resultados_pesquisa = []
        self.mostrar_estoque_tela(tabela_estoque)
        self.janela_estoque_atualizar.close()

    def fechar_janela_atualizar(self):
        self.starta_thread()
        self.lista_objetos_linedit = []
        self.dados_antigos_atualizar = []
        self.resultados_pesquisa = []
        self.destroi_janela_atualizar()

    def fechar_janela_excluir(self):
            self.starta_thread()
            self.destroi_janela_excluir()

    def destroi_janela_excluir(self, *args):
        global tabela_estoque
        self.mostrar_estoque_tela(tabela_estoque)
        self.lista_dados_excluir = []
        self.janela_estoque_excluir.close()

    def pesquisar(self):
        global tabela_estoque
        pesquisa = self.janela_estoque.input_buscar.text()
        self.resultados_pesquisa = []
        if self.janela_estoque.radioNomeProduto.isChecked():
            nome_buscado = pesquisa.upper()
            for produto in tabela_estoque:
                if nome_buscado in produto[1].upper():
                    self.resultados_pesquisa.append(produto)
            self.janela_estoque.input_buscar.setText("")
            if self.resultados_pesquisa:
                self.mostrar_estoque_tela(self.resultados_pesquisa)
            else:
                QtWidgets.QMessageBox.about(self.janela_estoque,
             'Gerenciador de estoque', f'Produto "{nome_buscado}" não encontrado.')
            return
        if self.janela_estoque.radioQtdMaior.isChecked():
            nome_buscado = pesquisa.upper()
            try:
                int(nome_buscado)
            except ValueError:
                QtWidgets.QMessageBox.about(self.janela_estoque,
             'Gerenciador de estoque', f'Quantidade "{nome_buscado}" inválida. Insira apenas números para buscar por quantidade.')
                return
            for produto in tabela_estoque:
                if int(nome_buscado) <= produto[2]:
                    self.resultados_pesquisa.append(produto)
            self.janela_estoque.input_buscar.setText("")
            if self.resultados_pesquisa:
                self.mostrar_estoque_tela(self.resultados_pesquisa)
            else:
                QtWidgets.QMessageBox.about(self.janela_estoque,
             'Gerenciador de estoque', f'Produto com quantidade maior que "{nome_buscado}" não encontrado.')
            return
        if self.janela_estoque.radioQtdMenor.isChecked():
            nome_buscado = pesquisa.upper()
            try:
                int(nome_buscado)
            except ValueError:
                QtWidgets.QMessageBox.about(self.janela_estoque,
             'Gerenciador de estoque', f'Quantidade "{nome_buscado}" inválida. Insira apenas números para buscar por quantidade.')
                return
            for produto in tabela_estoque:
                if int(nome_buscado) >= produto[2]:
                    self.resultados_pesquisa.append(produto)
            self.janela_estoque.input_buscar.setText("")
            if self.resultados_pesquisa:
                self.mostrar_estoque_tela(self.resultados_pesquisa)
            else:
                QtWidgets.QMessageBox.about(self.janela_estoque,
             'Gerenciador de estoque', f'Produto com quantidade menor que "{nome_buscado}" não encontrado.')
            return
        if self.janela_estoque.radioTodosRegistros.isChecked():
            self.resultados_pesquisa = []
            self.janela_estoque.input_buscar.setText("")
            self.mostrar_estoque_tela(tabela_estoque)
            return


    def excluir_dados(self):
        dados_delete = []
        for i in self.lista_dados_excluir:
            lista_aux = []
            for j in i:
                lista_aux.append(j)
            dados_delete.append(tuple(lista_aux))
        self.lista_dados_excluir = []
        print(dados_delete)
  
        ## Load spinner aqui
        excluir = db.Estoque()
        for i in range(len(dados_delete)):
            retorno = excluir.excluir_produto(dados_delete[i][0], dados_delete[i][1],
            dados_delete[i][2])
            if retorno == "Erro":
                QtWidgets.QMessageBox.about(self.janela_estoque_excluir,
             'Gerenciador de estoque', 'Ocorreu um erro ao excluir os dados.')
                self.fechar_janela_excluir()

        ## Fim load spinner aqui
        threading.Thread(target=carrega_tabela_estoque).start()
        QtWidgets.QMessageBox.about(self.janela_estoque_excluir,
             'Gerenciador de estoque', 'Dados Excluidos com Sucesso!')

        self.fechar_janela_excluir()

    def abrir_janela_excluir(self):
        dados = set(index.row() for index in self.janela_estoque.tableWidget.selectedIndexes())
        if len(dados) < 1:
            QtWidgets.QMessageBox.about(self.janela_estoque,
             'Gerenciador de estoque', 'Para Excluir um produto é necessario selecionar ao menos 1 registro.')
            return
        lista_de_dados = []
        for i in dados:
            lista_de_dados.append((self.janela_estoque.tableWidget.item(i, 0).text(),self.janela_estoque.tableWidget.item(i, 1).text(),
            self.janela_estoque.tableWidget.item(i, 2).text()))


        self.janela_estoque_excluir.tabelaExcluir.setRowCount(len(lista_de_dados))
        self.janela_estoque_excluir.tabelaExcluir.setColumnCount(len(lista_de_dados[0]))
        self.janela_estoque_excluir.tabelaExcluir.setHorizontalHeaderLabels(["Produto", "Quantidade", "Observação"])
        
        
        for i in range(len(lista_de_dados)): #linha
            for j in range(len(lista_de_dados[0])): #coluna
                item = QtWidgets.QTableWidgetItem(f"{lista_de_dados[i][j]}")
                self.janela_estoque_excluir.tabelaExcluir.setItem(i,j, item)
        self.lista_dados_excluir = lista_de_dados

        header = self.janela_estoque_excluir.tabelaExcluir.horizontalHeader()           # Colunas abaixo  
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.janela_estoque_excluir.show()

    def inserir_dados(self):
        ### PEGANDO OS DADOS DOS CAMPOS DE ENTRADA ###
        produto = self.janela_estoque_inserir.nomeProduto.text()
        qtd = self.janela_estoque_inserir.qtdProduto.text()
        observacao = self.janela_estoque_inserir.obsProduto.text()


        global tabela_estoque
        ##verificação do nome do produto##
        try:
            validacoes.valida_campo_vazio(produto)
            validacoes.valida_nome_produto(produto)
        except erros.CaractereInvalido:
            QtWidgets.QMessageBox.about(self.janela_estoque_inserir,
                'Gerenciador de alunos', 'Caractere inválido usado no nome do produto. Por favor use apenas\n\
                    letras maiusculas, minusculas e acentuação simples.')
            return
        except erros.CampoVazio:
            QtWidgets.QMessageBox.about(self.janela_estoque_inserir,
                'Gerenciador de alunos', 'Digite um nome antes de inserir.')
            return
        except erros.NomeCurto:
            QtWidgets.QMessageBox.about(self.janela_estoque_inserir,
                'Gerenciador de alunos', 'O nome precisa ter no mínimo 3 caracteres.')
            return
        if not observacao:
            observacao = "Nenhuma"

        inserir = db.Estoque()
        inserir.inserir_estoque(produto, qtd, observacao)
        threading.Thread(target=carrega_tabela_estoque).start()

        self.starta_thread()
        QtWidgets.QMessageBox.about(self.janela_estoque_inserir,
                'Sucesso!', "Produto inserido com sucesso!")
        self.janela_estoque_inserir.nomeProduto.setText("")
        self.janela_estoque_inserir.qtdProduto.setValue(1)
        self.janela_estoque_inserir.obsProduto.setText("")

    def abrir_janela_atualizar_estoque(self):
        global tabela_estoque
        dados = set(index.row() for index in self.janela_estoque.tableWidget.selectedIndexes())
        if len(dados) < 1:
            QtWidgets.QMessageBox.about(self.janela_estoque,
             'Gerenciador de estoque', 'Para atualizar, é necessario selecionar ao menos 1 registro.')
            return
        print(tabela_estoque)
        print(dados)
        
        
        lista_de_dados = []
        self.registros_com_id = []
        if len(self.resultados_pesquisa) > 0:
            for i in dados:
                self.registros_com_id.append(self.resultados_pesquisa[i])
        else:
            for i in dados:
                self.registros_com_id.append(tabela_estoque[i])
        self.resultados_pesquisa = []

        for i, j in enumerate(self.registros_com_id):
            self.registros_com_id[i] = tuple(j)
        print(self.registros_com_id)

        lista_de_dados = []
        for i in dados:
            lista_de_dados.append((self.janela_estoque.tableWidget.item(i, 0).text(),self.janela_estoque.tableWidget.item(i, 1).text(),
            self.janela_estoque.tableWidget.item(i, 2).text()))


        self.janela_estoque_atualizar.tabelaAtualizar.setRowCount(len(lista_de_dados))
        self.janela_estoque_atualizar.tabelaAtualizar.setColumnCount(len(lista_de_dados[0]))
        self.janela_estoque_atualizar.tabelaAtualizar.setHorizontalHeaderLabels(["Produto", "Quantidade", "Observação"])
        self.dados_antigos_atualizar = lista_de_dados
        
        self.lista_objetos_linedit = []
        style = "QLineEdit{font-size: 14px;\
                text-align: center;\
                color: white;\
                }"
        for i in range(len(lista_de_dados)): #linha
            for j in range(len(lista_de_dados[0])): #coluna
                item = None
                lista_temp = []
                if j == 0:
                    inputnormal = QLineEdit(self.janela_estoque.tableWidget)
                    inputnormal.setStyleSheet(style)
                    item = inputnormal.setText(str(lista_de_dados[i][j]))
                    inputnormal.setMaxLength(60)
                    lista_temp.append(inputnormal)
                    self.janela_estoque_atualizar.tabelaAtualizar.setCellWidget(i, j, inputnormal) 
                if j == 1:
                    inputidade = QLineEdit(self.janela_estoque.tableWidget)
                    inputidade.setStyleSheet(style)
                    inputidade.setText(str(lista_de_dados[i][j]))
                    inputidade.setInputMask("999")
                    lista_temp.append(inputidade)
                    self.janela_estoque_atualizar.tabelaAtualizar.setCellWidget(i, j, inputidade) 
                if j == 2:
                    inputcpf = QLineEdit(self.janela_estoque.tableWidget)
                    inputcpf.setStyleSheet(style)
                    item = inputcpf.setText(str(lista_de_dados[i][j]))
                    inputcpf.setMaxLength(60)
                    lista_temp.append(inputcpf)
                    self.janela_estoque_atualizar.tabelaAtualizar.setCellWidget(i, j, inputcpf)
                
                self.lista_objetos_linedit.append(lista_temp)
                
                
        self.janela_estoque_atualizar.show()


    def atualizar_dados(self):
        global tabela_estoque
        print(tabela_estoque)
       
        dados_update = []
        update = False
        lista_aux = []
        lista_aux2 = []
        lista_objetos = []

        self.lista_objetos_linedit = [item[0].text() for item in self.lista_objetos_linedit]
        lista = []
        lista_oficial = []
        i = 0
        for item in self.lista_objetos_linedit:
            lista.append(item)
            if i != 2:
                i += 1
            else:
                lista.insert(0, 0)
                lista_oficial.append(tuple(lista))
                lista = []
                i = 0
        
        self.lista_objetos_linedit = lista_oficial
        

        #print(self.lista_objetos_linedit)
        #print(self.registros_com_id)###Terminar essas coisas aqui. A questão de pegar a lista sem id e a com id, e mandar pro banco só a que tem o id

        dados_antigos = []
        cont = 0
        for j, registros_com_id in enumerate(self.registros_com_id):
            for i in range(len(registros_com_id)):
                if i == 0: continue
                if str(registros_com_id[i]) != self.lista_objetos_linedit[j][i]:
                    # print(type(registros_com_id[i]) , type(self.lista_objetos_linedit[j][i]))
                    # print(registros_com_id[i] , self.lista_objetos_linedit[j][i])
                    update = True
                lista_aux.append(self.lista_objetos_linedit[j][i])  
                lista_aux2.append(registros_com_id[i])
                if update and cont == 2:
                    lista_aux.insert(0, registros_com_id[0])
                    lista_aux2.insert(0, registros_com_id[0])
                    dados_update.append(tuple(lista_aux))
                    dados_antigos.append(tuple(lista_aux2))
                    cont = -1
                    update = False
                    lista_aux = []
                    lista_aux2 = []
                elif not update and cont == 2:
                    lista_aux = []
                    lista_aux2 = []
                    cont = -1
                cont += 1

        ###Aqui comecaria um load spinner
        print(dados_update)
        if dados_update:
            atualizar = db.Estoque()

            for dado in dados_update:
                resposta = atualizar.atualizar_estoque(id_produto=dado[0], produto=dado[1], qtd=dado[2], observacao=dado[3])
                if resposta == "Erro":
                    QtWidgets.QMessageBox.about(self.janela_estoque_atualizar,
                    'Gerenciador de estoque', 'Ocorreu um erro ao atualizar os dados.')
                    self.destroi_janela_atualizar()
                    return

        
        threading.Thread(target=carrega_tabela_estoque).start()
        QtWidgets.QMessageBox.about(self.janela_estoque_atualizar,
        'Gerenciador de estoque', 'Dados atualizados com Sucesso!')
        self.registros_com_id = []
        self.lista_objetos_linedit = []
        self.dados_antigos_atualizar = []
        self.fechar_janela_atualizar()


    def abrir_janela(self, tabela):
        ## erro caso o usuario tente acessar os dados antes das tabelas carregarem ##
        if tabela == [()]:
            QtWidgets.QMessageBox.about(self.janela_estoque,
             'Gerenciador de alunos', 'Ocorreu um erro ao acessar o banco de dados,\nVerifique sua conexão.')
            return

        self.janela_estoque.show()
        self.mostrar_estoque_tela(tabela)



    def mostrar_estoque_tela(self, tabela):
        self.janela_estoque.tableWidget.setRowCount(len(tabela))
        self.janela_estoque.tableWidget.setColumnCount(len(tabela[0])-1)
        self.janela_estoque.tableWidget.setHorizontalHeaderLabels(["Produto", "Quantidade", "Observação"])
        self.janela_estoque.tableWidget.resizeRowsToContents()
        for i in range(len(tabela)): #linha
            for j in range(len(tabela[0])): #coluna
                if j == 3: break
                item = QtWidgets.QTableWidgetItem(f"{tabela[i][j+1]}")

                self.janela_estoque.tableWidget.setItem(i,j, item)
        ## Reajustando o tamnho das células(colunoas) de acordo com o contúdo delas
        header = self.janela_estoque.tableWidget.horizontalHeader()           # Colunas abaixo  
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)


class JanelaDespesas(QMainWindow):
    def __init__(self):
        super().__init__()

        ### CARREGANDO TELAS QUE SERÃO USADAS ###
        self.janela_despesas = uic.loadUi('src\\telas\\telas_despesas\\tela_despesas.ui')
        self.janela_despesas_inserir = uic.loadUi('src\\telas\\telas_despesas\\inserir_despesa.ui')
        self.janela_despesas_atualizar = uic.loadUi('src\\telas\\telas_despesas\\atualizar_despesas.ui')
        self.janela_despesas_excluir = uic.loadUi('src\\telas\\telas_despesas\\excluir_despesas.ui')
        self.janela_despesas_inserir.dateEdit.setStyleSheet(ESTILO_DATA2)

        ### FECHAR A JANELA ###
        self.janela_despesas.btn_fechar.clicked.connect(lambda: self.janela_despesas.close())

        ### PESQUISAR ###
        self.janela_despesas.btn_pesquisar.clicked.connect(self.pesquisar)
        self.janela_despesas.input_buscar.returnPressed.connect(self.pesquisar)
        self.janela_despesas.radioDespesasVencidas.toggled.connect(lambda: self.radio_signals_vencidas())
        self.janela_despesas.radioDespesasNaoVencidas.toggled.connect(lambda: self.radio_signals_nao_vencidas())
        self.resultados_pesquisa = []
        
        ### ABRIR E FECHAR JANELA INSERIR ###
        self.janela_despesas.btn_abreJanelaInserir.clicked.connect(lambda: self.janela_despesas_inserir.show())
        self.janela_despesas_inserir.btn_fecharJanelaInserir.clicked.connect(lambda: self.fechar_janela_inserir())
        self.janela_despesas_inserir.btn_iserirDados.clicked.connect(lambda: self.inserir_dados())
        self.janela_despesas_inserir.closeEvent = self.fechar_janela_inserir

        ### ABRIR E FECHAR JANELA ATUALIZAR ###
        self.janela_despesas.btn_abreJanelaAtualizar.clicked.connect(lambda: self.abrir_janela_atualizar())
        self.janela_despesas_atualizar.btn_sairJanelaAtualizar.clicked.connect(lambda: self.fechar_janela_atualizar())
        self.janela_despesas_atualizar.btn_atualizarDados.clicked.connect(lambda: self.atualizar_dados())
        self.janela_despesas_atualizar.closeEvent = self.fechar_janela_atualizar

        ### ABRIR E FECHAR JANELA EXCLUIR ###
        self.janela_despesas.btn_excluirRegistro.clicked.connect(lambda: self.abrir_janela_excluir())
        self.janela_despesas_excluir.btn_sairJanelaExcluir.clicked.connect(lambda: self.fechar_janela_excluir())
        self.janela_despesas_excluir.closeEvent = self.fechar_janela_excluir

        ### BOTÃO EXCLUIR DADOS ###
        self.janela_despesas_excluir.btn_excluirDados.clicked.connect(lambda: self.excluir_registro())


    ### MÉTODOS/FUNCIONALIDADES###
    def starta_thread(self):
        threading.Thread(target=self.chama_mostrar_despesas).start()

    def chama_mostrar_despesas(self):
        global tabela_despesas
        time.sleep(1)
        self.mostrar_despesa_tela(tabela_despesas)

    def destroi_janela_inserir(self, *args):
        global tabela_despesas
        self.mostrar_despesa_tela(tabela_despesas)
        self.janela_despesas_inserir.close()

    def fechar_janela_inserir(self, *args):
        threading.Thread(target=carrega_tabela_despesa).start()
        self.starta_thread()
        self.janela_despesas_inserir.nomeProduto.setText("")
        self.janela_despesas_inserir.qtdProduto.setValue(1)
        self.janela_despesas_inserir.obsProduto.setText("")
        self.destroi_janela_inserir()

    def destroi_janela_atualizar(self, *args):
        global tabela_despesas
        self.lista_objetos_linedit = []
        self.dados_antigos_atualizar = []
        self.registros_com_id = []
        self.resultados_pesquisa = []
        self.mostrar_despesa_tela(tabela_despesas)
        self.janela_despesas_atualizar.close()

    def fechar_janela_atualizar(self, *args):
        threading.Thread(target=carrega_tabela_despesa).start()
        self.starta_thread()
        self.lista_objetos_linedit = []
        self.dados_antigos_atualizar = []
        self.resultados_pesquisa = []
        self.destroi_janela_atualizar()

    def fechar_janela_excluir(self, *args):
        threading.Thread(target=carrega_tabela_despesa).start()
        self.starta_thread()
        self.destroi_janela_excluir()

    def destroi_janela_excluir(self, *args):
        global tabela_despesas
        self.mostrar_despesa_tela(tabela_despesas)
        self.lista_dados_excluir = []
        self.janela_despesas_excluir.close()

    def radio_signals_vencidas(self):
        if self.janela_despesas.radioDespesasVencidas.isChecked() == True:
            self.janela_despesas.input_buscar.setEnabled(False)
            self.janela_despesas.input_buscar.setStyleSheet(DISABLED_INPUT)
        else:
            self.janela_despesas.input_buscar.setEnabled(True)
            self.janela_despesas.input_buscar.setStyleSheet(ENABLED_INPUT)

    def radio_signals_nao_vencidas(self):
        if self.janela_despesas.radioDespesasNaoVencidas.isChecked() == True:
            self.janela_despesas.input_buscar.setEnabled(False)
            self.janela_despesas.input_buscar.setStyleSheet(DISABLED_INPUT)
        else:
            self.janela_despesas.input_buscar.setEnabled(True)
            self.janela_despesas.input_buscar.setStyleSheet(ENABLED_INPUT)

    def pesquisar(self):
        global tabela_despesas
        pesquisa = self.janela_despesas.input_buscar.text()
        self.resultados_pesquisa = []
        if self.janela_despesas.radioNomeDespesa.isChecked():
            nome_buscado = pesquisa.upper()
            for produto in tabela_despesas:
                if nome_buscado in produto[1].upper():
                    self.resultados_pesquisa.append(produto)
            self.janela_despesas.input_buscar.setText("")
            if self.resultados_pesquisa:
                self.mostrar_despesa_tela(self.resultados_pesquisa)
            else:
                QtWidgets.QMessageBox.about(self.janela_despesas,
             'Gerenciador de despesas', f'Produto "{nome_buscado}" não encontrado.')
            return
        if self.janela_despesas.radioMaiorQue.isChecked():
            try:
                nome_buscado = int(pesquisa)
            except ValueError:
                QtWidgets.QMessageBox.about(self.janela_despesas,
             'Gerenciador de despesas', f'Valor: "{pesquisa}" inválido. Insira apenas números ')
                return
                
            for produto in tabela_despesas:
                if nome_buscado <= produto[2]:
                    self.resultados_pesquisa.append(produto)
            self.janela_despesas.input_buscar.setText("")
            if self.resultados_pesquisa:
                self.mostrar_despesa_tela(self.resultados_pesquisa)
            else:
                QtWidgets.QMessageBox.about(self.janela_despesas,
             'Gerenciador de despesas', f'Despesa com valor maior que "{nome_buscado}" não encontrado.')
            return
        if self.janela_despesas.radioMenorQue.isChecked():
            try:
                nome_buscado = int(pesquisa)
            except ValueError:
                QtWidgets.QMessageBox.about(self.janela_despesas,
             'Gerenciador de despesas', f'Valor: "{pesquisa}" inválido. Insira apenas números ')
                return
            for produto in tabela_despesas:
                if nome_buscado >= produto[2]:
                    self.resultados_pesquisa.append(produto)
            self.janela_despesas.input_buscar.setText("")
            if self.resultados_pesquisa:
                self.mostrar_despesa_tela(self.resultados_pesquisa)
            else:
                QtWidgets.QMessageBox.about(self.janela_despesas,
             'Gerenciador de despesas', f'Despesa com valor menor que "{nome_buscado}" não encontrado.')
            return
        if self.janela_despesas.radioDespesasVencidas.isChecked():
            hoje = formato_iso_para_br((str(dt.datetime.now().date())))
            for produto in tabela_despesas:
                try:
                    esta_vencida = compara_datas(hoje, formato_iso_para_br(produto[3]))
                    if esta_vencida:
                        self.resultados_pesquisa.append(produto)
                    else:
                        pass
                except Exception as err:
                    pass
            if self.resultados_pesquisa:
                self.mostrar_despesa_tela(self.resultados_pesquisa)
            else:
                QtWidgets.QMessageBox.about(self.janela_despesas,
             'Gerenciador de despesas', f'Não há nenhum produto com a data de pagamento vencida.')
            return

        if self.janela_despesas.radioDespesasNaoVencidas.isChecked():
            hoje = formato_iso_para_br((str(dt.datetime.now().date())))
            for produto in tabela_despesas:
                try:
                    nao_esta_vencida = compara_datas2(hoje, formato_iso_para_br(produto[3]))
                    print(nao_esta_vencida)
                    if nao_esta_vencida:
                        self.resultados_pesquisa.append(produto)
                    else:
                        pass
                except Exception as err:
                    pass
            if self.resultados_pesquisa:
                self.mostrar_despesa_tela(self.resultados_pesquisa)
            else:
                QtWidgets.QMessageBox.about(self.janela_despesas,
             'Gerenciador de despesas', f'Não existe registros de datas de pagamentos não vencidas.')
            return
        if self.janela_despesas.radioObservacao.isChecked():
            nome_buscado = pesquisa.upper()
            for produto in tabela_despesas:
                if nome_buscado in produto[4].upper():
                    self.resultados_pesquisa.append(produto)
            self.janela_despesas.input_buscar.setText("")
            if self.resultados_pesquisa:
                self.mostrar_despesa_tela(self.resultados_pesquisa)
            else:
                QtWidgets.QMessageBox.about(self.janela_despesas,
             'Gerenciador de despesas', f'Produto com observação "{nome_buscado}" não encontrado.')
            return
        if self.janela_despesas.radioTodosRegistros.isChecked():
            self.resultados_pesquisa = []
            self.mostrar_despesa_tela(tabela_despesas)
            return
        
    def excluir_registro(self):
        dados_delete = []
        for i in self.lista_dados_excluir:
            lista_aux = []
            for j in i:
                lista_aux.append(j)
            dados_delete.append(tuple(lista_aux))
        self.lista_dados_excluir = []
        print(dados_delete)
  
        ## Load spinner aqui
        print(dados_delete)
        

        excluir = db.Despesa()
        for i in range(len(dados_delete)):
            try: 
                data = dt.datetime.strptime(str(dados_delete[i][2]), '%d/%m/%Y')
                data = dt.datetime.strftime(data, format="%Y-%m-%d")
            except:
                data = str(dados_delete[i][2])
            retorno = excluir.excluir_despesa(dados_delete[i][0], dados_delete[i][1],
            data, dados_delete[i][3])

            if retorno == "Erro":
                QtWidgets.QMessageBox.about(self.janela_despesas_excluir,
             'Gerenciador de despesas', 'Ocorreu um erro ao excluir os dados.')
                self.fechar_janela_excluir()
                return

        ## Fim load spinner aqui
        threading.Thread(target=carrega_tabela_despesa).start()
        QtWidgets.QMessageBox.about(self.janela_despesas_excluir,
             'Gerenciador de despesas', 'Dados Excluidos com Sucesso!')

        self.fechar_janela_excluir()

    def inserir_dados(self):
        ### PEGANDO OS DADOS DOS CAMPOS DE ENTRADA ###
        despesa = self.janela_despesas_inserir.nomeProduto.text()
        valor = self.janela_despesas_inserir.qtdProduto.text()
        data_pagamento = dt.datetime.strftime(self.janela_despesas_inserir.dateEdit.date().toPyDate(), format="%Y-%m-%d")
        data_pagamento = formato_br_para_iso(data_pagamento)
        observacao = self.janela_despesas_inserir.obsProduto.text()


        ##verificação do nome do produto##
        try:
            validacoes.valida_campo_vazio(despesa)
            validacoes.valida_nome_produto(despesa)
        except erros.CaractereInvalido:
            QtWidgets.QMessageBox.about(self.janela_despesas_inserir,
                'Gerenciador de despesas', 'Caractere inválido usado no nome da despesa. Por favor use apenas\n\
                    letras maiusculas, minusculas e acentuação simples.')
            return
        except erros.CampoVazio:
            QtWidgets.QMessageBox.about(self.janela_despesas_inserir,
                'Gerenciador de despesas', 'Digite um nome de despesa antes de inserir.')
            return
        except erros.NomeCurto:
            QtWidgets.QMessageBox.about(self.janela_despesas_inserir,
                'Gerenciador de despesas', 'O nome da despesa precisa ter no mínimo 3 caracteres.')
            return
        if not observacao:
            observacao = "Nenhuma"

        inserir = db.Despesa()
        inserir.inserir_despesa(despesa, valor, data_pagamento, observacao)
        threading.Thread(target=carrega_tabela_despesa).start()

        self.starta_thread()
        QtWidgets.QMessageBox.about(self.janela_despesas_inserir,
                'Sucesso!', "Despesa inserido com sucesso!")
        self.janela_despesas_inserir.nomeProduto.setText("")
        self.janela_despesas_inserir.qtdProduto.setValue(1)
        data = dt.datetime.strptime(str("01/01/2021"), '%d/%m/%Y')
        self.janela_despesas_inserir.dateEdit.setDate(data)
        self.janela_despesas_inserir.obsProduto.setText("")

    def atualizar_dados(self):    
        dados_update = []
        update = False
        lista_aux = []
        lista_aux2 = []
        lista_objetos = []


        for item in self.lista_objetos_linedit:
            if isinstance(item[0], QtWidgets.QLineEdit):
                lista_objetos.append(item[0].text())
            if isinstance(item[0], QtWidgets.QDateEdit):
                lista_objetos.append(dt.datetime.strftime(item[0].date().toPyDate(), format="%Y-%m-%d"))
        self.lista_objetos_linedit = lista_objetos
        #print(self.lista_objetos_linedit)
        #self.lista_objetos_linedit = [item[0].text() for item in self.lista_objetos_linedit]
        lista = []
        lista_oficial = []
        i = 0
        for item in self.lista_objetos_linedit:
            lista.append(item)
            if i != 3:
                i += 1
            else:
                lista.insert(0, 0)
                lista_oficial.append(tuple(lista))
                lista = []
                i = 0
        
        self.lista_objetos_linedit = lista_oficial
        

        #print(self.lista_objetos_linedit)
        #print(self.registros_com_id)###Terminar essas coisas aqui. A questão de pegar a lista sem id e a com id, e mandar pro banco só a que tem o id

        dados_antigos = []
        cont = 0
        for j, registros_com_id in enumerate(self.registros_com_id):
            for i in range(len(registros_com_id)):
                if i == 0: continue
                if str(registros_com_id[i]) != str(self.lista_objetos_linedit[j][i]):
                    print(type(registros_com_id[i]) , type(self.lista_objetos_linedit[j][i]))
                    print(registros_com_id[i] , self.lista_objetos_linedit[j][i])
                    update = True
                lista_aux.append(self.lista_objetos_linedit[j][i])  
                lista_aux2.append(registros_com_id[i])
                if update and cont == 3:
                    lista_aux.insert(0, registros_com_id[0])
                    lista_aux2.insert(0, registros_com_id[0])
                    dados_update.append(tuple(lista_aux))
                    dados_antigos.append(tuple(lista_aux2))
                    cont = -1
                    update = False
                    lista_aux = []
                    lista_aux2 = []
                elif not update and cont == 3:
                    lista_aux = []
                    lista_aux2 = []
                    cont = -1
                cont += 1

        ###Aqui comecaria um load spinner
        print(dados_update)
        dados_update2 = []
        for i in range(len(dados_update)):
            data_inicio = dados_update[i][3]
            data_min_permitida = dt.datetime.strptime("2021-01-01", "%Y-%m-%d")
            data_max_permitida = dt.datetime.strptime("2050-01-01", "%Y-%m-%d")
            data_inicio = dt.datetime.strptime(data_inicio, "%Y-%m-%d")
            if not (data_min_permitida <= data_inicio <= data_max_permitida):
                QtWidgets.QMessageBox.about(self.janela_despesas_atualizar,
             'Gerenciador de despesas', f'Erro ao atualizar data de pagamento, por favor insira uma data de no\
             minimo 2021 e no máximo 2040')
                self.abrir_janela_atualizar()
                return
            dados_update2.append(list(dados_update[i]))

        for i in range(len(dados_update2)):
            try:
                validacoes.valida_campo_vazio(str(dados_update2[i][1]))
                validacoes.valida_nome_produto(str(dados_update2[i][1]))
            except erros.CaractereInvalido:
                QtWidgets.QMessageBox.about(self.janela_despesas_inserir,
                    'Gerenciador de despesas', f'Caractere inválido usado no nome da despesa da linha "{i+1}". Por favor use apenas'+
            'letras maiusculas, minusculas e acentuação simples.')
                self.abrir_janela_atualizar()
                return
            except erros.CampoVazio:
                QtWidgets.QMessageBox.about(self.janela_despesas_inserir,
                    'Gerenciador de despesas', f'Digite um nome de despesa na linha "{i+1}" antes de atualizar os dados.')
                self.abrir_janela_atualizar()
                return
            except erros.NomeCurto:
                QtWidgets.QMessageBox.about(self.janela_despesas_inserir,
                    'Gerenciador de despesas', f'O nome da despesa na linha "{i+1}" precisa ter no mínimo 3 caracteres.')
                self.abrir_janela_atualizar()
                return
            try:
                validacoes.valida_campo_vazio(dados_update2[i][4])
            except erros.CampoVazio:
                dados_update2[i][4] = "Nenhuma"
            if not dados_update2[i][2]:
                dados_update2[i][2] = "0"
            
        print(dados_update2)
        ### LOAD SPINNER ###
        if dados_update2:
            atualizar = db.Despesa()
            for dado in dados_update2:
                retorno = atualizar.atualizar_despesa(dado[0], dado[1], dado[2], dado[3], dado[4])
                if retorno == "Erro":
                    QtWidgets.QMessageBox.about(self.janela_despesas_atualizar,
                'Gerenciador de despesas', 'Ocorreu um erro ao atualizar a despesa.')
                    self.destroi_janela_atualizar()
                    return
        threading.Thread(target=carrega_tabela_despesa).start()
        ### FIM LOAD SPINNER ###
        QtWidgets.QMessageBox.about(self.janela_despesas_atualizar,
             'Gerenciador de despesas', 'Dados atualizados com Sucesso!')
        self.registros_com_id = []
        self.lista_objetos_linedit = []
        self.dados_antigos_atualizar = []
        self.fechar_janela_atualizar()


    def abrir_janela(self, tabela):
        ## erro caso o usuario tente acessar os dados antes das tabelas carregarem ##
        if tabela == [()]:
            QtWidgets.QMessageBox.about(self.janela_despesas,
             'Gerenciador de alunos', 'Ocorreu um erro ao acessar o banco de dados,\nVerifique sua conexão.')
            return

        self.janela_despesas.show()
        self.mostrar_despesa_tela(tabela)

    def mostrar_despesa_tela(self, tabela): 
        self.janela_despesas.tableWidget.setRowCount(len(tabela))
        self.janela_despesas.tableWidget.setColumnCount(len(tabela[0])-1)
        self.janela_despesas.tableWidget.setHorizontalHeaderLabels(["Nome despesa", "Valor despesa",
         "Data pagamento", "Observação"])
        self.janela_despesas.tableWidget.resizeRowsToContents()
        for i in range(len(tabela)): #linha
            for j in range(len(tabela[0])): #coluna
                if j == 4: break

                if j+1 == 3:
                    item = QtWidgets.QTableWidgetItem(f"{formato_iso_para_br(tabela[i][j+1])}")
                else:
                    item = QtWidgets.QTableWidgetItem(f"{tabela[i][j+1]}")

                self.janela_despesas.tableWidget.setItem(i,j, item)
        ## Reajustando o tamnho das células(colunoas) de acordo com o contúdo delas
        header = self.janela_despesas.tableWidget.horizontalHeader()           # Colunas abaixo  
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

    def abrir_janela_atualizar(self):
        global tabela_despesas
        dados = set(index.row() for index in self.janela_despesas.tableWidget.selectedIndexes())
        if len(dados) < 1:
            QtWidgets.QMessageBox.about(self.janela_despesas,
             'Gerenciador de despesas', 'Para atualizar, é necessario selecionar ao menos 1 registro.')
            return
        
        lista_de_dados = []
        self.registros_com_id = []
        if len(self.resultados_pesquisa) > 0:
            for i in dados:
                self.registros_com_id.append(self.resultados_pesquisa[i])
        else:
            for i in dados:
                self.registros_com_id.append(tabela_despesas[i])
        self.resultados_pesquisa = []

        for i, j in enumerate(self.registros_com_id):
            self.registros_com_id[i] = tuple(j)

        lista_de_dados = []
        for i in dados:
            lista_de_dados.append((self.janela_despesas.tableWidget.item(i, 0).text(),self.janela_despesas.tableWidget.item(i, 1).text(),
            self.janela_despesas.tableWidget.item(i, 2).text(), self.janela_despesas.tableWidget.item(i, 3).text()))


        self.janela_despesas_atualizar.tabelaAtualizar.setRowCount(len(lista_de_dados))
        self.janela_despesas_atualizar.tabelaAtualizar.setColumnCount(len(lista_de_dados[0]))
        self.janela_despesas_atualizar.tabelaAtualizar.setHorizontalHeaderLabels(["Nome despesa", "Valor", "Data de pagamento", "Observação"])
        self.dados_antigos_atualizar = lista_de_dados
        print(lista_de_dados)
        self.lista_objetos_linedit = []
        style = ESTILO_LINEEDIT
        style2 = ESTILO_DATA
        for i in range(len(lista_de_dados)): #linha
            for j in range(len(lista_de_dados[0])): #coluna
                item = None
                lista_temp = []
                if j == 0:
                    inputnormal = QLineEdit(self.janela_despesas.tableWidget)
                    inputnormal.setStyleSheet(style)
                    item = inputnormal.setText(str(lista_de_dados[i][j]))
                    inputnormal.setMaxLength(60)
                    lista_temp.append(inputnormal)
                    self.janela_despesas_atualizar.tabelaAtualizar.setCellWidget(i, j, inputnormal) 
                if j == 1:
                    inputidade = QLineEdit(self.janela_despesas.tableWidget)
                    inputidade.setStyleSheet(style)
                    inputidade.setText(str(lista_de_dados[i][j]))
                    inputidade.setInputMask("999999")
                    lista_temp.append(inputidade)
                    self.janela_despesas_atualizar.tabelaAtualizar.setCellWidget(i, j, inputidade) 

                if j == 2:
                    try:
                        inputnormal = QDateEdit(self.janela_despesas_atualizar.tabelaAtualizar,calendarPopup=True)
                        inputnormal.setStyleSheet(style2)
                        date = None
                        date = dt.datetime.strptime(str(lista_de_dados[i][j]), '%d/%m/%Y')
                        inputnormal.setDateTime(date)
                    except:
                        date = dt.datetime.strptime("01/01/2000", '%d/%m/%Y')
                        inputnormal.setDateTime(date) #QtCore.QDateTime.currentDateTime() <- pega data atual
                    finally:
                        lista_temp.append(inputnormal)
                        self.janela_despesas_atualizar.tabelaAtualizar.setCellWidget(i, j, inputnormal) 
                if j == 3:
                    inputcpf = QLineEdit(self.janela_despesas.tableWidget)
                    inputcpf.setStyleSheet(style)
                    item = inputcpf.setText(str(lista_de_dados[i][j]))
                    inputcpf.setMaxLength(60)
                    lista_temp.append(inputcpf)
                    self.janela_despesas_atualizar.tabelaAtualizar.setCellWidget(i, j, inputcpf)
                
                self.lista_objetos_linedit.append(lista_temp)
                
                
        self.janela_despesas_atualizar.show()

    def abrir_janela_excluir(self):
        dados = set(index.row() for index in self.janela_despesas.tableWidget.selectedIndexes())
        if len(dados) < 1:
            QtWidgets.QMessageBox.about(self.janela_despesas,
             'Gerenciador de estoque', 'Para Excluir uma despesa é necessario selecionar ao menos 1 registro.')
            return
        lista_de_dados = []

        for i in dados:
            lista_de_dados.append((self.janela_despesas.tableWidget.item(i, 0).text(),self.janela_despesas.tableWidget.item(i, 1).text(),
            self.janela_despesas.tableWidget.item(i, 2).text(), self.janela_despesas.tableWidget.item(i, 3).text()))


        self.janela_despesas_excluir.tabelaExcluir.setRowCount(len(lista_de_dados))
        self.janela_despesas_excluir.tabelaExcluir.setColumnCount(len(lista_de_dados[0]))
        self.janela_despesas_excluir.tabelaExcluir.setHorizontalHeaderLabels(["Nome despesa", "Valor", "Data de pagamento", "Observação"])
        
        
        for i in range(len(lista_de_dados)): #linha
            for j in range(len(lista_de_dados[0])): #coluna
                item = QtWidgets.QTableWidgetItem(f"{lista_de_dados[i][j]}")
                self.janela_despesas_excluir.tabelaExcluir.setItem(i,j, item)
        self.lista_dados_excluir = lista_de_dados

        header = self.janela_despesas_excluir.tabelaExcluir.horizontalHeader()           # Colunas abaixo  
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

        self.janela_despesas_excluir.show()


## FUNÇÕES ##
def carrega_tabela_alunos():
    ### CARREGANDO TABELA DOS ALUNOS ###
    global tabela_alunos
    selectAll = db.DadosAlunos()
    tabela = selectAll.retornaDadosDosAlunos()
    tabela_alunos = tabela


def carrega_tabela_avfisica():
    ### CARREGANDO TABELA DAS AV. FISICAS ###
    global tabela_avfisica
    selectAll = db.AvFisica()
    tabela = selectAll.retornaDadosAvFisicas()
    tabela_avfisica = tabela


def carrega_tabela_matricula():
    ### CARREGANDO TABELA DAS MATRICULAS  ###
    global tabela_matriculas
    selectAll = db.Matricula()
    tabela = selectAll.retornaDadosMatriculas()
    tabela_matriculas = tabela


def carrega_tabela_estoque():
    ### CARREGANDO TABELA DAS MATRICULAS  ###
    global tabela_estoque
    selectAll = db.Estoque()
    tabela = selectAll.retornaDadosEstoque()
    tabela_estoque = tabela


def carrega_tabela_despesa():
    ### CARREGANDO TABELA DAS MATRICULAS  ###
    global tabela_despesas
    selectAll = db.Despesa()
    tabela = selectAll.retornaDadosDespesas()
    tabela_despesas = tabela


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_screen = JanelaPrincipal()
    app.exec()
