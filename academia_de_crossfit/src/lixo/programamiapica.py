import sys
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QColor, QIcon, QKeyEvent, QPixmap, QRegExpValidator
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDateTime, QRegExp, QEvent, QSize, QThread, Qt
import mimetypes




class Telinha(QMainWindow):
    '''
    TABELA ANEXO ###
     Lista de listas correspondendo as seguinte informações:
    {1:[objetoframe, path_do_arquivo], 2:[objetoframe, path_do_arquivo], 3:[objetoframe, path_do_arquivo],...}
     Cada lista encadeada corresponde a 1 widget na tela
    '''
    anexos = {}
    def __init__(self):
        
        super().__init__()
        self.programa = uic.loadUi('src\\telas\\telas_principais\\tela_anexo_email.ui')
        self.programa.show()
        self.programa.escolher_arquivo.clicked.connect(lambda: self.seleciona_arquivo())
        self.qtd_anexos = 0
        

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

    def gera_anexo_widget(self, tipo_arquivo, nome_arquivo, path_arquivo):
        
        frame_3 = QFrame(self.programa.scrollAreaWidgetContents)
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

        excluir_anexo = QPushButton(frame_3)
        excluir_anexo.setObjectName(u"excluir_anexo")
        excluir_anexo.setMaximumSize(QSize(150, 80))
        excluir_anexo.setStyleSheet(u"QPushButton{\n"
                                        "background-color: rgb(70, 70, 70);\n"
                                        "border-radius:4px;\n"
                                        "font-size:18px;\n"
                                        "font-weight:bold;\n"
                                        "\n"
                                        "color: rgb(217, 217, 217);\n"
                                        "}\n"
                                        "QPushButton:hover{\n"
                                        "background-color: grey;\n"
                                        "\n"
                                        "}\n"
                                        "QPushButton:pressed{\n"
                                        "background-color: rgb(35, 35,35);\n"
                                        "}")
        icon1 = QIcon()
        icon1.addFile(u"src/Icons/iconX.png", QSize(), QIcon.Normal, QIcon.Off)
        excluir_anexo.setIcon(icon1)
        excluir_anexo.setIconSize(QSize(30, 30))
        excluir_anexo.setText("Excluir")

        horizontalLayout_2.addWidget(excluir_anexo)
        

        self.programa.verticalLayout_3.addWidget(frame_3)
        excluir_anexo.clicked.connect(lambda: self.deleta_widget(frame_3))
        Telinha.anexos[self.qtd_anexos] = [frame_3]
        Telinha.anexos[self.qtd_anexos].append(path_arquivo)
        self.qtd_anexos += 1
        self.programa.label_3.setText(str(self.qtd_anexos))

    def deleta_widget(self, frame):
        frame.deleteLater()
        self.qtd_anexos -= 1
        self.programa.label_3.setText(str(self.qtd_anexos))
        for i in Telinha.anexos:
            if Telinha.anexos[i][0] is frame:
                print("é")
                del Telinha.anexos[i]
                break
        print(Telinha.anexos)

def advinha_tipo_arquivo(attachmentFile: str) -> str:
    content_type, encoding = mimetypes.guess_type(attachmentFile)
    try:
        file = attachmentFile.split('/')[-1]
        if ".PDF" in file.upper():
            return "pdf"
        if ".XLSX" in file.upper():
            return "excel"
        if ".PY" in file.upper():
            return "python"
    except:
        pass
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(attachmentFile, 'rb')
        msg = "text"
        fp.close()
    elif main_type == 'image':
        fp = open(attachmentFile, 'rb')
        msg = "image"
        fp.close()
    elif main_type == 'audio':
        fp = open(attachmentFile, 'rb')
        msg = "audio"
        fp.close()
    else:
        fp = open(attachmentFile, 'rb')
        msg = "arquivo"
        fp.close()
    return msg

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tela = Telinha()

    app.exec_()
    

