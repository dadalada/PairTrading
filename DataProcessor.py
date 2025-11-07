import numpy as np
import pandas as pd
from RKDRetriever import *

class DataProcessor:
    def __init__(self, start_data, end_data):
        self.start_data = start_data
        self.end_data = end_data
        
    def get_data(self):
        
        retr = RKDRetriever()
        retr.CreateAuthorization()
        
        tickers = pd.read_csv('sp500_tickers_RIC.csv', header=None)
        tickers.columns = ['tickers','RIC']
        for ric in tickers['RIC']:    
            retr.smartRetrieveInterday(ric, self.start_data, self.end_data)
    
    def get_index(self):
        retr = RKDRetriever()
        retr.CreateAuthorization()
        
        data,_ = retr.smartRetrieveInterday('.SPX', self.start_data, self.end_data)
        ts = pd.to_datetime(data['TIMESTAMP'], utc=True)
        idx = pd.DatetimeIndex(ts).tz_convert(None).normalize()
        data.index = idx
        data = data.drop(columns=['TIMESTAMP'])
        data = data.dropna(axis=0)
        
        returns    = data['CLOSE'].pct_change().dropna() * 100
        volatility = returns.rolling(21).std()
        df = pd.concat([data['CLOSE'], returns, volatility], axis=1)
        df.columns = pd.MultiIndex.from_product(
            [['SPX'], ['close', 'returns', 'volatility']]
        )
        df = df.sort_index(axis=1, level=[0,1])
        
        return df
    
    def get_Stocks(self):
        retr = RKDRetriever()
        retr.CreateAuthorization()
        tickers = pd.read_csv('sp500_tickers_RIC.csv', header=None)
        tickers.columns = ['tickers','RIC']
        Stocks_list = []
        for ric in tickers['RIC']:    
            data,_ = retr.smartRetrieveInterday(ric, self.start_data, self.end_data)
            
            # Convert TIMESTAMP to datetime and set as index
            # Drop TIMESTAMP column and any rows with NaN values
            ts = pd.to_datetime(data['TIMESTAMP'], utc=True)
            idx = pd.DatetimeIndex(ts).tz_convert(None).normalize()
            data.index = idx
            data = data.drop(columns=['TIMESTAMP'])
            data = data.dropna(axis=0)
            
            if 'OPEN' not in data.columns or 'HIGH' not in data.columns or 'LOW' not in data.columns or 'CLOSE' not in data.columns or 'VOLUME' not in data.columns or 'VWAP' not in data.columns:
                print(f"Skip {ric}: Lack of columns")
                continue
            data.columns = pd.MultiIndex.from_product([[ric], data.columns])
            Stocks_list.append(data)
            
        Stocks = pd.concat(Stocks_list, axis=1)
        Stocks = Stocks.sort_index(axis=1, level=[0,1])
        #features = features.iloc[1:]
        #features = features.interpolate(method='linear',axis=0,limit=3,limit_direction='both')
        #features = features.dropna(axis=1, how='any')
        
        return Stocks    
    
