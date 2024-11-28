from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ChartWidget(QWidget):
    def __init__(self):
        super().__init__()

        #Initialize the figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_data(self, dates, prices, peaks, troughs):
        self.figure.clear()

        #Create a new subplot
        ax = self.figure.add_subplot(111)

        #Plot the stock data
        ax.plot(dates, prices, label="Stock Price", color='blue')

        # Highlight the peaks and troughs
        ax.scatter([dates[i] for i in peaks], [prices[i] for i in peaks], color='green', label='Peaks', zorder=5)
        ax.scatter([dates[i] for i in troughs], [prices[i] for i in troughs], color='red', label='Troughs', zorder=5)

        ax.set_title("Stock Prices with Peaks and Troughs", fontsize=16)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Price", fontsize=12)
        ax.legend()

        self.canvas.draw()
