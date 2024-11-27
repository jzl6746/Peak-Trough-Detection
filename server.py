from flask import Flask, jsonify, request
from backend.stock_data import fetch_stock_data
import pandas as pd

app = Flask(__name__)


# Helper function to calculate peaks and troughs
def find_peaks_and_troughs(prices, sensitivity=5):
    peaks = []
    troughs = []
    for i in range(1, len(prices) - 1):
        if prices[i] > prices[i - 1] and prices[i] > prices[i + 1]:
            peaks.append(i)
        elif prices[i] < prices[i - 1] and prices[i] < prices[i + 1]:
            troughs.append(i)
    return peaks, troughs


@app.route('/api/analyze', methods=['POST'])
def analyze_stock():
    data = request.get_json()
    ticker = data.get('ticker', 'AAPL')
    start_date = data.get('start_date', '2024-01-01')
    end_date = data.get('end_date', '2024-11-01')
    sensitivity = data.get('sensitivity', 5)

    # Fetch stock data from Alpha Vantage
    df = fetch_stock_data(ticker)

    if df is None:
        return jsonify({"error": "Failed to fetch stock data"}), 500

    # Filter data within the date range
    df = df[(df.index >= start_date) & (df.index <= end_date)]

    # Extract the "Close" prices
    close_prices = df['Close'].values.tolist()

    # Find peaks and troughs
    peaks, troughs = find_peaks_and_troughs(close_prices, sensitivity)

    # Prepare the response data
    response_data = {
        'peaks': peaks,
        'troughs': troughs,
        'stock_data': [{"date": str(date), "price": price} for date, price in zip(df.index, close_prices)]
    }

    return jsonify(response_data)


def run_flask():
    app.run(debug=True, use_reloader=False)


if __name__ == "__main__":
    run_flask()
