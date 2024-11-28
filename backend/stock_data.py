import requests
import pandas as pd

API_KEY = "535ANFU20KLL61KS"

""" 
Joe's Key:  BBCT3KLZKHATW4RP
Nate's Key: 535ANFU20KLL61KS
"""
BASE_URL = "https://www.alphavantage.co/query"

def fetch_stock_data(symbol, interval="TIME_SERIES_DAILY"):
    """
    Fetch stock data from Alpha Vantage API.
    :param symbol: Stock ticker symbol (e.g., "IBM").
    :param interval: Data interval ('TIME_SERIES_DAILY', 'TIME_SERIES_WEEKLY', etc.).
    :return: Pandas DataFrame of stock data.
    """
    try:
        params = {
            "function": interval,
            "symbol": symbol,
            "apikey": API_KEY
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        print(f"Raw response from API for {symbol}: {data}")

        if "Error Message" in data:
            raise ValueError(f"API Error: {data['Error Message']}")

        if "Note" in data:
            raise ValueError("API request limit reached. Please try again later.")

        if "Time Series (Daily)" in data:
            time_series = data["Time Series (Daily)"]
        elif "Weekly Time Series" in data:
            time_series = data["Weekly Time Series"]
        elif "Monthly Time Series" in data:
            time_series = data["Monthly Time Series"]
        else:
            raise ValueError("Invalid or unsupported interval provided.")

        #Convert time series data to a pandas DataFrame
        df = pd.DataFrame.from_dict(time_series, orient="index", dtype=float)
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)

        df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        }, inplace=True)

        return df
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None
