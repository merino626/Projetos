import main
import sys
from PyQt5 import uic, QtWidgets



def sair_modulo_matricula():
    main.tela_cadastro.close()



main.tela_cadastro.show()

main.tela_cadastro.pushButton_5.clicked.connect(sair_modulo_matricula)

main.app.exec()

