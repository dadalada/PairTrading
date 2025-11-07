import pandas as pd
import numpy as np
import ta


class FeatureEngineering():
    
    # Calculates the technical indicators and adds them to the dataframe
    # Filling the NaN values with 0
    # Using the ta library, ta stands for technical analysis
    
    def __init__(self):
        self.data = None
        self.derivatives = None
        
    def setParams(self, data, derivatives):
        self.data = data
        self.derivatives = derivatives

    def RSI(self):
        if 'RSI' in self.derivatives:
            self.data['RSI'] = ta.momentum.rsi(self.data['CLOSE'], fillna = True)
            return True
        return False
    
    def WilliamsR(self):
        if 'WilliamsR' in self.derivatives:
            self.data['WilliamsR'] = ta.momentum.williams_r(high = self.data['HIGH'], 
                            low = self.data['LOW'], close = self.data['CLOSE'], fillna = True)
            return True
        return False
    
    def PPO(self):
        if 'PPO' in self.derivatives:
            self.data['PPO'] = ta.momentum.ppo(close = self.data['CLOSE'], fillna = True)
            return True
        return False
    
    def CMF(self):
        if 'CMF' in self.derivatives:
            self.data['CMF'] = ta.volume.chaikin_money_flow(high = self.data['HIGH'], low = self.data['LOW'], 
                            close = self.data['CLOSE'], volume = self.data['VOLUME'], fillna = True)
            return True
        return False
    
    def FI(self):
        if 'FI' in self.derivatives:
            self.data['FI'] = ta.volume.force_index(close = self.data['CLOSE'], 
                                    volume = self.data['VOLUME'], fillna = True)
            return True
        return False
    
    def VPT(self):
        if 'VPT' in self.derivatives:
            self.data['VPT'] = ta.volume.volume_price_trend(close = self.data['CLOSE'], 
                                    volume = self.data['VOLUME'], fillna = True)
            return True
        return False
    
    def ArronUp(self):
        if 'ArronUp' in self.derivatives:
            self.data['ArronUp'] = ta.trend.aroon_up(close = self.data['CLOSE'], 
                                    fillna = True)
            return True
        return False
    
    def ArronDown(self):
        if 'ArronDown' in self.derivatives:
            self.data['ArronDown'] = ta.trend.aroon_down(close = self.data['CLOSE'], 
                                    fillna = True)
            return True
        return False
    
    def CCI(self):
        if 'CCI' in self.derivatives:
            self.data['CCI'] = ta.trend.cci(high = self.data['HIGH'], low = self.data['LOW'], 
                            close = self.data['CLOSE'], fillna = True)
            return True
        return False
    
    def MACD(self):
        if 'MACD' in self.derivatives:
            self.data['MACD'] = ta.trend.macd(close = self.data['CLOSE'], fillna = True)
            return True
        return False
    
    def LogVol(self):
        if 'LogVol' in self.derivatives:
            self.data['LogVol'] = np.log(self.data['VOLUME'])
            return True
        return False
    
    
    def Close_High(self):
        if 'Close_High' in self.derivatives:
            self.data['Close_High'] = (self.data['CLOSE'] - self.data['HIGH']) / self.data['HIGH']
            return True
        return False
    
    def Percent_Change(self):
        if 'Percent_Change' in self.derivatives:
            self.data['Percent_Change'] = self.data['CLOSE'].pct_change().fillna(0)
            return True
        return False
    
    def Range(self):
        if 'Range' in self.derivatives:
            self.data['Range'] = np.log(self.data['HIGH'] / self.data['LOW'])
            return True
        return False
    
    def Sigma_parkinson(self):
        if 'Sigma_parkinson' in self.derivatives:
            self.data['Sigma_parkinson'] = self.data['Range'] ** 2 / (4 * np.log(2))
            return True
        return False
    
    def Vol_R20(self):
        if 'Vol_R20' in self.derivatives:
            self.data['Vol_R20'] = self.data['VOLUME']/self.data['VOLUME'].rolling(20).mean()
            return True
        return False
    
    def Illiquidity(self):
        if 'Illiquidity' in self.derivatives:
            self.data['Illiquidity'] = self.data['Percent_Change'].abs() / (self.data['VOLUME'] * self.data['CLOSE'])
            return True
        return False
    
    
    
    def process(self):
        self.RSI()
        self.WilliamsR()
        self.PPO()
        self.CMF()
        self.FI()
        self.VPT()
        self.ArronUp()
        self.ArronDown()
        self.CCI()
        self.MACD()
        self.LogVol()
        self.Close_High()
        self.Percent_Change()
        self.Range()
        self.Sigma_parkinson()
        self.Vol_R20()
        self.Illiquidity()
        
    def all_ta(self):
        self.RSI()
        self.WilliamsR()
        self.PPO()
        self.CMF()
        self.FI()
        self.VPT()
        self.ArronUp()
        self.ArronDown()
        self.CCI()
        self.MACD()
        self.LogVol()
        self.Close_High()
        self.Percent_Change()
        self.Range()
        self.Sigma_parkinson()
        self.Vol_R20()
        self.Illiquidity()
    