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
        pen.setColor(Qt.red)
        pen.setWidth(2)

        # Create a QPainterPath to represent the graph
        path = QPainterPath()

        # Define the x values
        x_values = np.arange(-10, 11, 0.1)
        
        # Define the mathematical expression (e.g., x^2 - 5x + 6)
        y_values = [x ** 2 - 5 * x + 6 for x in x_values]

        # Scale the x and y values to fit the drawing area
        x_scale = graph_width / (x_values[-1] - x_values[0])
        y_scale = graph_height / (20)  # Assuming a range of -10 to 10 for the y-axis
        
        # Construct the QPainterPath for the graph
        for i in range(len(x_values)):
            x = graph_x + (x_values[i] - x_values[0]) * x_scale
            y = graph_y + graph_height - (y_values[i] + 10) * y_scale
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)

        # Create a QGraphicsPathItem to display the graph
        graph_item = QGraphicsPathItem(path)
        graph_item.setPen(pen)

        self.scene.addItem(graph_item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MathGraphApp()
    ex.show()
    sys.exit(app.exec_())

