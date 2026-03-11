import sys
import pprint
from api_client import AlphaVantageClient

def run():
    print("--- Stock Sentiment & Valuation Tracker ---")
    ticker = input("Enter a stock ticker (e.g., AAPL): ").upper()
    
    client = AlphaVantageClient()
    
    print(f"Fetching data for {ticker}...")
    price_data = client.get_stock_price(ticker)
    sentiment_data = client.get_sentiment(ticker)
    
    print("\n[Results]")
    print(f"Ticker: {ticker}")
    print("Data received.")
    print("Price Data")
    pprint.pprint(price_data)
    print("Sentiment Data")
    pprint.pprint(sentiment_data)

if __name__ == "__main__":
    run()