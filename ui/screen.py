import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton, QLabel,
    QDateEdit, QSlider, QGridLayout, QStatusBar, QMessageBox
)
from PyQt5.QtCore import Qt
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from backend.peak_trough_dectector import PeakTroughDetector
from chartwidget import ChartWidget  # Import the ChartWidget class

class StockAnalyzerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Peaks and Troughs Analyzer")
        self.setGeometry(100, 100, 1000, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        header_label = QLabel("Stock Peaks and Troughs Analyzer")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #4CAF50; padding: 10px;")
        main_layout.addWidget(header_label)

        input_layout = QGridLayout()
        main_layout.addLayout(input_layout)

        stock_label = QLabel("Select Stock:")
        input_layout.addWidget(stock_label, 0, 0)

        self.stock_dropdown = QComboBox()
        self.stock_dropdown.addItems(["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META"])
        input_layout.addWidget(self.stock_dropdown, 0, 1)

        start_date_label = QLabel("Start Date:")
        input_layout.addWidget(start_date_label, 1, 0)

        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDisplayFormat("yyyy-MM-dd")
        input_layout.addWidget(self.start_date_input, 1, 1)

        end_date_label = QLabel("End Date:")
        input_layout.addWidget(end_date_label, 2, 0)

        self.end_date_input = QDateEdit()
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDisplayFormat("yyyy-MM-dd")
        input_layout.addWidget(self.end_date_input, 2, 1)

        sensitivity_label = QLabel("Sensitivity:")
        input_layout.addWidget(sensitivity_label, 3, 0)

        self.sensitivity_slider = QSlider(Qt.Horizontal)
        self.sensitivity_slider.setRange(1, 10)
        self.sensitivity_slider.setValue(5)
        input_layout.addWidget(self.sensitivity_slider, 3, 1)

        self.analyze_button = QPushButton("Analyze Stock")
        self.analyze_button.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
            border: none;
        """)
        self.analyze_button.clicked.connect(self.analyze_stock)
        main_layout.addWidget(self.analyze_button)

        self.results_label = QLabel("Analysis Results will appear here.")
        self.results_label.setWordWrap(True)
        self.results_label.setStyleSheet("""
            padding: 15px;
            border: 1px solid #ccc;
            background: #f4f4f4;
            font-size: 14px;
        """)
        main_layout.addWidget(self.results_label)

        #Add the ChartWidget to display the plot
        self.chart_widget = ChartWidget()
        main_layout.addWidget(self.chart_widget)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def analyze_stock(self):
        #Get user inputs
        ticker = self.stock_dropdown.currentText()
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")
        sensitivity = self.sensitivity_slider.value()

        try:
            result = PeakTroughDetector.analyze_stock_from_ui(ticker, start_date, end_date, sensitivity)
            
            # Extract dates and prices
            dates = [entry['date'] for entry in result['stock_data']]
            prices = [entry['price'] for entry in result['stock_data']]
            
            self.display_results(result)
            self.chart_widget.plot_data(dates, prices, result['peaks'], result['troughs'])  # Use the new chart widget
            self.status_bar.showMessage("Analysis Complete!")
        except ValueError as e:
            QMessageBox.critical(self, "Analysis Error", str(e))
            self.status_bar.clearMessage()

    def display_results(self, data):
        peaks = data['peaks']
        troughs = data['troughs']
        stock_data = data['stock_data']

        results = f"Peaks: {peaks}\nTroughs: {troughs}\nStock Data:\n"
        for entry in stock_data:
            results += f"{entry['date']}: {entry['price']}\n"

        self.results_label.setText(results)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockAnalyzerUI()
    window.show()
    sys.exit(app.exec_())
