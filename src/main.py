import sys
import pprint
from api_client import AlphaVantageClient
from build import buildDataset

def run():
    print("--- Stock Sentiment & Valuation Tracker ---")
    try:
        ticker = input("Enter a stock ticker (e.g., AAPL): ").upper()
        
        client = AlphaVantageClient()
        
        print(f"Fetching data for {ticker}...")
        price_data = client.get_stock_price(ticker)
        sentiment_data = client.get_sentiment(ticker)
    except Exception as error:
        print("Error:", error)
        return
    
    print("\n[Results]")
    print(f"Ticker: {ticker}")
    print("Data received.")
    dataset = buildDataset(price_data, sentiment_data, ticker)
    pprint.pprint(dataset)

if __name__ == "__main__":
    run()