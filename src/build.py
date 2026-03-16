from datetime import datetime
from api_client import AlphaVantageClient

def buildDataset(price_dict, sentiment_dict, ticker):
    dataset = []
    dates = sorted(price_dict.keys()) #sort dates 

    for i in range(1, len(dates)): 
        today = dates[i]
        yesterday = dates[i-1]

        today_price = price_dict[today]
        yesterday_price = price_dict[yesterday]

        daily_return = (today_price-yesterday_price)/yesterday_price #get daily return

        sentiment = sentiment_dict.get(today, 0) #if sentiment doesnt exist for that day, set to 0 for now

        dataset.append({ #add a dict with these values
            "date": today,
            "price": today_price,
            "sentiment": sentiment,
            "return": daily_return,
        })

        for i in range(len(dataset) - 1): #afterwards, add a next_return which is just tomorrows return
            dataset[i]["next_return"] = dataset[i + 1]["return"]

        dataset[-1]["next_return"] = None

    return dataset

