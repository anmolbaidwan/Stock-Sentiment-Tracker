from datetime import datetime
from api_client import AlphaVantageClient

def buildDataset(price_dict, sentiment_dict, ticker):
    dataset = {}
    dates = sorted(price_dict.keys()) #sort dates 

    for i in range(1, len(dates)): 
        today = dates[i]
        yesterday = dates[i-1]

        today_price = price_dict[today]
        yesterday_price = price_dict[yesterday]

        daily_return = (today_price-yesterday_price)/yesterday_price #get daily return

        sentiment = sentiment_dict.get(yesterday, 0) #if sentiment doesnt exist for that day, set to 0 for now

        dataset[today] = { #add a dict with these values
            "price": today_price,
            "sentiment": sentiment,
            "return": daily_return,
        }

    dates = list(dataset.keys())
    for i in range(len(dates)-1): #afterwards, add a next_return which is just tomorrows return
        today = dates[i]
        tomorrow = dates[i+1]
        dataset[today]["next_return"] = dataset[tomorrow]["return"]
    last = dates[-1]
    dataset[last]["next_return"] = None
    return dataset

