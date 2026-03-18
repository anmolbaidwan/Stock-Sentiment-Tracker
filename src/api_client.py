import os
import time
import requests
import yfinance as yf
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta

load_dotenv() #load environment

class AlphaVantageClient:
    def __init__(self):
        self.api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        self.base_url = "https://www.alphavantage.co/query"
        past = datetime.now() + relativedelta(months=-3) #set search date to 3 months ago
        self.today = (datetime.now() + relativedelta(days=-1)).strftime('%Y-%m-%d')
        self.searchDate = past.strftime('%Y%m%d') + "T0000"

        
    def call_api(self, symbol):
        #helper to handle the 1-second delay and the request.
        newparams = {"function": "NEWS_SENTIMENT", "tickers": symbol, "apikey": self.api_key, "time_from": self.searchDate, "limit":1000}
        oldparams = {"function": "NEWS_SENTIMENT", "tickers": symbol, "apikey": self.api_key, "time_from": self.searchDate, "sort": "EARLIEST", "limit":1000}
        r1 = requests.get(self.base_url, params=newparams).json()
        time.sleep(1.1)
        r2 = requests.get(self.base_url, params=oldparams).json()
        if 'Information' in r1 or 'Information' in r2:
            raise RuntimeError("API Limit Reached")
        newfeed = r1['feed']
        oldfeed = r2['feed']
        feed = oldfeed + newfeed
        return feed

    def get_stock_price(self, symbol):
        data = {}
        ticker = yf.Ticker(symbol)
        try:
            priceHistory = ticker.history(period = '3mo', rounding = True)
            priceHistory = priceHistory.reset_index()
            priceHistory['Date'] = priceHistory['Date'].dt.strftime('%Y-%m-%d')
            priceHistory = priceHistory.to_dict('records')
            for record in reversed(priceHistory):
                data[record['Date']] = record['Close']
        except Exception as error:
            raise ValueError("Ticker Not Found")
        return data
    

    def get_recommend_scores(self, symbol): #returns a recommendation score between 1 to -1, 1 = strong buy, 0.5 = buy, 0 = hold, -0.5 = sell, -1 = strong sell
        data = {}
        ticker = yf.Ticker(symbol)
        rec = ticker.get_recommendations()
        rec = rec.to_dict("records")
        for entry in rec:
            score = ((1*entry['strongBuy']) + (0.5*entry['buy']) + (0*entry['hold']) + (-0.5*entry['sell']) + (-1*entry['strongSell'])) / ((entry['strongBuy']) + (entry['buy']) + (entry['hold']) + (entry['sell']) + (entry['strongSell']))
            period = entry["period"]
            if period == '0m':
                date = datetime.now()
            elif period =='-1m':
                date = datetime.now() + relativedelta(months=-1)
            elif period =='-2m':
                date = datetime.now() + relativedelta(months=-2)
            elif period =='-3m':
                date = datetime.now() + relativedelta(months=-3)
            date = date.strftime("%Y-%m")
            data[str(date)] = score
        return data

    def get_sentiment(self, symbol):
        feed = self.call_api(symbol)
        weighted_sentiment = 0
        data = {}
        for article in feed: #for each news article
            date = datetime.strptime(article['time_published'], "%Y%m%dT%H%M%S")
            formatDate = date.strftime("%Y-%m-%d") #get formatted time for consistency
            for t in article['ticker_sentiment']: #for each ticker in the article
                if t['ticker'] == symbol and float(t['relevance_score']) >= 0.3: #if correct ticker and relevant enough
                    weighted_sentiment = float(t['ticker_sentiment_score']) * float(t['relevance_score'])
                    if formatDate not in data: #create a list if it doesnt exist
                        data[formatDate] = [weighted_sentiment]
                    else:
                        data[formatDate].append(weighted_sentiment)
        averages = {}
        for date, values in data.items():
            averages[date] = sum(values) / len(values) #calculate and return averages

        return averages
