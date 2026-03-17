import sys
from api_client import AlphaVantageClient
from build import buildDataset
from tickerData import TickerData

def run():
    print("--- Stock Sentiment & Valuation Tracker ---")
    tickerData = TickerData()
    client = AlphaVantageClient()
    # dataset = {}
    loop = ""
    while(loop != "N"):
        ticker = input("Enter a stock ticker (e.g., AAPL): ").upper()
        fetchNew = input("Would you like to update data for this ticker? (Y/N): ").upper()
        if fetchNew == "Y":
            try:
                print(f"Fetching data for {ticker}...")
                price_data = client.get_stock_price(ticker)
                sentiment_data = client.get_sentiment(ticker)
                build = buildDataset(price_data, sentiment_data, ticker)
                upOrAppend = input("Replace or Append entries to JSON? (R/A):").upper()
                if upOrAppend == 'R':
                    print("Replacing entries in JSON...")
                    tickerData.updateData(build, ticker)
                else:
                    print("Appending entries to JSON...")
                    tickerData.appendData(build, ticker)
            except Exception as error:
                print("Error:", error)
                return
        else:
            tickerData.getData(ticker)
        print("\n[Results]")
        print(f"Ticker: {ticker}")
        print("Data received.")
        tickerData.signalMessage(ticker)
        loop = input("Would you like to process new data? (Y/N)").upper()

if __name__ == "__main__":
    run()