import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import *


class RTE(QMainWindow):
    def __init__(self):
        super(RTE, self).__init__()
        

        self.editor = QTextEdit()
        self.fontSizeBox = QSpinBox()

        font = QFont('Times', 24)
        self.editor.setFont(font)
        self.path = ""
        self.setCentralWidget(self.editor)
        self.setWindowTitle('Rich Text Editor')
        self.showMaximized()
        self.create_tool_bar()
        self.editor.setFontPointSize(24)
        
    def create_tool_bar(self):
        toolbar = QToolBar()
        
        
        undoBtn = QAction(QIcon('src/icons/undo.png'), 'undo', self)
        undoBtn.triggered.connect(self.editor.undo)
        toolbar.addAction(undoBtn)
        
        redoBtn = QAction(QIcon('src/icons/redo.png'), 'redo', self)
        redoBtn.triggered.connect(self.editor.redo)
        toolbar.addAction(redoBtn)
        
        copyBtn = QAction(QIcon('src/icons/copy.png'), 'copy', self)
        copyBtn.triggered.connect(self.editor.copy)
        toolbar.addAction(copyBtn)
        
        cutBtn = QAction(QIcon('src/icons/cut.png'), 'cut', self)
        cutBtn.triggered.connect(self.editor.cut)
        toolbar.addAction(cutBtn)
        
        pasteBtn = QAction(QIcon('src/icons/paste.png'), 'paste', self)
        pasteBtn.triggered.connect(self.editor.paste)
        toolbar.addAction(pasteBtn)
        
        
        self.fontBox = QComboBox(self)
        self.fontBox.addItems(["Courier Std", "Hellentic Typewriter Regular", "Helvetica", "Arial", "SansSerif", "Helvetica", "Times", "Monospace"])
        self.fontBox.activated.connect(self.setFont)
        toolbar.addWidget(self.fontBox)
        
        self.fontSizeBox.setValue(24)
        self.fontSizeBox.valueChanged.connect(self.setFontSize)
        toolbar.addWidget(self.fontSizeBox)
        
        rightAllign = QAction(QIcon('src/icons/right-align.png'), 'Right Allign', self)
        rightAllign.triggered.connect(lambda : self.editor.setAlignment(Qt.AlignRight))
        toolbar.addAction(rightAllign)
        
        leftAllign = QAction(QIcon('src/icons/left-align.png'), 'left Allign', self)
        leftAllign.triggered.connect(lambda : self.editor.setAlignment(Qt.AlignLeft))
        toolbar.addAction(leftAllign)
        
        centerAllign = QAction(QIcon('src/icons/center-align.png'), 'Center Allign', self)
        centerAllign.triggered.connect(lambda : self.editor.setAlignment(Qt.AlignCenter))
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
        

        self.addToolBar(toolbar)    
        
    def setFontSize(self):
        value = self.fontSizeBox.value()
        self.editor.setFontPointSize(value)
        
    def setFont(self):
        font = self.fontBox.currentText()
        self.editor.setCurrentFont(QFont(font))    
        
    def italicText(self):
        state = self.editor.fontItalic()
        self.editor.setFontItalic(not(state)) 
    
    def underlineText(self):
        state = self.editor.fontUnderline()
        self.editor.setFontUnderline(not(state))   
        
    def boldText(self):
        print(self.editor.toHtml())
        if self.editor.fontWeight != QFont.Bold:
            self.editor.setFontWeight(QFont.Bold)
            return
        self.editor.setFontWeight(QFont.Normal)         
    
        
app = QApplication(sys.argv)
window = RTE()
window.show()
sys.exit(app.exec_())   