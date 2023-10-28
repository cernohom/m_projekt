import typing
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import sys
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 300, 300) # settting parameters for window
        self.setWindowTitle("Graphic Calculator") # setting window title
        self.initUI()

    def initUI(self):
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("click me")
        self.b1.clicked.connect(self.clicked)

        self.label = QtWidgets.QLabel(self)
        self.label.setText("ez kalkulacka")
        self.label.move(100,100)
    
    def clicked(self):
        self.label.setText("button pressed")
        self.update()
    
    def update(self):
        self.label.adjustSize()

def window():
    app = QApplication(sys.argv) #get system info
    win = MyWindow() # opening window
    win.setGeometry(200, 200, 300, 300) # settting parameters for window
    win.setWindowTitle("Graphic Calculator") # setting window title

    
    win.show() # window showup
    sys.exit(app.exec_()) # clean exit from app

window()

