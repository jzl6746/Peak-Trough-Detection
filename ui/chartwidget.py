from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


class ChartWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_data(self, dates, prices, peaks, troughs):
        print("IN PLOT DATA")
        print(f"DATES:\n{dates}")
        print(f"PRICES:\n{prices}")
        print(f"PEAKS:\n{peaks}")
        print(f"TROUGHS:\n{troughs}")
        
        # Convert string dates to datetime objects for plotting
        dates = [datetime.strptime(date_str, '%Y-%m-%d') for date_str in dates]
        print("Converted Dates:", dates)
        
        print(f"Number of dates: {len(dates)}")
        print(f"Number of prices: {len(prices)}")

        if not dates or not prices:
            print("Error: Dates or prices are empty!")
            return
        
        self.figure.clear()
    
        # Create a new subplot
        ax = self.figure.add_subplot(111)
    
        # Plot the stock data
        ax.plot(dates, prices, label="Stock Price", color='blue')
    
        # Highlight the peaks and troughs if they exist
        if peaks:
            ax.scatter([dates[i] for i in peaks], [prices[i] for i in peaks], color='green', label='Peaks', zorder=5)
        if troughs:
            ax.scatter([dates[i] for i in troughs], [prices[i] for i in troughs], color='red', label='Troughs', zorder=5)
    
        # Add a title, labels, and legend
        ax.set_title("Stock Prices with Peaks and Troughs", fontsize=16)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Price", fontsize=12)
        ax.legend()

        # Format the x-axis to handle datetime objects properly
        ax.xaxis.set_major_locator(mdates.WeekdayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        
        # Rotate the date labels for better readability
        plt.xticks(rotation=45)

        # Redraw the canvas
        self.canvas.draw()
