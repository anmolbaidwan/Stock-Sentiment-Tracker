import sys
from apscheduler.schedulers.background import BackgroundScheduler
from api_client import AlphaVantageClient
from build import buildDataset
from tickerData import TickerData
from profiles import Profiles
from alert import process_alerts
from datetime import datetime


profiles = Profiles()
tickerData = TickerData()
client = AlphaVantageClient()

def get_pending_alerts(outdated):
    indexData = tickerData.index
    alerts = {}
    for email in outdated:
        alerts[email] = []
        for ticker in outdated[email]:
            date = outdated[email][ticker]['from']
            alertData = {'ticker':ticker,
                         'date':date,
                        'close':0,
                        'sent':0,
                        'rec':0}
            validAlert = False
            oldclose = outdated[email][ticker]['close']
            oldsent = outdated[email][ticker]['sentiment']
            oldrec = outdated[email][ticker]['recommendation']

            newclose = indexData[ticker]['close']
            newsent = indexData[ticker]['sentiment']
            newrec = indexData[ticker]['recommendation']

            dclose = (oldclose-newclose)/abs(oldclose)
            dsent = (oldsent-newsent)/abs(oldsent)
            drec = 0
            if oldrec and newrec:
                drec = (oldrec-newrec)/abs(oldrec)

            if(dclose > 0.10):
                alertData['close'] = round(dclose,2)
                validAlert = True
            elif(dclose < -0.10):
                alertData['close'] = round(dclose,2)
                validAlert = True

            if(dsent > 0.10):
                alertData['sent'] = round(dsent,2)
                validAlert = True
            elif(dsent < -0.10):
                alertData['sent'] = round(dsent,2)
                validAlert = True

            if(drec > 0.10):
                alertData['rec'] = round(drec,2)
                validAlert = True
            elif(drec < -0.10):
                alertData['rec'] = round(drec,2)
                validAlert = True

            if validAlert:
                alerts[email].append(alertData)
        if alerts[email] == []:
            alerts.pop(email)
    return alerts

def update_tracked_ticker(outdated): #updates track
    tickers = []
    index = tickerData.index
    today = datetime.now().strftime('%Y-%m-%d')
    for user in outdated:
        for ticker in outdated[user]:
            if ticker not in tickers:
                tickers.append(ticker)           
    for ticker in tickers:
        if index[ticker]['from'] < today:
            update_ticker(ticker)

def update_alerted_users(pendingAlerts):
    for email in pendingAlerts:
        for alert in pendingAlerts[email]:
            ticker = alert['ticker']
            tdata = tickerData.getIndexData(ticker)
            profiles.update_ticker(email, ticker, tdata)

def daily_update():
    outdated = profiles.get_outdated()
    update_tracked_ticker(outdated)
    pendingAlerts = get_pending_alerts(outdated)
    update_alerted_users(pendingAlerts)
    process_alerts(pendingAlerts)

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(daily_update, trigger='cron', hour='13', minute=0, id='daily_update',replace_existing=True)
# scheduler.add_job(daily_update, 'interval', seconds = 10,  id='daily_update', replace_existing=True)
scheduler.start()

def update_ticker(ticker):
    if ticker:
        price_data = client.get_stock_price(ticker)
        sentiment_data = client.get_sentiment(ticker)
        recommendation_data = client.get_recommend_scores(ticker)
        build = buildDataset(price_data, sentiment_data, recommendation_data, ticker)
        tickerData.appendData(build, ticker)

def run(ticker):
    index = tickerData.index
    try:
        if ticker in index and client.yesterday <= index[ticker]["from"]:
            dataset = tickerData.getData(ticker) #doesn't do anything?
        else:
            update_ticker(ticker)
        chart = tickerData.getChart(ticker, dataset=tickerData.getData(ticker))
        return {
            "ticker": ticker,
            "message": tickerData.signalString(ticker),
            "sentiment": tickerData.sentiString(ticker),
            "price": tickerData.getPrice(ticker),
            "bar": ((tickerData.getRecScore(ticker) + 1)/2)*100,
            "recommendation": tickerData.getRecString(ticker),
            "chart": chart
        }
    except Exception as error:
        return {"error": str(error)}

def signup(email, username, password):
    profiles.add_profile(email, username, password)

def get_users():
    return profiles.get_users()

def get_email(username): #very jank please remove this later
    return profiles.get_email(username)

def get_tracked(email):
    return profiles.get_tracked(email)

def track_ticker(email, ticker):
    tdata = tickerData.getIndexData(ticker)
    profiles.update_ticker(email, ticker, tdata)

def untrack_ticker(email, ticker):
    profiles.remove_ticker(email, ticker)

def edit_username(email, username):
    profiles.edit_username(email, username)

# ONLY FOR CLI VERSION -- DEPRICATED
if __name__ == "__main__":
    print("--- Stock Sentiment & Valuation Tracker ---")
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
        print(f"expert recommendation: {tickerData.getRecString(ticker)}")
        barwidth = 30
        bar = int(((tickerData.getRecScore(ticker) + 1)/2)*barwidth)
        print(("["+"■"*bar)+("□"*(barwidth-bar))+("]"))
        print(f"Closing Price: ${tickerData.getPrice(ticker)}")
        print(f"Overall Market Sentiment: {tickerData.sentiString(ticker)}")
        print(f"Correlation between price and sentiment: {tickerData.signalString(ticker)}")
        loop = input("Would you like to process new data? (Y/N)").upper()