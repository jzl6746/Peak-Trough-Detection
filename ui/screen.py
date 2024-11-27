import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QDateEdit, QSlider, QHBoxLayout, QStatusBar, QMessageBox
import requests
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class StockAnalyzerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Peaks and Troughs Analyzer")
        self.setGeometry(100, 100, 1000, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Header
        header_label = QLabel("Stock Peaks and Troughs Analyzer")
        header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(header_label)

        # Inputs for stock analysis
        self.ticker_input = QLineEdit()
        self.ticker_input.setPlaceholderText("Enter Stock Ticker (e.g., AAPL)")
        main_layout.addWidget(self.ticker_input)

        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDisplayFormat("yyyy-MM-dd")
        main_layout.addWidget(QLabel("Start Date:"))
        main_layout.addWidget(self.start_date_input)

        self.end_date_input = QDateEdit()
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDisplayFormat("yyyy-MM-dd")
        main_layout.addWidget(QLabel("End Date:"))
        main_layout.addWidget(self.end_date_input)

        self.sensitivity_slider = QSlider(Qt.Horizontal)
        self.sensitivity_slider.setRange(1, 10)
        self.sensitivity_slider.setValue(5)
        main_layout.addWidget(QLabel("Sensitivity:"))
        main_layout.addWidget(self.sensitivity_slider)

        # Analyze button
        self.analyze_button = QPushButton("Analyze Stock")
        self.analyze_button.clicked.connect(self.analyze_stock)
        main_layout.addWidget(self.analyze_button)

        # Display results
        self.results_label = QLabel("Analysis Results will appear here.")
        main_layout.addWidget(self.results_label)

        # Add a figure canvas for the plot
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        # Status bar for feedback
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def analyze_stock(self):
        # Get user inputs
        ticker = self.ticker_input.text()
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")
        sensitivity = self.sensitivity_slider.value()

        # Input validation
        if not ticker:
            QMessageBox.warning(self, "Input Error", "Please enter a stock ticker symbol.")
            return

        # Show status message
        self.status_bar.showMessage("Analyzing... Please wait.")

        # Send request to Flask API
        payload = {
            'ticker': ticker,
            'start_date': start_date,
            'end_date': end_date,
            'sensitivity': sensitivity
        }
        try:
            response = requests.post('http://127.0.0.1:5000/api/analyze', json=payload)

            if response.status_code == 200:
                data = response.json()
                self.display_results(data)
                self.plot_stock_data(data)
                self.status_bar.showMessage("Analysis Complete!")
            else:
                QMessageBox.warning(self, "Error", "Failed to analyze stock data.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Error while contacting the server: {e}")
            self.status_bar.clearMessage()

    def display_results(self, data):
        peaks = data['peaks']
        troughs = data['troughs']
        stock_data = data['stock_data']

        # Format the results as a string
        results = f"Peaks: {peaks}\nTroughs: {troughs}\nStock Data:\n"
        for entry in stock_data:
            results += f"{entry['date']}: {entry['price']}\n"

        # Display results in the UI
        self.results_label.setText(results)

    def plot_stock_data(self, data):
        # Clear the figure
        self.figure.clear()

        # Extract stock data
        dates = [entry['date'] for entry in data['stock_data']]
        prices = [entry['price'] for entry in data['stock_data']]
        peaks = data['peaks']
        troughs = data['troughs']

        # Ensure peaks and troughs are within bounds
        peaks = [i for i in peaks if i < len(dates)]
        troughs = [i for i in troughs if i < len(dates)]

        # Create a new subplot
        ax = self.figure.add_subplot(111)

        # Plot the stock data
        ax.plot(dates, prices, label="Stock Price", color='blue')

        # Highlight the peaks and troughs
        ax.scatter([dates[i] for i in peaks], [prices[i] for i in peaks], color='green', label='Peaks', zorder=5)
        ax.scatter([dates[i] for i in troughs], [prices[i] for i in troughs], color='red', label='Troughs', zorder=5)

        ax.set_title("Stock Prices with Peaks and Troughs")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend()

        # Redraw the canvas
        self.canvas.draw()


if __name__ == "__main__":
    # Run PyQt5 UI
    app = QApplication(sys.argv)
    window = StockAnalyzerUI()
    window.show()
    sys.exit(app.exec_())
