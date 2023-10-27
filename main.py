import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class GraphingCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphing Calculator")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        self.display = QLineEdit("sin(x)")  # Initial function to plot
        layout.addWidget(self.display)

        self.canvas = PlotCanvas(self, width=5, height=4)
        layout.addWidget(self.canvas)

        plot_button = QPushButton("Plot")
        plot_button.clicked.connect(self.plot)
        layout.addWidget(plot_button)

        self.central_widget.setLayout(layout)
        
        # Plot the initial function upon application launch
        self.plot()

    def plot(self):
        function_text = self.display.text()
        x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)  # Define the range of x values
        try:
            y = eval(function_text)  # Evaluate the function
            self.canvas.plot(x, y)
        except Exception as e:
            self.canvas.clear()

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

    def plot(self, x, y):
        self.ax.clear()
        self.ax.plot(x, y)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_title('Function Plot')
        self.draw()

    def clear(self):
        self.ax.clear()
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = GraphingCalculator()
    calculator.show()
    sys.exit(app.exec_())
