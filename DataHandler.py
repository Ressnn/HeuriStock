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
""" A class to acsess data from google trends and yahoo finance"""
class DataAcsessor():
    #Sets up the PyTrends Requester class to get trend data
    def __init__(self):
        """
        The constructor of the DataAcsessor class

        Returns
        -------
        None.

        """
        self.PytrendsRequester = TrendReq(hl='en-US', tz=360)
        
    #Gets Stock Data   
    def GetPanelData(self,tickers,start_date,end_date): 
        """
        Returns stock data

        Parameters
        ----------
        tickers : list
            A list of strings containing stocks to get data for
        start_date : String
            The start data
        end_date : String
            The stop date

        Returns
        -------
        pd.Dataframe
            A dataframe of the stock data

        """
        return web.get_data_yahoo(tickers, start_date, end_date)
    
    #Gets Trend Data
    def GetTrendData(self,tickers,start_date,end_date):
        """
        Returns stock data

        Parameters
        ----------
        tickers : list
            A list of strings containing stocks to get data
        start_date : String
            The start data
        end_date : String
            The stop date

        Returns
        -------
        pd.Dataframe
            A dataframe of the stock data

        """
        total_dates = start_date + ' ' + end_date
        self.PytrendsRequester.build_payload(tickers,cat=0, timeframe=total_dates, geo='', gprop='')
        return self.PytrendsRequester.interest_over_time()
    
""" The main class tasked with handling data from
the other DataAcsessor
"""

class RawDataHandler():
    #Constructs RawDataHandler nothing much here
    def __init__(self):
        """
        The constructor for the RawDataHandler
     
        Returns 
        -------
        None.

        """
        #DataStream sets up a Raw Data Stream that allows us to easily acsess raw data
        self.DataStream = DataAcsessor()
        #A Standardizing Scaler used later
        self.Scaler = StandardScaler()
        
    def GetSingleStandarized(self,ticker,start_date,end_date):
        """
        Gets a single standardized data value

        Parameters
        ----------
        ticker : String
            The stock ticker to predict for
        start_date : String
            The start date
        end_date : String
            The stop date

        Returns
        -------
        Standardized : np.array
            The standardized datasets
        Dates : String
            The last day that stock data is for

        """
        
        
        Concat_Data = self.GetMergeDataOne(ticker,start_date,end_date)
        Standardized = self.StandardizeData(Concat_Data[0])
        Dates = Concat_Data[1]
        return Standardized, Dates
    
    #Gets multiple standardized values from a stock
    def GetMultipleStandardized(self,tickers,start_date,end_date):
        """
        

        Parameters
        ----------
        tickers : list
            the tickers of the stocks you want to predict for
        start_date : String
            The start date
        end_date : String
            The stop date

        Returns
        -------
        final_list : np.array
            an array full of the final useful stock values
        dates : String
            The last day recorded

        """
        final_list = []
        dates = []
        for idx in range(0,len(tickers)):
            data = self.GetSingleStandarized(tickers[idx],start_date,end_date)
            final_list.append(data[0])
            dates.append(data[1])
        return final_list,dates
    
    def StandardizeData(self,data):
        """
        Standardizes Data
        
        Parameters
        ----------
        data : list
            Data to scale

        Returns
        -------
        np.array
            Scaled attacks

        """
        return self.Scaler.fit_transform(data)
    
    def GetMergeDataOne(self,ticker,start_date,end_date):
        """
        A class to get and Merge the panel and trend data of one stock

        Parameters
        ----------
        ticker : String
            The ticker to predict for
        start_date : String
            The date to start getting data for
        end_date : String
            The data to stop getting data for

        Returns
        -------
        np.array
            Stacked Data
        DatesPanel : list
            The Dates of each of the stock entries

        """
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
    
    
    def Reshape1(self,dataset,target_size):
        """
        The reshaping algorithm to combine panel and trend data

        Parameters
        ----------
        dataset : np.array
            The panel and trend data
        target_size : int
            The target size to reshape the array

        Returns
        -------
        np.array
            returns a numpy array of the target size

        """
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

    def Reshape2(self,dataset,targetsize):
        """
        The reshaping algorithm above but with higher dimentional arrays
        
        Parameters
        ----------
        dataset : np.array
            a multidimentional numpy array that needs to be reshaped
        targetsize : int
            the target size

        Returns
        -------
        new_list : list
            A list of numpy arrays that were reshaped

        """
        new_list = []
        for i in dataset:
            new_list.append(self.Reshape1(i,targetsize))
        return new_list
    
    def MakeBatches(self,x,window_size,step_size):
        """
        A function to split data into windowed batches


        Parameters
        ----------
        x : np.array
            dataset to make batches of
        window_size : int
            the length of each batch
        step_size : int
            the distance between windows

        Returns
        -------
        return_list : list
            A list with windowed batches Standardized Data inside of it

        """
        return_list = []
        for i in range(0,len(x)-window_size+1,step_size):
            return_list.append(self.StandardizeData(x[i:i+window_size]))
        return return_list
    
    def MultiMakeBatches(self,x,window_size,step_size):
        """
        A function to make batches with higher orders of dimentions

        Parameters
        ----------
        x : numpy array
            dataset to make batches of
        window_size : int
            the length of each window
        step_size : int
            the steps between windows

        Returns
        -------
        numpy array
            a numpy array filled with higer order batches

        """
        sub_list = []
        for subsection in x:
            sub_list += self.MakeBatches(subsection,window_size,step_size)
            
        return np.array(sub_list)
    
    def MultiMakeBatchesArranged(self,x,window_size,step_size):
        """
        A function to make multiple batches and then split them by Stock

        Parameters
        ----------
        x : np.array
            the dataset
        window_size : int
            length of window
        step_size : int
            steps between each window

        Returns
        -------
        no.array
            a numpy array of each batch

        """
        sub_list = []
        for subsection in x:
            sub_list.append(self.MakeBatches(subsection,window_size,step_size))
        return np.array(sub_list)
        

"""A raw version of the RawDataHandler meant to work with diffed amounts instead of raw data"""
class BuySellHandler(RawDataHandler):
    def __init__(self):
        """
        The buy sell constructor

        Returns
        -------
        None.

        """
        super().__init__()
        
 
    def GetSingleDiffed(self,ticker,start_date,end_date):
        """
        Diffrence the value of a single stock

        Parameters
        ----------
        ticker : list
            The tickers to use
        start_date : String
            The start date
        end_date : String
            The stop date

        Returns
        -------
        Standardized : np.array
            A numpy array of the diffed data
        Dates : np.array
            the stock dates

        """
        Concat_Data = self.GetMergeDataOne(ticker,start_date,end_date)
        Standardized = self.StandardizeData(np.diff(Concat_Data[0],1,0))
        Dates = Concat_Data[1]
        return Standardized, Dates
    
    
    def GetMultipleDiffed(self,tickers,start_date,end_date):
        """
        Getting Multiple Diffrenced Stocks

        Parameters
        ----------
        ticker : list
            The tickers to use
        start_date : String
            The start date
        end_date : String
            The stop date

        Returns
        -------
        final_list : np.array
            stacked diffed arrays
        dates : list
            A list of the dates

        """
        final_list = []
        dates = []
        for idx in range(0,len(tickers)):
            data = self.GetSingleDiffed(tickers[idx],start_date,end_date)
            final_list.append(data[0])
            dates.append(data[1])
        return final_list,dates
   
    def BuySell(self,tickers,start_date,end_date):
        """
        Calculating the buy or sell array of for multiple tickers

        Parameters
        ----------
        ticker : list
            The tickers to use
        start_date : String
            The start date
        end_date : String
            The stop date

        Returns
        -------
        np.array
            stock data
        int
            ShouldBuy
        np.array
            trend data

        """
        # Labels|'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume','Trends'|
        Data = self.GetMultipleDiffed(tickers,start_date,end_date)
        final_list = np.array(Data[0])[:][::]
        ShouldBuy= final_list>0
        return np.array(Data[0]),ShouldBuy.astype(int),Data[1]
    
    def BuySellSingle(self,tickers,start_date,end_date):
        """
        Calculating the buy or sell array of a single ticker

        Parameters
        ----------
        ticker : list
            The tickers to use
        start_date : String
            The start date
        end_date : String
            The stop date

        Returns
        -------
        np.array
            stock data
        int
            ShouldBuy
        np.array
            trend data

        """
        # Labels|'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume','Trends'|
        Data = self.GetSingleDiffed(tickers,start_date,end_date)
        final_list = np.array(Data[0])[:][::]
        ShouldBuy= final_list>0
        return np.array(Data[0]),ShouldBuy.astype(int),Data[1]
    


#A =  BuySellHandler()
#x = (A.BuySell(["NVDA","AMD"],"2014-01-01","2019-01-01"))