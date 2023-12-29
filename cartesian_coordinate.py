import sys
import numpy as np
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPathItem, QGraphicsTextItem, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QPainterPath, QBrush, QColor

class MathGraphApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.view = QGraphicsView(self)
        self.setCentralWidget(self.view)
        self.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)

        #hodnoty pro graf
        self.velikost_grafu = 50
        self.graph_width = 600
        self.graph_height = 800
        self.graph_x = 100
        self.graph_y = 100
        self.buttonsize = 50
        self.zoom_size = 50

        self.setWindowTitle('Math Expression Graph')
        self.setGeometry(100, 100, self.graph_width + 200,self.graph_height + 200)

        self.UiComponents()
        self.show()

    def UiComponents(self):
        #zoom button
        zoom = QPushButton("PyQt button", self)
        zoom.setText("+")
        zoom.setGeometry(self.graph_width + self.graph_x - self.buttonsize, self.graph_y, self.buttonsize, self.buttonsize)
        zoom.clicked.connect(self.clicked_plus)
        
        #unzoom button
        unzoom = QPushButton("PyQt button", self)
        unzoom.setText("-")
        unzoom.setGeometry(self.graph_width + self.graph_x, self.graph_y , self.buttonsize, self.buttonsize)
        unzoom.clicked.connect(self.clicked_minus)
        
    #what happens after i click plus
    def clicked_plus(self):
        if self.zoom_size < 300 :
            self.velikost_grafu += self.zoom_size
        else:
            self.velikost_grafu/10
        self.view.repaint

    #what happens after i click minus
    def clicked_minus(self):
        if self.velikost_grafu - self.zoom_size > 0:
            self.velikost_grafu -= self.zoom_size
            round(self.velikost_grafu,1)
        #too small numbers too hard for comp
        elif self.velikost_grafu > 0.1:
            self.velikost_grafu = self.velikost_grafu / 10
        else:    
            pass
        MathGraphApp()

        
    def paintEvent(self, event):
        #additional values to not calculate everytime
        self.graph_x_middle = self.graph_width/2
        self.graph_y_middle = self.graph_height/2

        # Create a pen for drawing the graph
        pen = QPen()
        pen.setColor(Qt.red)
        pen.setWidth(2)

        # Create a QPainterPath to represent the graph
        path = QPainterPath()
        path2 = QPainterPath()
        path3 = QPainterPath()
        path4 = QPainterPath()

        #background
        path4.addRect(self.graph_x, self.graph_y, self.graph_width, self.graph_height)
        graph_item = QGraphicsPathItem(path4)
        graph_item.setPen(pen)
        graph_item.setBrush(QBrush(QColor(Qt.white)))
        self.scene.addItem(graph_item)

        #vertical lines + labels
        pen.setColor(Qt.black)
        pen.setWidth(1)

        #on the right from y axis
        for i  in np.arange (self.graph_x_middle, self.graph_width, 50) :
            x_label = QGraphicsTextItem(str (round ((i - self.graph_x_middle) / self.velikost_grafu, 1)))
            x_label.setPos(self.graph_x + i, self.graph_y + self.graph_y_middle)
            self.scene.addItem(x_label)
            #start in the middle of the graph and make line down
            if i == 0:
                path.moveTo(self.graph_x,self.graph_y)
                path.lineTo(self.graph_x, self.graph_height + self.graph_y)
            # move to the top of the graph
            else:
                self.graph_x_pen = self.graph_x + i
                path.moveTo(self.graph_x_pen, self.graph_y)
                path.lineTo(self.graph_x_pen, self.graph_height + self.graph_y)
        
        #on the left from y axis
        for i  in reversed(np.arange (self.graph_x - 50, self.graph_x_middle, 50)) :
            x_label = QGraphicsTextItem(str (round ((i - self.graph_x_middle) / self.velikost_grafu, 1)))
            x_label.setPos(self.graph_x + i, self.graph_y + self.graph_y_middle)
            self.scene.addItem(x_label)
            #start in the middle of the graph and make line down
            if i == 0:
                path.moveTo(self.graph_x,self.graph_y)
                path.lineTo(self.graph_x, self.graph_height + self.graph_y)
            # move to the top of the graph
            else:
                self.graph_x_pen = self.graph_x + i
                path.moveTo(self.graph_x_pen, self.graph_y)
                path.lineTo(self.graph_x_pen, self.graph_height + self.graph_y)    

        #horizontal lines
        for i  in np.arange (self.graph_y_middle + self.graph_y - 50, self.graph_height, 50) :
            y_label = QGraphicsTextItem(str (round (((i - self.graph_y_middle) / self.velikost_grafu) * - 1, 1)))
            y_label.setPos(self.graph_x + self.graph_x_middle, self.graph_y + i)
            self.scene.addItem(y_label)
            if i == 0:
                path.moveTo(self.graph_x,self.graph_y)
                path.lineTo(self.graph_width + self.graph_x, self.graph_y)
            else:
                self.graph_y_pen = self.graph_y + i
                path.moveTo(self.graph_x, self.graph_y_pen)
                path.lineTo(self.graph_width + self.graph_x, self.graph_y_pen)

        for i  in reversed(np.arange (self.graph_y - 50, self.graph_y_middle, 50)) :
            y_label = QGraphicsTextItem(str (round (((i - self.graph_y_middle) / self.velikost_grafu) * - 1, 1)))
            y_label.setPos(self.graph_x + self.graph_x_middle, self.graph_y + i)
            self.scene.addItem(y_label)
            if i == 0:
                path.moveTo(self.graph_x,self.graph_y)
                path.lineTo(self.graph_width + self.graph_x, self.graph_y)
            else:
                self.graph_y_pen = self.graph_y + i
                path.moveTo(self.graph_x, self.graph_y_pen)
                path.lineTo(self.graph_width + self.graph_x, self.graph_y_pen)
        
        # Create a QGraphicsPathItem to display the graph
        graph_item = QGraphicsPathItem(path)
        graph_item.setPen(pen)
        self.scene.addItem(graph_item)
        
        #y and x axes
        pen.setWidth(2)
        pen.setColor(Qt.darkBlue)
        path2.moveTo(self.graph_x + self.graph_x_middle, self.graph_y)
        path2.lineTo(self.graph_x + self.graph_x_middle, self.graph_y + self.graph_height)
        path2.moveTo(self.graph_x, self.graph_y + self.graph_y_middle)
        path2.lineTo(self.graph_x + self.graph_width,  self.graph_y + self.graph_y_middle)
         
        graph_item = QGraphicsPathItem(path2)
        graph_item.setPen(pen)
        self.scene.addItem(graph_item)
            
        #draw the graph
        #TODO not manual input of the expression
        x_values = np.arange(-(self.graph_x_middle)/self.velikost_grafu, (self.graph_x_middle)/self.velikost_grafu, 1/10)
        y_values = [x ** 2 for x in x_values]

        #contruct path for the expression
        for i in range(len(x_values)):
            x = self.graph_x + self.graph_x_middle + (x_values[i]*self.velikost_grafu)
            if (y_values[i] * self.velikost_grafu) > self.graph_y_middle and i != 0:
                path3.moveTo(x, self.graph_y)
            elif (y_values[i] * self.velikost_grafu) < -self.graph_y_middle and i != 0:
                path3.moveTo(x, self.graph_y + self.graph_height)
            else:    
                y = self.graph_y + (self.graph_y_middle - (y_values[i] * self.velikost_grafu))
                if i == 0:
                    path3.moveTo(x, y)
                else:
                    path3.lineTo(x, y)

        pen.setWidth(2)
        pen.setColor(Qt.red)
        graph_item = QGraphicsPathItem(path3)
        graph_item.setPen(pen)
        self.scene.addItem(graph_item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MathGraphApp()
    ex.show()
    sys.exit(app.exec_())
