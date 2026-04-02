from pathlib import Path
from datetime import datetime
import json

class Profiles:
    profiles = {}
    def __init__(self):
        self.directory = Path("profiles")        
        self.directory.mkdir(parents=True, exist_ok=True)
        self.profiles = self.load_profiles()

    def load_profiles(self):
        profiles = {}
        fname = "profiles.json"
        filepath = self.directory / fname
        try:
            with open(filepath,"r") as file:
                profiles = json.load(file)
        except:
            with open(filepath,"w") as file:
                json.dump(profiles, file, indent=4)
        return profiles

    def add_profile(self, email, username, password):
        if email not in self.profiles:
            self.profiles[email] = {'username':username,
                            'password':password,
                            'tdata':{}} 
            fname =  "profiles.json"
            filepath = self.directory / fname
            with open(filepath,"w") as file:
                json.dump(self.profiles, file, indent=4)

    def update_ticker(self, email, ticker, tdata):
        if email in self.profiles:
            self.profiles[email]['tdata'][ticker] = tdata

    def get_outdated(self): #Returns a dictionary of all profiles with list of outdated tickers and their data
        outdated = {}
        today = datetime.now().strftime('%Y-%m-%d')
        for email in self.profiles.keys():
            tickers = []
            for ticker in self.profiles[email]['tdata'].keys():
                if self.profiles[email]['tdata'][ticker]["from"] < today:
                    tickers.append({ticker : self.profiles[email]['tdata'][ticker]})
            outdated[email] = tickers
        return outdated