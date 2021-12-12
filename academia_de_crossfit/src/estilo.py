ESTILO_DATA = """QDateEdit{font-size: 14px;
                text-align: center;
                color: white;
                background-color: #272727;
                border-style: solid;
                border-width: 1px;
                border-color: rgb(19,20,30);
                }

                QCalendarWidget QToolButton {
                height: 10px;
                width: 70px;
                color: white;
                font-size: 16px;
                icon-size: 25px, 25px;
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #333333);
                }

                QCalendarWidget QMenu {
                    width: 105px;
                    left: 10px;
                    color: white;
                    font-size:  14px;
                    background-color: rgb(100, 100, 100);
                }

                QCalendarWidget QSpinBox { 
                    width: 105px; 
                    font-size:16px; 
                    color: white; 
                    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #333333); 
                    selection-background-color: rgb(136, 136, 136);
                    selection-color: rgb(255, 255, 255);
                }

                QCalendarWidget QSpinBox::up-button {
                    subcontrol-origin: border;
                    subcontrol-position: top right;
                    width:20px;
                }

                QCalendarWidget QSpinBox::down-button {
                    subcontrol-origin: border;
                    subcontrol-position: bottom right;
                    width:20px;}

                QCalendarWidget QSpinBox::up-arrow { 
                    width:20px;
                    height:20px;
                }

                QCalendarWidget QSpinBox::down-arrow{
                    width:20px;
                    height:20px;
                }
                
                QCalendarWidget QWidget {
                    alternate-background-color: rgb(128, 128, 128);
                }
                
                QCalendarWidget QAbstractItemView:enabled{
                    font-size:16px;  
                    color: rgb(180, 180, 180);  
                    background-color: #272727;  
                    selection-background-color: rgb(64, 64, 64); 
                    selection-color: rgb(0, 255, 0); 
                }
                
                QCalendarWidget QWidget#qt_calendar_navigationbar { 
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #333333); 
                }

                QCalendarWidget QAbstractItemView:disabled { 
                color: rgb(64, 64, 64); 
                }
                }"""


ESTILO_COMBOBOX = """QComboBox, QComboBox QAbstractItemView{font-size: 14px;
                text-align: center;
                color: white;
                border-style: solid;
                border-width: 1px;
                border-color: rgb(19,20,30);
                }"""


ESTILO_LINEEDIT = "QLineEdit{font-size: 14px;\
                text-align: center;\
                color: white;\
                }"


SUCESS_LOGIN = """	border: 2px solid rgb(47, 211, 1);\
                    border-radius:5px;\
                    padding: 15px;\
                    background-color: rgb(30, 30, 30);\
                    color: rgb(100, 100, 100);"""


MENSAGEM_SUCESSO = """background-color: rgb(35, 131, 0);\
                    border-radius: 10px;"""


FAILED_LOGIN = """	border: 2px solid rgb(255, 0, 0);\
                    border-radius:5px;\
                    padding: 15px;\
                    background-color: rgb(30, 30, 30);\
                    color: rgb(100, 100, 100);"""


ESTILO_DATA2 = """QDateEdit{
                font-size: 20px;
                text-align: center;
                border-radius: 10px;
                background-color: rgb(20, 20, 20);
                color: rgb(255, 255, 255);
                }

                QCalendarWidget QToolButton {
                height: 10px;
                width: 70px;
                color: white;
                font-size: 16px;
                icon-size: 25px, 25px;
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #333333);
                }

                QCalendarWidget QMenu {
                    width: 105px;
                    left: 10px;
                    color: white;
                    font-size:  14px;
                    background-color: rgb(100, 100, 100);
                }

                QCalendarWidget QSpinBox { 
                    width: 105px; 
                    font-size:16px; 
                    color: white; 
                    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #333333); 
                    selection-background-color: rgb(136, 136, 136);
                    selection-color: rgb(255, 255, 255);
                }

                QCalendarWidget QSpinBox::up-button {
                    subcontrol-origin: border;
                    subcontrol-position: top right;
                    width:20px;
                }

                QCalendarWidget QSpinBox::down-button {
                    subcontrol-origin: border;
                    subcontrol-position: bottom right;
                    width:20px;}

                QCalendarWidget QSpinBox::up-arrow { 
                    width:20px;
                    height:20px;
                }

                QCalendarWidget QSpinBox::down-arrow{
                    width:20px;
                    height:20px;
                }
                
                QCalendarWidget QWidget {
                    alternate-background-color: rgb(128, 128, 128);
                }
                
                QCalendarWidget QAbstractItemView:enabled{
                    font-size:16px;  
                    color: rgb(180, 180, 180);  
                    background-color: #272727;  
                    selection-background-color: rgb(64, 64, 64); 
                    selection-color: rgb(0, 255, 0); 
                }
                
                QCalendarWidget QWidget#qt_calendar_navigationbar { 
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #333333); 
                }

                QCalendarWidget QAbstractItemView:disabled { 
                color: rgb(64, 64, 64); 
                }
                }"""


DISABLED_INPUT = """QLineEdit{
  font-size: 20px;
  text-align: center;
  border-radius: 10px;
background-color: #505050;
padding-left: 10px;
}"""

ENABLED_INPUT = """QLineEdit{
  font-size: 20px;
  text-align: center;
  border-radius: 10px;
background-color: #ffffff;
padding-left: 10px;
}"""


HTML_PLACEHOLDER = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;"><p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:16px; font-weight:600;">Digite a mensagem do email...</span></p></body></html>"""