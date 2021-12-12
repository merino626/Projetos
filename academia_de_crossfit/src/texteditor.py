#!/usr/bin/python3
# -- coding: utf-8 --
from PyQt5.QtWidgets import QTextEdit, QWidget, QVBoxLayout, QApplication, QFileDialog, QMessageBox, QHBoxLayout, \
                         QToolBar, QComboBox, QAction, QLineEdit, QMenu, QMainWindow, QActionGroup, \
                        QFontComboBox, QColorDialog, QInputDialog, QPushButton, QPlainTextEdit
from PyQt5.QtGui import QIcon, QPainter, QTextFormat, QColor, QTextCursor, QKeySequence, QClipboard, \
                        QTextCharFormat, QTextCharFormat, QFont, QPixmap, QFontDatabase, QFontInfo, QTextDocumentWriter, \
                        QImage, QTextListFormat, QTextBlockFormat, QTextDocumentFragment, QKeyEvent
from PyQt5.QtCore import Qt, QDir, QFile, QFileInfo, QTextStream, QSettings, QTextCodec, QSize, QMimeData, QUrl, QSysInfo, QEvent
from PyQt5 import QtPrintSupport
import sys, os, webbrowser

tab = "\t"
eof = "\n"
tableheader2 = "<table></tr><tr><td>    Column1    </td><td>    Column2    </td></tr></table>"
tableheader3 = "<table></tr><tr><td>    Column1    </td><td>    Column2    </td><td>    Column3    </td></tr></table>"


class myEditor(QWidget):
    def __init__(self, parent = None):
        super(myEditor, self).__init__(parent)

        self.setStyleSheet(myStyleSheet(self))
        self.MaxRecentFiles = 5
        self.windowList = []
        self.recentFileActs = []
        self.mainText = " "

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.editor = QTextEdit() 

        self.editor.setStyleSheet(myStyleSheet(self))
        self.editor.setTabStopWidth(14)
        self.editor.setContextMenuPolicy(Qt.CustomContextMenu)
      

        self.createToolbar()
        self.createMenubar()



    def createToolbar(self):          

        ### Format Toolbar
        self.format_tb = QToolBar(self)
        self.format_tb.setIconSize(QSize(16, 16))
        self.format_tb.setWindowTitle("Format Toolbar")
        
        self.actionTextBold = QAction(QIcon.fromTheme('format-text-bold-symbolic'), "&Bold", self, priority=QAction.LowPriority,
                shortcut=Qt.CTRL + Qt.Key_B, triggered=self.textBold, checkable=True)
        self.actionTextBold.setStatusTip("bold")
        bold = QFont()
        bold.setBold(True)
        self.actionTextBold.setFont(bold)
        self.format_tb.addAction(self.actionTextBold)    

        self.actionTextItalic = QAction(QIcon.fromTheme('format-text-italic-symbolic'), "&Italic", self, priority=QAction.LowPriority,
                shortcut=Qt.CTRL + Qt.Key_I, triggered=self.textItalic, checkable=True)
        italic = QFont()
        italic.setItalic(True)
        self.actionTextItalic.setFont(italic)
        self.format_tb.addAction(self.actionTextItalic)
        
        self.actionTextUnderline = QAction(QIcon.fromTheme('format-text-underline-symbolic'), "&Underline", self, priority=QAction.LowPriority,
                shortcut=Qt.CTRL + Qt.Key_U, triggered=self.textUnderline, checkable=True)
        underline = QFont()
        underline.setUnderline(True)
        self.actionTextUnderline.setFont(underline)
        self.format_tb.addAction(self.actionTextUnderline)
        
        self.format_tb.addSeparator()
        
        self.grp = QActionGroup(self, triggered=self.textAlign)

        if QApplication.isLeftToRight():
            self.actionAlignLeft = QAction(QIcon.fromTheme('format-justify-left-symbolic'),"&Left", self.grp)
            self.actionAlignCenter = QAction(QIcon.fromTheme('format-justify-center-symbolic'),"C&enter", self.grp)
            self.actionAlignRight = QAction(QIcon.fromTheme('format-justify-right-symbolic'),"&Right", self.grp)
        else:
            self.actionAlignRight = QAction(QIcon.fromTheme('gtk-justify-right-symbolic'),"&Right", self.grp)
            self.actionAlignCenter = QAction(QIcon.fromTheme('gtk-justify-center-symbolic'),"C&enter", self.grp)
            self.actionAlignLeft = QAction(QIcon.fromTheme('format-justify-left-symbolic'),"&Left", self.grp)
 
        self.actionAlignJustify = QAction(QIcon.fromTheme('format-justify-fill-symbolic'),"&Justify", self.grp)

        self.actionAlignLeft.setShortcut(Qt.CTRL + Qt.Key_L)
        self.actionAlignLeft.setCheckable(True)
        self.actionAlignLeft.setPriority(QAction.LowPriority)

        self.actionAlignCenter.setShortcut(Qt.CTRL + Qt.Key_E)
        self.actionAlignCenter.setCheckable(True)
        self.actionAlignCenter.setPriority(QAction.LowPriority)

        self.actionAlignRight.setShortcut(Qt.CTRL + Qt.Key_R)
        self.actionAlignRight.setCheckable(True)
        self.actionAlignRight.setPriority(QAction.LowPriority)

        self.actionAlignJustify.setShortcut(Qt.CTRL + Qt.Key_J)
        self.actionAlignJustify.setCheckable(True)
        self.actionAlignJustify.setPriority(QAction.LowPriority)

        self.format_tb.addActions(self.grp.actions())

        #self.indentAct = QAction(QIcon.fromTheme("format-indent-more-symbolic"), "indent more", self, triggered = self.indentLine, shortcut = "F8")

        pix = QPixmap(16, 16)
        pix.fill(Qt.black)
        self.actionTextColor = QAction(QIcon(pix), "TextColor...", self,
                triggered=self.textColor)
        self.format_tb.addSeparator()
        self.format_tb.addAction(self.actionTextColor)
        
        self.font_tb = QToolBar(self)
        self.font_tb.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)
        self.font_tb.setWindowTitle("Font Toolbar")
        
        self.comboStyle = QComboBox(self.font_tb)
        self.font_tb.addWidget(self.comboStyle)
        self.comboStyle.addItem("Standard")
        self.comboStyle.addItem("Bullet List (Disc)")
        self.comboStyle.addItem("Bullet List (Circle)")
        self.comboStyle.addItem("Bullet List (Square)")
        self.comboStyle.addItem("Ordered List (Decimal)")
        self.comboStyle.addItem("Ordered List (Alpha lower)")
        self.comboStyle.addItem("Ordered List (Alpha upper)")
        self.comboStyle.addItem("Ordered List (Roman lower)")
        self.comboStyle.addItem("Ordered List (Roman upper)")
        self.comboStyle.activated.connect(self.textStyle)

        self.comboFont = QFontComboBox(self.font_tb)
        self.font_tb.addSeparator()
        self.font_tb.addWidget(self.comboFont)
        self.comboFont.activated[str].connect(self.textFamily)

        self.comboSize = QComboBox(self.font_tb)
        self.font_tb.addSeparator()
        self.comboSize.setObjectName("comboSize")
        self.font_tb.addWidget(self.comboSize)
        self.comboSize.setEditable(True)

        db = QFontDatabase()
        for size in db.standardSizes():
            self.comboSize.addItem("%s" % (size))
        self.comboSize.addItem("%s" % (90))
        self.comboSize.addItem("%s" % (100))
        self.comboSize.addItem("%s" % (160))
        self.comboSize.activated[str].connect(self.textSize)
        self.comboSize.setCurrentIndex(
                self.comboSize.findText(
                        "%s" % (QApplication.font().pointSize())))    
   
        # self.addToolBar(self.format_tb)    

        # self.addToolBar(self.font_tb)

    def msgbox(self,title, message):
        QMessageBox.warning(self, title, message)

    def indentLine(self):
        if not self.editor.textCursor().selectedText() == "":
            ot = self.editor.textCursor().selection().toHtml()
            self.msgbox("HTML", str(ot))
        
    def indentLessLine(self):
        if not self.editor.textCursor().selectedText() == "":
            newline = u"\u2029"
            list = []
            ot = self.editor.textCursor().selectedText()
            theList  = ot.splitlines()
            linecount = ot.count(newline)
            for i in range(linecount + 1):
                list.insert(i, (theList[i]).replace(tab, "", 1))
            self.editor.textCursor().insertText(newline.join(list))
            self.setModified(True)    

    def createMenubar(self):        


        # Laying out...
        layoutV = QVBoxLayout()
        layoutV.addWidget(self.editor)
        ### main window
        mq = QWidget(self)
        mq.setLayout(layoutV)
        # self.setCentralWidget(mq)
        # self.statusBar().showMessage("Welcome to RichTextEdit * ")
        # Event Filter ...
        self.installEventFilter(self)
        self.cursor = QTextCursor()
        self.editor.setTextCursor(self.cursor)
        
        self.editor.setPlainText(self.mainText)
        self.editor.moveCursor(self.cursor.End)
        self.editor.textCursor().deletePreviousChar()
        self.editor.document().modificationChanged.connect(self.setWindowModified)
        self.extra_selections = []
        self.fname = ""
        self.filename = ""
        self.editor.setFocus()
        self.setModified(False)
        self.fontChanged(self.editor.font())
        self.colorChanged(self.editor.textColor())
        self.alignmentChanged(self.editor.alignment())
        self.editor.document().modificationChanged.connect(
                self.setWindowModified)

        self.setWindowModified(self.editor.document().isModified())
        self.editor.setAcceptRichText(True)
        self.editor.currentCharFormatChanged.connect(
                self.currentCharFormatChanged)
        self.editor.cursorPositionChanged.connect(self.cursorPositionChanged)

    def insertDate(self):
        import time
        from datetime import date
        today = date.today().strftime("%A, %d.%B %Y")
        self.editor.textCursor().insertText(today)

    def insertTime(self):
        import time
        from datetime import date
        today = time.strftime("%H:%M Uhr")
        self.editor.textCursor().insertText(today)

    def insertDateTime(self):
        self.insertDate()
        self.editor.textCursor().insertText(eof)
        self.insertTime()
        self.editor.textCursor().insertText(eof)

    def changeBGColor(self):
        all = self.editor.document().toHtml()
        bgcolor = all.partition("<body style=")[2].partition(">")[0].partition('bgcolor="')[2].partition('"')[0]
        if not bgcolor == "":
            col = QColorDialog.getColor(QColor(bgcolor), self)
            if not col.isValid():
                return
            else:
                colorname = col.name()
                new = all.replace("bgcolor=" + '"' + bgcolor + '"', "bgcolor=" + '"' + colorname + '"')
                self.editor.document().setHtml(new)
        else:
            col = QColorDialog.getColor(QColor("#FFFFFF"), self)
            if not col.isValid():
                return
            else:
                all = self.editor.document().toHtml()
                body = all.partition("<body style=")[2].partition(">")[0]
                newbody = body + "bgcolor=" + '"' + col.name() + '"'
                new = all.replace(body, newbody)    
                self.editor.document().setHtml(new)

    def editBody(self):
        all = self.editor.document().toHtml()
        body = all.partition("<body style=")[2].partition(">")[0]
        dlg = QInputDialog()
        mybody, ok = dlg.getText(self, 'change body style', "", QLineEdit.Normal, body, Qt.Dialog)
        if ok:
            new = all.replace(body, mybody)    
            self.editor.document().setHtml(new)
            self.statusBar().showMessage("body style changed")
        else:
            self.statusBar().showMessage("body style not changed")
        
    def insertTable(self):
        self.editor.textCursor().insertHtml(tableheader2)

    def insertTable3(self):
        self.editor.textCursor().insertHtml(tableheader3)

    def handleBrowser(self):
        if self.editor.toPlainText() == "":
            self.statusBar().showMessage("no text")
        else:
            if not self.editor.document().isModified() == True:
                webbrowser.open(self.filename, new=0, autoraise=True)
            else:
                myfilename = "/tmp/browser.html"
                writer = QTextDocumentWriter(myfilename)
                success = writer.write(self.editor.document())
                if success:
                    webbrowser.open(myfilename, new=0, autoraise=True)
                return success


    def grabLine(self):
        text = self.editor.textCursor().block().text()
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        

    def findText(self):
        word = self.findfield.text()
        if self.editor.find(word):
            return
        else:
            self.editor.moveCursor(QTextCursor.Start)            
            if self.editor.find(word):
                return
        
    def handleQuit(self):
        print("Goodbye ...")
        app.quit()

    def document(self):
        return self.editor.document
        
    def isModified(self):
        return self.editor.document().isModified()

    def setModified(self, modified):
        self.editor.document().setModified(modified)

    def setLineWrapMode(self, mode):
        self.editor.setLineWrapMode(mode)

    def clear(self):
        self.editor.clear()

    def setPlainText(self, *args, **kwargs):
        self.editor.setPlainText(*args, **kwargs)

    def setDocumentTitle(self, *args, **kwargs):
        self.editor.setDocumentTitle(*args, **kwargs)

    def set_number_bar_visible(self, value):
        self.numbers.setVisible(value)
        
    def replaceAll(self):
        oldtext = self.findfield.text()
        newtext = self.replacefield.text()
        if not oldtext == "":
            h = self.editor.toHtml().replace(oldtext, newtext)
            self.editor.setText(h)
            self.setModified(True)
            self.statusBar().showMessage("all replaced")
        else:
            self.statusBar().showMessage("nothing to replace")
        
    def replaceOne(self):
        oldtext = self.findfield.text()
        newtext = self.replacefield.text()
        if not oldtext == "":
            h = self.editor.toHtml().replace(oldtext, newtext, 1)
            self.editor.setText(h)
            self.setModified(True)
            self.statusBar().showMessage("one replaced")
        else:
            self.statusBar().showMessage("nothing to replace")
        

 
    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()

    def textBold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(self.actionTextBold.isChecked() and QFont.Bold or QFont.Normal)
        self.mergeFormatOnWordOrSelection(fmt)

    def textUnderline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.actionTextUnderline.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def textItalic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.actionTextItalic.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def textFamily(self, family):
        fmt = QTextCharFormat()
        fmt.setFontFamily(family)
        self.mergeFormatOnWordOrSelection(fmt)

    def textSize(self, pointSize):
        pointSize = float(self.comboSize.currentText())
        if pointSize > 0:
            fmt = QTextCharFormat()
            fmt.setFontPointSize(pointSize)
            self.mergeFormatOnWordOrSelection(fmt)

    def textStyle(self, styleIndex):
        cursor = self.editor.textCursor()
        if styleIndex:
            styleDict = {
                1: QTextListFormat.ListDisc,
                2: QTextListFormat.ListCircle,
                3: QTextListFormat.ListSquare,
                4: QTextListFormat.ListDecimal,
                5: QTextListFormat.ListLowerAlpha,
                6: QTextListFormat.ListUpperAlpha,
                7: QTextListFormat.ListLowerRoman,
                8: QTextListFormat.ListUpperRoman,
                        }

            style = styleDict.get(styleIndex, QTextListFormat.ListDisc)
            cursor.beginEditBlock()
            blockFmt = cursor.blockFormat()
            listFmt = QTextListFormat()

            if cursor.currentList():
                listFmt = cursor.currentList().format()
            else:
                listFmt.setIndent(1)
                blockFmt.setIndent(0)
                cursor.setBlockFormat(blockFmt)

            listFmt.setStyle(style)
            cursor.createList(listFmt)
            cursor.endEditBlock()
        else:
            bfmt = QTextBlockFormat()
            bfmt.setObjectIndex(-1)
            cursor.mergeBlockFormat(bfmt)

    def textColor(self):
        col = QColorDialog.getColor(self.editor.textColor(), self)
        if not col.isValid():
            return

        fmt = QTextCharFormat()
        fmt.setForeground(col)
        self.mergeFormatOnWordOrSelection(fmt)
        self.colorChanged(col)

    def textAlign(self, action):
        if action == self.actionAlignLeft:
            self.editor.setAlignment(Qt.AlignLeft | Qt.AlignAbsolute)
        elif action == self.actionAlignCenter:
            self.editor.setAlignment(Qt.AlignHCenter)
        elif action == self.actionAlignRight:
            self.editor.setAlignment(Qt.AlignRight | Qt.AlignAbsolute)
        elif action == self.actionAlignJustify:
            self.editor.setAlignment(Qt.AlignJustify)

    def currentCharFormatChanged(self, format):
        self.fontChanged(format.font())
        self.colorChanged(format.foreground().color())

    def cursorPositionChanged(self):
        self.alignmentChanged(self.editor.alignment())

    def clipboardDataChanged(self):
        self.actionPaste.setEnabled(len(QApplication.clipboard().text()) != 0)

    def mergeFormatOnWordOrSelection(self, format):
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)

        cursor.mergeCharFormat(format)
        self.editor.mergeCurrentCharFormat(format)

    def fontChanged(self, font):
        self.comboFont.setCurrentIndex(
                self.comboFont.findText(QFontInfo(font).family()))
        self.comboSize.setCurrentIndex(
                self.comboSize.findText("%s" % font.pointSize()))
        self.actionTextBold.setChecked(font.bold())
        self.actionTextItalic.setChecked(font.italic())
        self.actionTextUnderline.setChecked(font.underline())

    def colorChanged(self, color):
        pix = QPixmap(26, 20)
        pix.fill(color)
        self.actionTextColor.setIcon(QIcon(pix))

    def alignmentChanged(self, alignment):
        if alignment & Qt.AlignLeft:
            self.actionAlignLeft.setChecked(True)
        elif alignment & Qt.AlignHCenter:
            self.actionAlignCenter.setChecked(True)
        elif alignment & Qt.AlignRight:
            self.actionAlignRight.setChecked(True)
        elif alignment & Qt.AlignJustify:
            self.actionAlignJustify.setChecked(True)

            
    def handlePrintPreview(self):
        if self.editor.toPlainText() == "":
            self.statusBar().showMessage("no text")
        else:
            dialog = QtPrintSupport.QPrintPreviewDialog()
            dialog.setGeometry(30, 0, self.width() - 60, self.height() - 60)
            dialog.paintRequested.connect(self.handlePaintRequest)
            dialog.exec_()
            self.statusBar().showMessage("Print Preview closed")

    def handlePaintRequest(self, printer):
        printer.setDocName(self.filename)
        document = self.editor.document()
        document.print_(printer)
  
def myStyleSheet(self):
    return """
    QTextEdit
    {
    background: #fafafa;
    color: #202020;
    border: 1px solid #1EAE3D;
    selection-background-color: #729fcf;
    selection-color: #ffffff;
    }
    QMenuBar
    {
    background: transparent;
    border: 0px;
    }
    QToolBar
    {
    background: transparent;
    border: 0px;
    }
    QMainWindow
    {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                    stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
    }
        """       

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = myEditor()
    win.setWindowIcon(QIcon.fromTheme("gnome-mime-application-rtf"))
    win.setWindowTitle("RichTextEdit" + "[*]")
    win.setMinimumSize(640,250)
    win.showMaximized()
    if len(sys.argv) > 1:
        print(sys.argv[1])
        win.openFileOnStart(sys.argv[1])
    app.exec_()