from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class chartwidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a figure and canvas for plotting
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Set up layout for the widget
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot(self, data, peaks, troughs):
        """Plot the stock data with peaks and troughs."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.plot(data['Date'], data['Close'], label="Stock Price")
        ax.scatter(data['Date'][peaks], data['Close'][peaks], color='green', label='Peaks')
        ax.scatter(data['Date'][troughs], data['Close'][troughs], color='red', label='Troughs')

        ax.set_title("Stock Prices with Peaks and Troughs")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend()

        self.canvas.draw()

