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
        self.setGeometry(100, 100, 800, 600)

    def paintEvent(self, event):
        # Define the drawing area
        graph_width = 600
        graph_height = 400
        graph_x = 50
        graph_y = 50

        # Create a pen for drawing the graph
        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(1)

        # Create a QPainterPath to represent the graph
        path = QPainterPath()

        for i  in np.arange (10, graph_width, 10) :
            if i == 0:
                path.moveTo(i,i)
                path.lineTo(i, graph_height)
            else:
                path.moveTo(i, self.velikost_grafu)
                path.lineTo(i, graph_height)
                path.moveTo(i, self.velikost_grafu)
        
        for i  in np.arange (10, graph_height, 10) :
            if i == 0:
                path.moveTo(i,i)
                path.lineTo(graph_width, i)
            else:
                path.moveTo(self.velikost_grafu, i)
                path.lineTo(graph_width, i)
                path.moveTo(self.velikost_grafu, i)
        
                # Create a QGraphicsPathItem to display the graph
        graph_item = QGraphicsPathItem(path)
        graph_item.setPen(pen)
        self.scene.addItem(graph_item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MathGraphApp()
    ex.show()
    sys.exit(app.exec_())
