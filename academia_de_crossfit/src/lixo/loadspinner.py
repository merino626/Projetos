import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *
from time import sleep

from waitingspinnerwidget import QtWaitingSpinner


class Loadspinner(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


        self.spinner = QtWaitingSpinner(self)
        self.spinner.setRoundness(90.0)
        self.spinner.setMinimumTrailOpacity(15.0)
        self.spinner.setTrailFadePercentage(70.0)
        self.spinner.setNumberOfLines(25)
        self.spinner.setLineLength(30)
        self.spinner.setLineWidth(3)
        self.spinner.setInnerRadius(19)
        self.spinner.setRevolutionsPerSecond(1)
        self.spinner.setColor(QColor(0, 0, 0))


    def startAnimation(self):
        self.show() 
        self.spinner.start()
        timer = QTimer(self)
        timer.singleShot(30000, self.stopAnimation)
    
    def stopAnimation(self):
        self.spinner.close()
        self.close()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Loadspinner()
    main.startAnimation()
    sys.exit(app.exec())