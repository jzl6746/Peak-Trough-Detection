from .stock_data import fetch_stock_data_with_date_range
from .cnn_model import CNNModel
import numpy as np

class PeakTroughDetector:
    @staticmethod
    def preprocess_data(df, window_size):
        """
        Preprocess stock data into sliding windows for prediction.
        """
        features = ['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_10']  # Adjust as needed
        windows = []
        for i in range(len(df) - window_size):
            window = df[features].iloc[i:i + window_size].values
            # Normalize each feature in the window
            window = (window - np.mean(window, axis=0)) / np.std(window, axis=0)
            windows.append(window)
        return np.array(windows).reshape(-1, window_size, len(features))

    
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
        df = fetch_stock_data_with_date_range(ticker, start_date, end_date)

        if df is None:
            raise ValueError(f"Failed to fetch data for ticker: {ticker}. Please check the symbol or try again later.")

        df['SMA_10'] = df['Close'].rolling(window=10).mean()
        df['SMA_10'].fillna(method='bfill', inplace=True)  # Backfill with the next valid value

        if df.empty:
            raise ValueError("No data available for the given date range.")

        #Find peaks and troughs
        peaks, troughs = PeakTroughDetector.find_peaks_and_troughs(df, 'cnn_model.h5')

        response_data = {
            'peaks': peaks,
            'troughs': troughs,
            'stock_data': [{"date": str(date.date()), "price": price} for date, price in zip(df.index, df['Close'].values.tolist())]
        }

        return response_data
