# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 21:45:43 2020

@author: Pranav Devarinti
"""
import tkinter as tk
from tkinter import *
import DataHandler
import Model
#Same Window Size Parameter as in other file
window_size = 64
step_size = 1
#Trend Data Soruce: Google Trends
#Stock Data Source: Yahoo Finance


# In[]


# The App class runs both the GUI and the backend
class App():
    #Here we initialize the required GUI, The predictor, and start the GUI loop
    def __init__(self,window_size):
        super().__init__()
        self.window_size = window_size
        self.UI = tk.Tk()
        self.UI.minsize(150,200)
        self.DH = DataHandler.BuySellHandler()
        self.BuildUIElements()
        self.Predictor = Model.StockPredictingModel((self.window_size,7))
        self.Predictor.Load()
        self.UI.mainloop()
        
    #Here we define the UI elements seen by the user
    def BuildUIElements(self):
        self.Citations = Label(self.UI, text="Trend Data provided by Google Trends:")
        self.Citations2 = Label(self.UI, text="Stock Data provided by Yahoo Finance:")
        self.StartDateBox = Label(self.UI, text="Starting Date yyyy-mm-dd:")
        self.StopDateBox = Label(self.UI, text="Stopping Date yyyy-mm-dd:")
        self.StockTickerBox = Label(self.UI, text="Enter the ticker here:")
        self.OutputBox = Label(self.UI, text="Output will appear here:")
        self.PredictButton = Button(self.UI,text="Predict For this Stock",command=self.ButtonPressed)
        self.StartDate = Entry()
        self.StopDate = Entry()
        self.TickerBox = Entry()
        
        #Now that weve defined everything lets put them into a row and make them show up
        self.StartDateBox.grid(row=0,column=0)
        self.StartDate.grid(row=1,column=0)
        self.StopDateBox.grid(row=2,column=0)
        self.StopDate.grid(row=3,column=0)
        self.StockTickerBox.grid(row=4,column=0)
        self.TickerBox.grid(row=5,column=0)
        self.PredictButton.grid(row=6,column=0)
        self.OutputBox.grid(row=7,column=0)
        self.Citations.grid(row=8)
        self.Citations2.grid(row=9)
        
    def ButtonPressed(self):
        try:
            StartDate = self.StartDate.get()
            EndDate = self.StopDate.get()
            Tickers = self.TickerBox.get()
            print(Tickers)
            Data = self.DH.BuySell(list(str(Tickers)),StartDate,EndDate)
            Model_throughput_X = Data[0][-1][-window_size:].reshape(1,window_size,7)
            Return_Values = self.Predictor.Predict(Model_throughput_X)
            br = ""
            if Return_Values[0][0]>.5:
                br = "Buy"
            else:
                br = "Sell"
            self.OutputBox['text'] = "Prediction( P:"+ str(Return_Values[0][0])+", Action:" + br +")"
        except:
            self.OutputBox['text'] = "Backend Error, try a diffrent stock or timeframe"


        
        return True
        
App(window_size)
