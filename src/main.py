import sys
from api_client import AlphaVantageClient
from build import buildDataset
from tickerData import TickerData
from linearModel import graph

def run():
    print("--- Stock Sentiment & Valuation Tracker ---")
    data = TickerData()
    client = AlphaVantageClient()
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
                print(f"Fetching data for {ticker}...")
                price_data = client.get_stock_price(ticker)
                sentiment_data = client.get_sentiment(ticker)
                build = buildDataset(price_data, sentiment_data, ticker)
                upOrAppend = input("Replace or Append entries to JSON? (U/R):").upper()
                if upOrAppend == 'R':
                    print("Replacing entries in JSON...")
                    dataset = data.updateData(build, ticker)
                else:
                    print("Appending entries to JSON...")
                    dataset = data.appendData(build, ticker)
            except Exception as error:
                print("Error:", error)
                return
        else:
            dataset = data.getData(ticker)
            if not dataset:
                print(f"Error no cached data for {ticker}")

        print("\n[Results]")
        print(f"Ticker: {ticker}")
        print("Data received.")
        graph(dataset)
        loop = input("Would you like to process new data? (y/n)").upper()
        
if __name__ == "__main__":
    run()