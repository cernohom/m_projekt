import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPathItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QPainterPath

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
        self.velikost_grafu = 100
        
        self.setWindowTitle('Math Expression Graph')
        self.setGeometry(100, 100, 1200,600)

    def paintEvent(self, event):
        # Define the drawing area
        graph_width = 1200
        graph_height = 600
        graph_x = 100
        graph_y = 100

        # Create a pen for drawing the graph
        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(1)

        # Create a QPainterPath to represent the graph
        path = QPainterPath()
        path2 = QPainterPath()
        path3 = QPainterPath()
        #vertical lines
        for i  in np.arange (0, graph_width + 1, self.velikost_grafu) :
            #start on the cornen of the graph and make line down
            if i == 0:
                path.moveTo(graph_x,graph_y)
                path.lineTo(graph_x, graph_height + graph_y)
            # move to the top of the graph
            else:
                graph_x_pen = graph_x + i
                path.moveTo(graph_x_pen, graph_y)
                path.lineTo(graph_x_pen, graph_height + graph_y)
        #horizontal lines
        for i  in np.arange (0, graph_height + 1, self.velikost_grafu) :
            if i == 0:
                path.moveTo(graph_x,graph_y)
                path.lineTo(graph_width + graph_x, graph_y)
            else:
                graph_y_pen = graph_y + i
                path.moveTo(graph_x, graph_y_pen)
                path.lineTo(graph_width + graph_x, graph_y_pen)
        # Create a QGraphicsPathItem to display the graph
        graph_item = QGraphicsPathItem(path)
        graph_item.setPen(pen)
        self.scene.addItem(graph_item)
        
        #y and x axes
        pen.setWidth(2)
        path2.moveTo(graph_x + graph_width/2, graph_y)
        path2.lineTo(graph_x + graph_width/2, graph_y + graph_height)
        path2.moveTo(graph_x, graph_y + graph_height/2)
        path2.lineTo(graph_x + graph_width,  graph_y + graph_height/2)
         
        graph_item = QGraphicsPathItem(path2)
        graph_item.setPen(pen)
        self.scene.addItem(graph_item)
        
        #draw the graph
        values_amount = graph_width/self.velikost_grafu
        
        #TODO not manual input of the expression
        x_values = np.arange(-(values_amount/2), (values_amount/2) + 1, self.velikost_grafu/100)
        y_values = [x ** 2 for x in x_values]

        #contruct path for the expression
        for i in range(len(x_values)):
            x = graph_x + (x_values[i] - x_values[0])
            y = graph_y + (graph_height - y_values[i])
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
