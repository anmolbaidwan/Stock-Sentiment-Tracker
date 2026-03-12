import os
import time
import requests
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta

load_dotenv()

class AlphaVantageClient:
    def __init__(self):
        self.api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        self.base_url = "https://www.alphavantage.co/query"
        past = datetime.now() + relativedelta(months=-6)
        self.searchDate = past.strftime('%Y%m%d') + "T0000"

    def call_api(self, params):
        #helper to handle the 1-second delay and the request.
        response = requests.get(self.base_url, params=params)
        time.sleep(1.1) 
        return response.json()

    def get_stock_price(self, symbol):
        params = {"function": "TIME_SERIES_DAILY", "symbol": symbol, "outputsize":"compact", "apikey": self.api_key}
        return self.call_api(params)

    def get_sentiment(self, symbol):
        params = {"function": "NEWS_SENTIMENT", "tickers": symbol, "apikey": self.api_key, "time_from": self.searchDate, "limit":1000}
        return self.call_api(params)