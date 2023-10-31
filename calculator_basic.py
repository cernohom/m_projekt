# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calculator_basic.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(30, 10, 391, 361))
        font = QtGui.QFont()
        font.setFamily("MS PGothic")
        font.setPointSize(16)
        self.frame.setFont(font)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayoutWidget = QtWidgets.QWidget(self.frame)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(56, 0, 320, 261))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pEquals = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pEquals.setObjectName("pEquals")
        self.gridLayout.addWidget(self.pEquals, 4, 1, 1, 1)
        self.p2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.p2.setObjectName("p2")
        self.gridLayout.addWidget(self.p2, 1, 1, 1, 1)
        self.p1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.p1.setObjectName("p1")
        self.gridLayout.addWidget(self.p1, 1, 0, 1, 1)
        self.p7 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.p7.setObjectName("p7")
        self.gridLayout.addWidget(self.p7, 3, 0, 1, 1)
        self.p4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.p4.setObjectName("p4")
        self.gridLayout.addWidget(self.p4, 2, 0, 1, 1)
        self.pPlus = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pPlus.setObjectName("pPlus")
        self.gridLayout.addWidget(self.pPlus, 4, 2, 1, 1)
        self.pdivided = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pdivided.setObjectName("pdivided")
        self.gridLayout.addWidget(self.pdivided, 3, 3, 1, 1)
        self.p5 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.p5.setObjectName("p5")
        self.gridLayout.addWidget(self.p5, 2, 1, 1, 1)
        self.pTimes = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pTimes.setObjectName("pTimes")
        self.gridLayout.addWidget(self.pTimes, 2, 3, 1, 1)
        self.Answer = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Answer.setAutoFillBackground(True)
        self.Answer.setObjectName("Answer")
        self.gridLayout.addWidget(self.Answer, 0, 0, 1, 4)
        self.p6 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.p6.setObjectName("p6")
        self.gridLayout.addWidget(self.p6, 2, 2, 1, 1)
        self.p3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.p3.setObjectName("p3")
        self.gridLayout.addWidget(self.p3, 1, 2, 1, 1)
        self.p0 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.p0.setObjectName("p0")
        self.gridLayout.addWidget(self.p0, 4, 0, 1, 1)
        self.p9 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.p9.setObjectName("p9")
        self.gridLayout.addWidget(self.p9, 3, 2, 1, 1)
        self.pMinus = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pMinus.setObjectName("pMinus")
        self.gridLayout.addWidget(self.pMinus, 4, 3, 1, 1)
        self.pDEL = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pDEL.setObjectName("pDEL")
        self.gridLayout.addWidget(self.pDEL, 1, 3, 1, 1)
        self.p8 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.p8.setObjectName("p8")
        self.gridLayout.addWidget(self.p8, 3, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.p1.clicked.connect(lambda:self.clicked(str("1")))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pEquals.setText(_translate("MainWindow", "="))
        self.p2.setText(_translate("MainWindow", "2"))
        self.p1.setText(_translate("MainWindow", "1"))
        self.p7.setText(_translate("MainWindow", "7"))
        self.p4.setText(_translate("MainWindow", "4"))
        self.pPlus.setText(_translate("MainWindow", " +"))
        self.pdivided.setText(_translate("MainWindow", "/"))
        self.p5.setText(_translate("MainWindow", "5"))
        self.pTimes.setText(_translate("MainWindow", "*"))
        self.Answer.setText(_translate("MainWindow", ""))
        self.p6.setText(_translate("MainWindow", "6"))
        self.p3.setText(_translate("MainWindow", "3"))
        self.p0.setText(_translate("MainWindow", "0"))
        self.p9.setText(_translate("MainWindow", "9"))
        self.pMinus.setText(_translate("MainWindow", "-"))
        self.pDEL.setText(_translate("MainWindow", "DEL"))
        self.p8.setText(_translate("MainWindow", "8"))

    def clicked(self, text)-> None:
        self.Answer.setText(str(self.Answer.text) + str(text))
        self.Answer.adjustSize()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())