import requests
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

API_KEY = "BBCT3KLZKHATW4RP"

""" 
Joe's Key:  BBCT3KLZKHATW4RP
Nate's Key: 535ANFU20KLL61KS
Chase's Key: 7IWMRGGSNYTQFAQB'
"""
BASE_URL = "https://www.alphavantage.co/query"

def fetch_stock_data_with_date_range(ticker, start_date, end_date):
    """
    Fetch stock data for a given ticker and filter it for the specified date range.
    
    Args:
        ticker (str): Stock ticker symbol.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        api_key (str): Your Alpha Vantage API key.
        
    Returns:
        pd.DataFrame: Filtered stock data within the date range.
    """
    # Initialize the TimeSeries object
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    
    # Fetch full historical data
    try:
        data, meta_data = ts.get_daily(symbol=ticker, outputsize='full')
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None
    
    # Convert index to datetime
    data.index = pd.to_datetime(data.index)
    
    data.sort_index(inplace=True)
    data.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    }, inplace=True)
    
    # Filter data for the specified date range
    filtered_data = data[(data.index >= start_date) & (data.index <= end_date)]
    
    return filtered_data

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
        df = pd.DataFrame.from_dict(time_series, orient="index")
        df = df.apply(pd.to_numeric, errors="coerce")  # Convert all columns to numeric
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)

        df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        }, inplace=True)

        print(df.head())
        return df
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None
