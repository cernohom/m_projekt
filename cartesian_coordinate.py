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
        #Buttons to zoom and unzoom
        zoom = QPushButton("PyQt button", self)
        zoom.setText("+")
        zoom.setGeometry(self.graph_width -self.buttonsize, self.graph_y, self.buttonsize, self.buttonsize)
        zoom.clicked.connect(self.clicked_plus)
        
        unzoom = QPushButton("PyQt button", self)
        unzoom.setText("-")
        unzoom.setGeometry(self.graph_width, self.graph_y , self.buttonsize, self.buttonsize)
        unzoom.clicked.connect(self.clicked_minus)
        
    def clicked_plus(self):
        self.velikost_grafu += 50
        ex = MathGraphApp()
        ex.show()

    def clicked_minus(self):
        if self.velikost_grafu - self.zoom_size > 0:
            self.velikost_grafu -= self.zoom_size
            ex = MathGraphApp()
            ex.show()
        else:
            self.zoom_size = self.zoom_size/10
            pass
        

        
    def paintEvent(self, event):
        # Define the drawing area
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
        #vertical lines
        pen.setColor(Qt.black)
        pen.setWidth(1)
        for i  in np.arange (0, self.graph_width + 1, self.velikost_grafu) :
            #start on the cornen of the graph and make line down
            if i == 0:
                path.moveTo(self.graph_x,self.graph_y)
                path.lineTo(self.graph_x, self.graph_height + self.graph_y)
            # move to the top of the graph
            else:
                self.graph_x_pen = self.graph_x + i
                path.moveTo(self.graph_x_pen, self.graph_y)
                path.lineTo(self.graph_x_pen, self.graph_height + self.graph_y)

        #horizontal lines
        for i  in np.arange (0, self.graph_height + 1, self.velikost_grafu) :
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

        #oznaceni os
        for x_poz in np.arange(-(self.graph_x_middle), self.graph_x_middle, self.velikost_grafu):
            x_label = QGraphicsTextItem(str(x_poz/self.velikost_grafu))
            x_label.setPos(self.graph_x + self.graph_x_middle + x_poz, self.graph_y + self.graph_y_middle)
            self.scene.addItem(x_label)
        
        for y_poz in np.arange(-(self.graph_y_middle), self.graph_y_middle, self.velikost_grafu):
            if y_poz != 0:
                y_label = QGraphicsTextItem(str((y_poz/self.velikost_grafu)*-1))
                y_label.setPos(self.graph_x + self.graph_x_middle, self.graph_y + self.graph_y_middle + y_poz)
                self.scene.addItem(y_label)
            
        #draw the graph
        #TODO not manual input of the expression
        x_values = np.arange(-(self.graph_x_middle)/self.velikost_grafu, (self.graph_x_middle)/self.velikost_grafu, 1/1000)
        y_values = [math.sin(x) for x in x_values]

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
