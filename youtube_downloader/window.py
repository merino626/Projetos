# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'telapJjRUo.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PyQt5.QtWidgets import *

import resources

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(740, 622)
        MainWindow.setMinimumSize(QSize(740, 600))
        MainWindow.setMaximumSize(QSize(800, 700))
        icon = QIcon()
        icon.addFile(u":/youtube/2592371-200.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"background-color: rgb(32, 32, 32);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(150, 16777215))
        self.label_4.setPixmap(QPixmap(u":/youtube/logo.png"))
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_4)

        self.label_5 = QLabel(self.frame_2)
        self.label_5.setObjectName(u"label_5")
        font = QFont()
        font.setFamily(u"Tahoma")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_5)


        self.verticalLayout_2.addWidget(self.frame_2)

        self.line = QFrame(self.frame)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 50))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setSpacing(8)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 0))
        self.label_3.setMaximumSize(QSize(450, 16777215))
        font1 = QFont()
        font1.setFamily(u"Tahoma")
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setWeight(75)
        self.label_3.setFont(font1)
        self.label_3.setStyleSheet(u"color:white;")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_3)

        self.pushButton = QPushButton(self.frame_3)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"color:white;\n"
"background-color: rgb(50, 50, 50);\n"
"font-size:19px;")
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QSize(25, 25))

        self.horizontalLayout_2.addWidget(self.pushButton)


        self.verticalLayout_2.addWidget(self.frame_3)

        self.label_12 = QLabel(self.frame)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setStyleSheet(u"color:white;")
        self.label_12.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_12)

        self.line_2 = QFrame(self.frame)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setStyleSheet(u"")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_2)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 50))
        self.frame_4.setMaximumSize(QSize(16777215, 250))
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setSpacing(8)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(180, 16777215))
        self.label_2.setStyleSheet(u"color:white;")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.lineEdit = QLineEdit(self.frame_4)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMaximumSize(QSize(500, 16777215))
        self.lineEdit.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_3.addWidget(self.lineEdit)


        self.verticalLayout_2.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.frame)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 50))
        self.frame_5.setMaximumSize(QSize(16777215, 50))
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton_2 = QPushButton(self.frame_5)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMaximumSize(QSize(200, 16777215))
        self.pushButton_2.setStyleSheet(u"color:white;\n"
"background-color: rgb(50, 50, 50);\n"
"font-size:19px;")

        self.horizontalLayout_4.addWidget(self.pushButton_2)


        self.verticalLayout_2.addWidget(self.frame_5)

        self.label_13 = QLabel(self.frame)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setStyleSheet(u"color:white;\n"
"\n"
"font-size:19px;")
        self.label_13.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_13)

        self.stackedWidget = QStackedWidget(self.frame)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_4 = QVBoxLayout(self.page)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.frame_6 = QFrame(self.page)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 250))
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_6 = QLabel(self.frame_6)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(300, 250))
        self.label_6.setPixmap(QPixmap(u":/youtube/video_thumb.jpg"))
        self.label_6.setScaledContents(True)

        self.horizontalLayout_5.addWidget(self.label_6)

        self.frame_7 = QFrame(self.frame_6)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_7)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_8 = QFrame(self.frame_7)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_7 = QLabel(self.frame_8)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setLayoutDirection(Qt.LeftToRight)
        self.label_7.setStyleSheet(u"color:white;\n"
"\n"
"font-size:19px;")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.label_7)

        self.pushButton_3 = QPushButton(self.frame_8)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setStyleSheet(u"color:white;\n"
"background-color: rgb(50, 50, 50);\n"
"font-size:19px;")

        self.horizontalLayout_6.addWidget(self.pushButton_3)


        self.verticalLayout_3.addWidget(self.frame_8)

        self.frame_9 = QFrame(self.frame_7)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_8 = QLabel(self.frame_9)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setStyleSheet(u"color:white;\n"
"\n"
"font-size:16px;\n"
"font-weight:bold;")
        self.label_8.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.label_8)

        self.pushButton_4 = QPushButton(self.frame_9)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setStyleSheet(u"color:white;\n"
"background-color: rgb(50, 50, 50);\n"
"font-size:19px;")

        self.horizontalLayout_7.addWidget(self.pushButton_4)


        self.verticalLayout_3.addWidget(self.frame_9)

        self.frame_14 = QFrame(self.frame_7)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_10 = QLabel(self.frame_14)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(205, 0))
        self.label_10.setLayoutDirection(Qt.LeftToRight)
        self.label_10.setStyleSheet(u"color:white;\n"
"\n"
"font-size:19px;")
        self.label_10.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_12.addWidget(self.label_10)

        self.pushButton_5 = QPushButton(self.frame_14)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setStyleSheet(u"color:white;\n"
"background-color: rgb(50, 50, 50);\n"
"font-size:19px;")

        self.horizontalLayout_12.addWidget(self.pushButton_5)


        self.verticalLayout_3.addWidget(self.frame_14)

        self.label_15 = QLabel(self.frame_7)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setStyleSheet(u"color:white;\n"
"\n"
"font-size:19px;")

        self.verticalLayout_3.addWidget(self.label_15)


        self.horizontalLayout_5.addWidget(self.frame_7)


        self.verticalLayout_4.addWidget(self.frame_6)

        self.stackedWidget.addWidget(self.page)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_6 = QVBoxLayout(self.page_3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_11 = QLabel(self.page_3)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setStyleSheet(u"font-size:50px;\n"
"color:white;")
        self.label_11.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.label_11)

        self.stackedWidget.addWidget(self.page_3)

        self.verticalLayout_2.addWidget(self.stackedWidget)


        self.verticalLayout.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Youtube Downloader", None))
        self.label_4.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:36pt; color:#ffffff;\">YouTube Downloader</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Selecionar diret\u00f3rio:", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Selecionar", None))
        self.label_12.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">Url do video:</span></p></body></html>", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Buscar", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_6.setText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Maior resolu\u00e7\u00e3o (720p>)", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Baixa qualidade (360p<)", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Mp3", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Procurando video ...", None))
    # retranslateUi

