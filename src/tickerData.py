from pathlib import Path
import json

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
            return
        for date, d in newdata.items():
            olddata[date] = newdata[d]
        self.storeData(olddata, ticker)

    
    def getData(self, ticker) -> list: #return the dataset of the corresponding ticker
        dataset = []
        if ticker in self.index:
            fname = f"{ticker}_data.json"
            filepath = self.directory / fname
            with open(filepath,"r") as file:
                print(f"Fetching data for {ticker} from {self.index[ticker]} ...")
                dataset = json.load(file)
        else:
            print(f"Error no cached data for {ticker}")
            return None
        return dataset
    
    def getDate(self, dataset) -> str: #find most recent date in the dataset
        return dataset[len(dataset)-1]["date"]

    def updateIndex(self, dataset ,ticker):
        self.index[ticker] = self.getDate(dataset)
        fname = "index.json"
        filepath = self.directory / fname
        with open(filepath,"w") as file:
            json.dump(self.index, file, indent=4)
