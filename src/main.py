import sys
from api_client import AlphaVantageClient
from build import buildDataset
from tickerData import TickerData
from linearModel import graph

def run():
    print("--- Stock Sentiment & Valuation Tracker ---")
    data = TickerData()
    dataset = {}

    #while True:
    #    ticker = input("Enter a stock ticker (e.g., AAPL): ").upper()
    #    dataset = data.getData(ticker)
    #    graph(dataset)
    loop = ""
    while(loop != "N"):
        ticker = input("Enter a stock ticker (e.g., AAPL): ").upper()
        fetchNew = input("Would you like to update data for this ticker? (y/n): ").upper()
        if fetchNew == "Y":
            try:
                client = AlphaVantageClient()
                print(f"Fetching data for {ticker}...")
                price_data = client.get_stock_price(ticker)
                sentiment_data = client.get_sentiment(ticker)
                dataset = buildDataset(price_data, sentiment_data, ticker)
                data.updateData(dataset, ticker)
            except Exception as error:
                print("Error:", error)
                return
        dataset = data.getData(ticker)
        print("\n[Results]")
        print(f"Ticker: {ticker}")
        print("Data received.")
        graph(dataset)
        loop = input("Would you like to process new data? (y/n)").upper()
if __name__ == "__main__":
    run()