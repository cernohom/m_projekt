import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPathItem, QGraphicsTextItem
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
        graph_width = 1000
        graph_height = 1000
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
        pen.setColor(Qt.darkBlue)
        path2.moveTo(graph_x + graph_width/2, graph_y)
        path2.lineTo(graph_x + graph_width/2, graph_y + graph_height)
        path2.moveTo(graph_x, graph_y + graph_height/2)
        path2.lineTo(graph_x + graph_width,  graph_y + graph_height/2)
         
        graph_item = QGraphicsPathItem(path2)
        graph_item.setPen(pen)
        self.scene.addItem(graph_item)

        #oznaceni os
        for x_poz in range(-(graph_width//2), graph_width//2, self.velikost_grafu):
            x_label = QGraphicsTextItem(str(x_poz/self.velikost_grafu))
            x_label.setPos(graph_x + graph_width/2 + x_poz, graph_y + graph_height/2)
            self.scene.addItem(x_label)
        
        for y_poz in range(-(graph_height//2), graph_height//2, self.velikost_grafu):
            if y_poz != 0:
                y_label = QGraphicsTextItem(str((y_poz/self.velikost_grafu)*-1))
                y_label.setPos(graph_x + graph_width/2, graph_x + graph_width/2 + y_poz)
                self.scene.addItem(y_label)
            
        #draw the graph
        #TODO not manual input of the expression
        #TODO functional input
        x_values = np.arange(-(graph_width/2), (graph_width/2) + 1, self.velikost_grafu/100)
        y_values = [x**2 for x in x_values]

        #contruct path for the expression
        for i in range(len(x_values)):
            x = graph_x + (x_values[i] - x_values[0])
            if (y_values[i] / self.velikost_grafu) > graph_height/2 or (y_values[i] / self.velikost_grafu) < -graph_height/2 and i != 0:
                path3.moveTo(x, graph_y)
            elif (y_values[i] / self.velikost_grafu) < -graph_height/2 and i != 0:
                path3.moveTo(x, graph_y + graph_height)
            else:    
                y = graph_y + (graph_height/2 - (y_values[i] / self.velikost_grafu))
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
