from backend.stock_data import fetch_stock_data

class PeakTroughDetector:
    @staticmethod
    def find_peaks_and_troughs(prices, sensitivity=5):
        """
        Helper function to calculate peaks and troughs.
        """
        peaks = []
        troughs = []
        for i in range(1, len(prices) - 1):
            if prices[i] > prices[i - 1] and prices[i] > prices[i + 1]:
                peaks.append(i)
            elif prices[i] < prices[i - 1] and prices[i] < prices[i + 1]:
                troughs.append(i)
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
        peaks, troughs = PeakTroughDetector.find_peaks_and_troughs(close_prices, sensitivity)

        response_data = {
            'peaks': peaks,
            'troughs': troughs,
            'stock_data': [{"date": str(date.date()), "price": price} for date, price in zip(df.index, close_prices)]
        }

        return response_data
