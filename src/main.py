import sys
from api_client import AlphaVantageClient
from build import buildDataset
from tickerData import TickerData

def run(ticker):
    tickerData = TickerData()
    client = AlphaVantageClient()
    index = tickerData.index

    try:
        if ticker in index:
            dataset = tickerData.getData(ticker)
        else:
            price_data = client.get_stock_price(ticker)
            sentiment_data = client.get_sentiment(ticker)
            build = buildDataset(price_data, sentiment_data, ticker)
            dataset = tickerData.appendData(build, ticker)
        return {
            "ticker": ticker,
            "message": tickerData.signalString(ticker),
            "sentiment": tickerData.sentiString(ticker),
            "price": tickerData.getPrice(ticker)
        }
    except Exception as error:
        return {"error": str(error)}

if __name__ == "__main__":
    print("--- Stock Sentiment & Valuation Tracker ---")
    tickerData = TickerData()
    client = AlphaVantageClient()
    tickerData.printCachedTickers()
    loop = ""
    while(loop != "N"):
        ticker = input("Enter a stock ticker (e.g., AAPL): ").upper()
        fetchNew = input("Would you like to update data for this ticker? (Y/N): ").upper()
        if fetchNew == "Y":
            try:
                print(f"Fetching data for {ticker}...")
                price_data = client.get_stock_price(ticker)
                sentiment_data = client.get_sentiment(ticker)
                recommendation_data = client.get_recommend_scores(ticker)
                build = buildDataset(price_data, sentiment_data, recommendation_data, ticker)
                upOrAppend = input("Replace or Append entries to JSON? (R/A):").upper()
                if upOrAppend == 'R':
                    print("Replacing entries in JSON...")
                    tickerData.updateData(build, ticker)
                else:
                    print("Appending entries to JSON...")
                    tickerData.appendData(build, ticker)
            except Exception as error:
                print("Error:", error)
        else:
            tickerData.getData(ticker)
        print("\n[Results]")
        print(f"Ticker: {ticker}")
        print("Data received.")
        tickerData.signalMessage(ticker)
        loop = input("Would you like to process new data? (Y/N)").upper()