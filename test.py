# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(463, 393)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button1 = QtWidgets.QPushButton(self.centralwidget)
        self.button1.setGeometry(QtCore.QRect(70, 150, 141, 61))
        self.button1.setObjectName("button1")
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(50, 40, 191, 81))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label1.setFont(font)
        self.label1.setObjectName("label1")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 463, 18))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFIleW = QtWidgets.QMenu(self.menubar)
        self.menuFIleW.setObjectName("menuFIleW")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionew = QtWidgets.QAction(MainWindow)
        self.actionew.setObjectName("actionew")
        self.actionnoo = QtWidgets.QAction(MainWindow)
        self.actionnoo.setObjectName("actionnoo")
        self.actionbumbum = QtWidgets.QAction(MainWindow)
        self.actionbumbum.setObjectName("actionbumbum")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.menuFile.addAction(self.actionew)
        self.menuFile.addAction(self.actionnoo)
        self.menuFIleW.addAction(self.actionCopy)
        self.menuFIleW.addAction(self.actionPaste)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuFIleW.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button1.setText(_translate("MainWindow", "Zmackni"))
        self.label1.setText(_translate("MainWindow", "Sportu zdar"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuFIleW.setTitle(_translate("MainWindow", "Edit"))
        self.actionew.setText(_translate("MainWindow", "New"))
        self.actionew.setStatusTip(_translate("MainWindow", "Create a new file"))
        self.actionew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionnoo.setText(_translate("MainWindow", "Save"))
        self.actionnoo.setStatusTip(_translate("MainWindow", "Save a file"))
        self.actionnoo.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionbumbum.setText(_translate("MainWindow", "bumbum"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setStatusTip(_translate("MainWindow", "Copy Text"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionPaste.setStatusTip(_translate("MainWindow", "Paste text"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
