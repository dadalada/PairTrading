# This script is used to retrieve data from the RKD API.
# smartRetrieveInterday() and smartRetrieveIntraday() will 
# first check if the data already exists in the local directory and meet the time range.
# If so, it will read the data from the local directory.
# If not, it will retrieve the data from the RKD API and save it to the local directory.
# RetrieveInterday() and RetrieveIntraday() will always retrieve the data from the RKD API.

import os
import sys
import re
import requests
import json
import numpy as np
import pandas as pd


class RKDRetriever:
    def __init__(self):
        # IMPORTANT: Set your Refinitiv API credentials here
        # For security, consider using environment variables instead of hardcoding
        self.username = 'your_email@example.com'  # Replace with your username
        self.password = 'your_password'            # Replace with your password
        self.appid = 'YourApplicationID'           # Replace with your application ID
        self.token = None
        
    @staticmethod
    def doSendRequest(url,requestMsg, headers):
        """
        Send a request to the RKD API.
        """
        result = None
        try:
            result = requests.post(url, data=json.dumps(requestMsg), headers=headers)
            
            if result.status_code != 200:
                print("Request failed with status code:", result.status_code)
    
                if result.status_code == 500: #Failure due to wrong username or password or appid                   
                    print('Error: %s' % (json.dumps(result.json(),
                                                    sort_keys=True, indent=2, separators=(',', ':'))))
                result.raise_for_status()
                
        except requests.exceptions.RequestException as e:
            print('Exception!!!')
            print(e)
            sys.exit(1)
        return result
    
        # Perform authentication
    def CreateAuthorization(self):
        username = self.username
        password = self.password
        appid = self.appid
        
        self.token = None
        # create authentication request URL, message and header
        authenMsg = {'CreateServiceToken_Request_1': {
            'ApplicationID': appid, 'Username': username, 'Password': password}}
        authenURL = 'https://api.rkd.refinitiv.com/api/TokenManagement/TokenManagement.svc/REST/Anonymous/TokenManagement_1/CreateServiceToken_1'
        headers = {'content-type': 'application/json;charset=utf-8'}
        authenResult = RKDRetriever.doSendRequest(authenURL, authenMsg, headers)
        if authenResult and authenResult.status_code == 200:
            print('Authen success')
            # print('response status %s' % (authenResult.status_code))
            # get Token
            self.token = authenResult.json()['CreateServiceToken_Response_1']['Token']
            return self.token
        
        return None
    
    def RetrieveInterday(self, ricName, startTime, endTime, interval = 'DAILY',
                         fields = ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'BID', 'ASK', 'VWAP']):
   
        token = self.token
        
        if not token:
 
            return None
        appid = self.appid
        interdayRequestMsg = {
            'GetInterdayTimeSeries_Request_5': {
                'Field': fields,
                'TrimResponse': False,
                'Symbol': ricName,
                'StartTime': startTime,
                'EndTime': endTime,
                'Interval': interval,
                'MetaField': ['NAME', 'QOS', 'CCY', 'TZ', 'TZOFFSET', 'NAME_LL']
            }
        }
        # construct Time Series Interday URL and header
        interdayURL = 'http://api.rkd.refinitiv.com/api/TimeSeries/TimeSeries.svc/REST/TimeSeries_1/GetInterdayTimeSeries_5'
        headers = {'content-type': 'application/json;charset=utf-8',
                   'X-Trkd-Auth-ApplicationID': appid, 'X-Trkd-Auth-Token': token}
        # send request
        interdayResult = RKDRetriever.doSendRequest(interdayURL, interdayRequestMsg, headers)
        #print('############### Sending Time Series Interday request message to RKD ###############')
        if interdayResult and interdayResult.status_code == 200:
            print('Interday request success')
            json_data = interdayResult.json()
            resp_obj = json_data.get('GetInterdayTimeSeries_Response_5', {})
            if 'Row' in resp_obj:
                interday_data = resp_obj['Row']
                columns = list(interday_data[0].keys()) 
                df = pd.DataFrame(interday_data, columns=columns)
                return df
            else:
                print("No row field, indicating that there may be no data for this period")
                return None
            
            
    def RetrieveIntraday(self, ricName, startTime, endTime, interval = 'MINUTE',
                         fields = ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']):

        token = self.token
        if not token:
            return None
        appid = self.appid
        intradayRequestMsg = {
            'GetIntradayTimeSeries_Request_5': {
                'Field': fields,
                'TrimResponse': False,
                'Symbol': ricName,
                'StartTime': startTime,
                'EndTime': endTime,
                'Interval': interval,
                'MetaField': ['NAME', 'QOS', 'CCY', 'TZ', 'TZOFFSET', 'NAME_LL']
            }
        }
        # construct Time Series Intraday URL and header
        intradayURL = 'http://api.rkd.refinitiv.com/api/TimeSeries/TimeSeries.svc/REST/TimeSeries_1/GetIntradayTimeSeries_5'
        headers = {'content-type': 'application/json;charset=utf-8',
                   'X-Trkd-Auth-ApplicationID': appid, 'X-Trkd-Auth-Token': token}

        intradayResult = RKDRetriever.doSendRequest(intradayURL, intradayRequestMsg, headers)
        if intradayResult and intradayResult.status_code == 200:
            print('Intraday request success')
            json_data = intradayResult.json()
            resp_obj = json_data.get('GetIntradayTimeSeries_Response_5', {})
            if 'Row' in resp_obj:
                intraday_data = resp_obj['Row']
                columns = list(intraday_data[0].keys())  
                df = pd.DataFrame(intraday_data, columns=columns)
                return df
            else:
                print("No row field, indicating that there may be no data for this period")
                return None
    @staticmethod
    def getPath(ricName, suffix):
        ricName = re.sub(r'[^\w\s]', '', ricName)
        # Ensure data directory exists
        if not os.path.isdir('data'):
            os.mkdir('data')
        return 'data/' + ricName + '.' + suffix
    
    @staticmethod
    def readFile(path, path_time):
        data = pd.read_excel(path, index_col = 0)
        startTime = None
        endTime = None
        with open(path_time, 'r') as f:
            startTime = f.readline().strip()
            endTime = f.readline().strip()
        return data, startTime, endTime
    
    @staticmethod
    def saveFile(data, startTime, endTime, path, path_time):
        data.to_excel(path)
        with open(path_time, 'w') as f:
            f.write(startTime + '\n')
            f.write(endTime + '\n')        

    def smartRetrieveInterday(self, ricName, startTime, endTime, reuse = True, interval = 'DAILY',
                         fields = ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'BID', 'ASK', 'VWAP'], save = True):
        data = None
        path = RKDRetriever.getPath(ricName, 'xlsx')
        path_time = RKDRetriever.getPath(ricName, 'txt')
        if reuse and os.path.isfile(path) and os.path.isfile(path_time):
            data, data_start, data_end = RKDRetriever.readFile(path, path_time)
            #print (data['TIMESTAMP'].iloc[0], data['TIMESTAMP'].iloc[-1] >= endTime)
            if data_start <= startTime and data_end >= endTime:
                data = data[data['TIMESTAMP'] >= startTime + '+00:00']
                data = data[data['TIMESTAMP'] <= endTime + '+00:00']
                return data, True
            else:
                print ('Retrieving missing dates for %s .' % (ricName))
                data = self.RetrieveInterday(ricName, startTime, endTime, interval, fields)
                if save:
                    RKDRetriever.saveFile(data, startTime, endTime, path, path_time)
                return data, False
        else:
            print ('Retrieving %s.' % (ricName))
            data = self.RetrieveInterday(ricName, startTime, endTime, interval, fields)
            if save:
                RKDRetriever.saveFile(data, startTime, endTime, path, path_time)
            return data, False
    
    @staticmethod
    def getIntraPath(ricName, date, suffix):
        ricName = re.sub(r'[^\w\s]', '', ricName)
        # Ensure data directory exists
        if not os.path.isdir('data'):
            os.mkdir('data')
        if not os.path.isdir('data/' + ricName):
            os.mkdir('data/' + ricName)
        return 'data/' + ricName + '/' + ricName + '_' + date + '.' + suffix
    
    @staticmethod
    def readIntraFile(path):
        data = pd.read_excel(path, index_col = 0)
        return data
    
    @staticmethod
    def saveIntraFile(data, path):
        data.to_excel(path)

    def smartRetrieveIntraday(self, ricName, date, reuse = True, interval = 'MINUTE',
                         fields = ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'BID', 'ASK', 'VWAP'], save = True):
        data = None
        path = RKDRetriever.getIntraPath(ricName, date, 'xlsx')
        #path_time = RKDRetriever.getPath(ricName, 'txt')
        startTime = date + 'T00:00:00'
        endTime = date + 'T23:59:59'
        if reuse and os.path.isfile(path):
            data = RKDRetriever.readIntraFile(path)
            return data, True
        else:
            print ('Retrieving %s on date %s.' % (ricName, date))
            data = self.RetrieveIntraday(ricName, startTime, endTime, interval, fields)
            if data is None:
                data = pd.DataFrame()
            if save:
                RKDRetriever.saveIntraFile(data, path)
            return data, False


if __name__ == '__main__':

    # Set the working directory to the directory of the script
    print("Current Working Directory:", os.getcwd())
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print("Change it to:", os.getcwd())
    
    retr = RKDRetriever()
    ricName = '.SPX' #change your RIC name
    startTime = '2020-08-20T00:00:00' #change your StartTime
    endTime =   '2020-09-10T23:59:59'  #change your EndTime

    retr.CreateAuthorization()
    #interdayResult = retr.RetrieveInterday(ricName, startTime, endTime)
    #intradayResult = retr.RetrieveIntraday(ricName, startTime, endTime)
    interdayResult = retr.smartRetrieveInterday(ricName, startTime, endTime)
    #intradayResult = retr.smartRetrieveIntraday(ricName, '2024-08-26')
    #intradayResult = retr.smartRetrieveIntraday(ricName, '2024-08-27')
    #intradayResult = retr.smartRetrieveIntraday(ricName, '2024-08-28')
    #intradayResult = retr.smartRetrieveIntraday(ricName, '2024-08-29')
    #intradayResult = retr.smartRetrieveIntraday(ricName, '2024-08-30')
    #intradayResult = retr.smartRetrieveIntraday(ricName, '2024-08-31')
    print (interdayResult)
    #print (intradayResult) 
