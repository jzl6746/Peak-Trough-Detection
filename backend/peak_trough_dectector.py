from .stock_data import fetch_stock_data
from .cnn_model import CNNModel
import numpy as np

class PeakTroughDetector:
    @staticmethod
    def preprocess_data(prices, window_size):
        """
        Preprocess stock prices into sliding windows for prediction.
        """
        windows = []
        for i in range(len(prices) - window_size):
            window = prices[i:i + window_size]
            # Normalize the window
            window = (window - np.mean(window)) / np.std(window)
            windows.append(window)
        return np.array(windows).reshape(-1, window_size, 1)
    
    @staticmethod
    def find_peaks_and_troughs(prices, model_path, window_size=50):
        """
        Detect peaks and troughs using the trained CNN model.
        """
        # Load the trained model
        if not model_path:
            raise ValueError("Model path is required.")
        model = CNNModel.load_trained_model(model_path)

        # Preprocess the data
        preprocessed_data = PeakTroughDetector.preprocess_data(prices, window_size)
        print("Preprocessed Data Shape:", preprocessed_data.shape)

        # Predict using the CNN
        predictions = model.predict(preprocessed_data)
        print("Raw Predictions:", predictions[:5])  # Debug: first 5 raw predictions
        predictions = np.argmax(predictions, axis=1)
        print("Class Predictions:", predictions[:20])  # Debug: first 20 class predictions

        # Map predictions to indices
        peaks = [i for i, pred in enumerate(predictions) if pred == 1]  # Peak
        troughs = [i for i, pred in enumerate(predictions) if pred == 2]  # Trough

        return peaks, troughs

    @staticmethod
    def analyze_stock_from_ui(ticker, start_date, end_date, sensitivity=5):
        """
        Analyze stock data
        """
        df = fetch_stock_data(ticker)

        if df is None:
            raise ValueError(f"Failed to fetch data for ticker: {ticker}. Please check the symbol or try again later.")

        df = df[(df.index >= start_date) & (df.index <= end_date)]

        if df.empty:
            raise ValueError("No data available for the given date range.")

        close_prices = df['Close'].values.tolist()

        #Find peaks and troughs
        peaks, troughs = PeakTroughDetector.find_peaks_and_troughs(close_prices, 'cnn_model.h5')

        response_data = {
            'peaks': peaks,
            'troughs': troughs,
            'stock_data': [{"date": str(date.date()), "price": price} for date, price in zip(df.index, close_prices)]
        }

        return response_data
