import sys
import pprint
from api_client import AlphaVantageClient
from build import buildDataset
from tickerData import TickerData
from linearModel import graph

def run():
    print("--- Stock Sentiment & Valuation Tracker ---")
    data = TickerData()
    ticker = input("Enter a stock ticker (e.g., AAPL): ").upper()
    fetchNew = input("Would you like to update data for this ticker? (y/n): ").upper()
    dataset = []
    if fetchNew == "Y":
        try:
            client = AlphaVantageClient()
            print(f"Fetching data for {ticker}...")
            price_data = client.get_stock_price(ticker)
            sentiment_data = client.get_sentiment(ticker)
            dataset = buildDataset(price_data, sentiment_data, ticker)
            data.storeData(dataset, ticker)
        except Exception as error:
            print("Error:", error)
            return
    else:
        dataset = data.getData(ticker)
    print("\n[Results]")
    print(f"Ticker: {ticker}")
    print("Data received.")
    pprint.pprint(dataset)
    graph(dataset)
if __name__ == "__main__":
    run()