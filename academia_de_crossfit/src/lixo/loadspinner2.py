import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
  
  
class LoadingGif(QtWidgets.QMainWindow):
  
    def mainUI(self):
        self.loading = QtWidgets.QLabel() # create the QLabel
        self.addWidget(self.loading) # add it to our layout
        movie = QMovie("spinner.gif") # Create a QMovie from our gif
        self.loading.setMovie(movie) # use setMovie function in our QLabel
        self.loading.setFixedSize(60, 60) # set its size
        self.loading.setMaximumWidth(50) # set Max width
        movie.start() # now start the gif
        # and to stop the gif
        movie.stop()
  

  
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
demo = LoadingGif()
demo.mainUI(window)
window.show()
sys.exit(app.exec_())