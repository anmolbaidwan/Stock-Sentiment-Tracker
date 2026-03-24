from pathlib import Path
import json
from tickerAnalysis import analyze

class TickerData:
    def __init__(self):
        self.directory = Path("tickers")        
        self.directory.mkdir(parents=True, exist_ok=True)
        self.index = self.getIndex()

    def getIndex(self) -> dict: #get a dictionary of all currently stored datasets
        index = {}
        fname = "index.json"
        filepath = self.directory / fname
        try:
            with open(filepath,"r") as file:
                index = json.load(file)
        except:
            with open(filepath,"w") as file:
                json.dump(index, file, indent=4)
        return index

    def storeData(self, dataset, ticker): #store the dataset in a json file
        fname = f"{ticker}_data.json"
        filepath = self.directory / fname
        with open(filepath,"w") as file:
            json.dump(dataset, file, indent=4)
        self.updateIndex(dataset, ticker)

    def updateData(self, newdata, ticker): 
        olddata = self.getData(ticker)
        if not olddata:
            self.storeData(newdata, ticker)
            return newdata
        olddata.update(newdata)
        self.storeData(olddata, ticker)
        return olddata

    def appendData(self, newdata, ticker): #Checks if dataset exists in a json file and appends any new entries from the new dataset if exists
        data = newdata
        if ticker in self.index:
            data = self.getData(ticker)
            for k, v in newdata.items():
                if k not in data:
                    data.update({k:v})
        self.storeData(data, ticker)
        return data
    
    def getData(self, ticker) -> dict: #return the dataset of the corresponding ticker
        dataset = {}
        if ticker in self.index:
            fname = f"{ticker}_data.json"
            filepath = self.directory / fname
            with open(filepath,"r") as file:
                print(f"Fetching data for {ticker} from {self.index[ticker]['from']} ...")
                dataset = json.load(file)
        else:
            print(f"Error no cached data for {ticker}")
            return None
        return dataset
    
    def getDate(self, dataset) -> str: #find most recent date in the dataset
        return max(dataset.keys())

    def findSentiment(self, dataset):
        for date in sorted(dataset.keys(), reverse=True):
            sent = dataset[date]["sentiment"]
            if sent != 0:
                return sent
        return 0
        

    def updateIndex(self, dataset ,ticker):
        date = self.getDate(dataset)
        self.index[ticker] = {'from' : date,
                             'signal' : analyze(dataset),
                             'close' : dataset[date]["price"],
                             'sentiment': self.findSentiment(dataset),
                             'recommendation': dataset[date]["recommendation"]}
        fname = "index.json"
        filepath = self.directory / fname
        with open(filepath,"w") as file:
            json.dump(self.index, file, indent=4)

    def updateIndexAll(self): #runs updateIndex on every ticker stored in index.json
        for k in self.index.keys():
            dataset = self.getData(k)
            self.updateIndex(dataset, k)

    def signalMessage(self, ticker):
        corr = self.index[ticker]["signal"]
        if abs(corr) > 0.2:
            print("Strong signal:", corr)
        elif abs(corr) > 0.1:
            print("Weak Signal:", corr)
        else:
            print("Signal likely noise:", corr)

    def signalString(self, ticker):
        signal = self.index[ticker]["signal"]
        ret = "-"
        if signal > 0.2:
            ret = "Positive"
        elif signal > 0.1:
            ret = "Weakly Positive"
        elif signal <= 0.1 and signal >= -0.1:
            ret = "Likely Noise"
        elif signal < -0.2:
            ret = "Negative"
        elif signal < -0.1:
            ret = "Weakly Negative"
        return ret

    def sentiString(self, ticker):
            senti = self.index[ticker]["sentiment"]
            ret = "-"
            if senti <= -0.35:
                ret = "Bearish"
            elif senti <= -0.15:
                ret = "Somewhat Bearish"
            elif senti < 0.15:
                ret = "Neutral"
            elif senti <= 0.35:
                ret = "Somewhat Bullish"
            else:
                ret = "Bullish"
            return ret
    
    def getPrice(self, ticker):
        return self.index[ticker]["close"]
    
    def getRecScore(self, ticker):
        recScore = self.index[ticker]["recommendation"]
        if recScore is None:
            recScore = -1
        return recScore

    def getRecString(self, ticker):
        score = self.index[ticker]["recommendation"]
        ret = "N/A"
        if score is not None:
            if score > 0.25:
                ret = "BUY"
            elif score < -0.25:
                ret = "SELL"
            else:
                ret = "HOLD"
        return ret

    def printCachedTickers(self):
        print("\n---[Cached Tickers]---")
        indexByDate = sorted(self.index.items(), key=lambda x: x[1]['from'],reverse=True)
        for symbol, data in indexByDate:
            print(f"|{symbol}"+" "*(10-len(symbol))+ f"{data['from']}|")
        print("----------------------")
