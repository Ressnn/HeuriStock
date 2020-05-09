# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 20:47:44 2020

@author: Pranav Devarinti
"""
# In[]
import numpy as np
import csv
import pandas_datareader.data as web
from pytrends.request import TrendReq
from sklearn.preprocessing import StandardScaler
import pandas as pd
import pytrends
# All of out imports 
#we use fix_yahoo_finance to pull data and pytrends to get the trend data
#Trend Data Soruce: Google Trends
#Stock Data Source: Yahoo Finance
# In[]
# A simple class to get both trend data and Panel Data easily
class DataAcsessor():
    #Sets up the PyTrends Requester class to get trend data
    def __init__(self):
        self.PytrendsRequester = TrendReq(hl='en-US', tz=360)
        
    #Gets Stock Data   
    def GetPanelData(self,tickers,start_date,end_date): 
        return web.get_data_yahoo(tickers, start_date, end_date)
    
    #Gets Trend Data
    def GetTrendData(self,tickers,start_date,end_date):
        total_dates = start_date + ' ' + end_date
        self.PytrendsRequester.build_payload(tickers,cat=0, timeframe=total_dates, geo='', gprop='')
        return self.PytrendsRequester.interest_over_time()
    
    
class RawDataHandler():
    #Constructs RawDataHandler nothing much here
    def __init__(self):
        #DataStream sets up a Raw Data Stream that allows us to easily acsess raw data
        self.DataStream = DataAcsessor()
        #A Standardizing Scaler used later
        self.Scaler = StandardScaler()
        
    #Gets the single standarized value of a stock
    def GetSingleStandarized(self,ticker,start_date,end_date):
        Concat_Data = self.GetMergeDataOne(ticker,start_date,end_date)
        Standardized = self.StandardizeData(Concat_Data[0])
        Dates = Concat_Data[1]
        return Standardized, Dates
    
    #Gets multiple standardized values from a stock
    def GetMultipleStandardized(self,tickers,start_date,end_date):
        final_list = []
        dates = []
        for idx in range(0,len(tickers)):
            data = self.GetSingleStandarized(tickers[idx],start_date,end_date)
            final_list.append(data[0])
            dates.append(data[1])
        return final_list,dates
    #Standardizes Data
    def StandardizeData(self,data):
        return self.Scaler.fit_transform(data)
    
    #A class to get and Merge the panel and trend data of one stoclk
    def GetMergeDataOne(self,ticker,start_date,end_date):
        tickers = [ticker]
        PanelData = self.DataStream.GetPanelData(tickers,start_date,end_date)
        TrendData = self.DataStream.GetTrendData(tickers,start_date,end_date)
        DatesPanel = PanelData.index.tolist()
        DatesTrend = TrendData.index.tolist()
        PanelData = np.array(PanelData)
        TrendData = np.array(TrendData)
        Final_Length = len(DatesPanel)
        Adjusted_Trend_Data = np.array(self.Reshape2(np.transpose(TrendData),Final_Length)[0]).reshape(-1,1)
        return np.concatenate((PanelData,Adjusted_Trend_Data),1),DatesPanel 
    
    #The reshaping algorithm to combine panel and trend data
    def Reshape1(self,dataset,target_size):
        dataset = np.array(dataset)
        target_list = []
        for i in range(0,target_size):
            target_list.append(target_size)
        dataset = np.array(dataset)
        nl = []
        for i in dataset:
            nl.append(i)
            nl.append(i)
        dataset = np.array(nl)
        dataset = np.array(dataset)
        while np.array(dataset).shape[0] < target_size:
            nl = []
            for i in dataset:
                nl.append(i)
                nl.append(i)
            dataset = np.array(nl)
            dataset = np.array(dataset)
        dataset = nl
        n2dl = []
        target_size = np.array(target_size)
        n2d = (np.array(dataset).shape[0]-target_size)
        scale_fac = np.array(dataset).shape[0]/(np.array(dataset).shape[0]-target_size)
        for i in range(0,n2d):
            n2dl.append(int(i*scale_fac))
        dl = []
        for i in range(0,np.array(dataset).shape[0]):
            if i not in n2dl:
                dl.append(dataset[i])
    
        return np.array(dl)
    
    #The reshaping algorithm above but with higher dimentional arrays
    def Reshape2(self,dataset,targetsize):
        new_list = []
        for i in dataset:
            new_list.append(self.Reshape1(i,targetsize))
        return new_list
    
    #A function to split data into windowed batches
    def MakeBatches(self,x,window_size,step_size):
        return_list = []
        for i in range(0,len(x)-window_size+1,step_size):
            return_list.append(self.StandardizeData(x[i:i+window_size]))
        return return_list
    
    #A function to make batches with higher orders of dimentions
    def MultiMakeBatches(self,x,window_size,step_size):
        sub_list = []
        for subsection in x:
            sub_list += self.MakeBatches(subsection,window_size,step_size)
            
        return np.array(sub_list)
    
    #A function to make multiple batches and then split them by Stock
    def MultiMakeBatchesArranged(self,x,window_size,step_size):
        sub_list = []
        for subsection in x:
            sub_list.append(self.MakeBatches(subsection,window_size,step_size))
        return np.array(sub_list)
        

#A raw version of the RawDataHandler meant to work with diffed amounts instead of raw data
class BuySellHandler(RawDataHandler):
    def __init__(self):
        super().__init__()
        
    #Diffrence the value of a single stock
    def GetSingleDiffed(self,ticker,start_date,end_date):
        Concat_Data = self.GetMergeDataOne(ticker,start_date,end_date)
        Standardized = self.StandardizeData(np.diff(Concat_Data[0],1,0))
        Dates = Concat_Data[1]
        return Standardized, Dates
    
    #Getting Multiple Diffrenced Stocks
    def GetMultipleDiffed(self,tickers,start_date,end_date):
        final_list = []
        dates = []
        for idx in range(0,len(tickers)):
            data = self.GetSingleDiffed(tickers[idx],start_date,end_date)
            final_list.append(data[0])
            dates.append(data[1])
        return final_list,dates
    #A Specific data handling method for this version of SPV6
    def BuySell(self,tickers,start_date,end_date):
        # Labels|'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume','Trends'|
        Data = self.GetMultipleDiffed(tickers,start_date,end_date)
        final_list = np.array(Data[0])[:][::]
        ShouldBuy= final_list>0
        return np.array(Data[0]),ShouldBuy.astype(int),Data[1]
    def BuySellSingle(self,tickers,start_date,end_date):
        # Labels|'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume','Trends'|
        Data = self.GetSingleDiffed(tickers,start_date,end_date)
        final_list = np.array(Data[0])[:][::]
        ShouldBuy= final_list>0
        return np.array(Data[0]),ShouldBuy.astype(int),Data[1]
    


#A =  BuySellHandler()
#x = (A.BuySell(["NVDA","AMD"],"2014-01-01","2019-01-01"))