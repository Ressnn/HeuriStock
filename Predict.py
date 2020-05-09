# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 12:29:19 2020

@author: Pranav Devarinti
"""

import sys
import DataHandler
import Model
window_size = 64
step_size = 1
if len(sys.argv) == 1: 
    import kivy
    kivy.require("1.10.1")
    from kivy.app import App
    from kivy.uix.floatlayout import FloatLayout
    from kivy.uix.label import Label
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.textinput import TextInput
    from kivy.uix.button import Button
    from kivy.graphics import *
    from kivy.uix.popup import Popup
    
    

    #Same Window Size Parameter as in other file

    #Trend Data Soruce: Google Trends
    #Stock Data Source: Yahoo Finance
    
    
    class PredictorPage(GridLayout):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.cols = 2
            self.add_widget(Label(text="Company Name:", font_size=30))
            self.Ticker = TextInput(multiline=False, font_size=30)
            self.add_widget(self.Ticker)
    
            self.add_widget(Label(text="Start Refrence (yyyy-mm-dd):", font_size=30))
            self.Start = TextInput(multiline=False, font_size=30)
            self.add_widget(self.Start)
            
            self.add_widget(Label(text="Stop Refrence(yyyy-mm-dd):", font_size=30))
            self.Stop = TextInput(multiline=False, font_size=30)
            self.add_widget(self.Stop)
            
            self.Predict = Button(text="Predict", font_size=30)
            self.Predict.bind(on_release=self.PredictButton)
            self.add_widget(self.Predict)
            
            self.Updates = Button(text="Version Information", font_size=30)
            self.Updates.bind(on_press=self.InfoPopup)
            self.add_widget(self.Updates)
            
            self.OutputPrediction = Label(text="Decision", font_size=30)
            self.add_widget(self.OutputPrediction)
            
            self.Probability = Label(text="Probability", font_size=30)
            self.add_widget(self.Probability)
            try:
                self.DH = DataHandler.BuySellHandler()
                self.Predictor = Model.StockPredictingModel((window_size,7))
                self.Predictor.Load()
            except:
                raise AssertionError("Load Failed")
            
        def InfoPopup(self,ext):
            layout = GridLayout(cols=1,padding= 10)
            layout.add_widget(Label(text='Made by Pranav Devarinti', font_size=20))
            layout.add_widget(Label(text='Version: 6.1.4', font_size=20))
            layout.add_widget(Label(text='Stock data gathered from Yahoo Finance', font_size=20))
            layout.add_widget(Label(text='Trend Data gathered from Google Trends', font_size=20))
            
            popup = Popup(title="Version Information", content=layout,size_hint =(None, None), size =(500, 400))
            popup.open()
        def PredictButton(self, instance):
            try:
                Ticker = self.Ticker.text
                print([Ticker])
                Start = self.Start.text
                Stop = self.Stop.text
                Data = self.DH.BuySell([Ticker],Start,Stop)
                Model_throughput_X = Data[0][-1][-window_size:].reshape(1,window_size,7)
                Return_Values = self.Predictor.Predict(Model_throughput_X)
                br = ""
                bkg = (0,0,0,0)
                if Return_Values[0][0]>.5:
                    br = "Buy"
                    bkg = (0,1,0,1)
                else:
                    br = "Sell"
                    bkg = (1,0,0,1)
                print(br)
                pb = Return_Values
            except:
                br = "Error"
                bkg = (0,0,1,1)
                pb = "Check Inputs"
            self.OutputPrediction.text = br
            self.OutputPrediction.color = bkg
            self.Probability.text = str(pb[0][0])
            
    class PredictorApp(App):
        def build(self):
            return PredictorPage()
    
    cs = PredictorApp().run()
else:
    DH = DataHandler.BuySellHandler()
    Predictor = Model.StockPredictingModel((window_size,7))
    Predictor.Load()
    stocks = sys.argv[1].split(",")
    print("Sotcks Entered:"+str(stocks))
    Data = DH.BuySell(stocks,sys.argv[2],sys.argv[3])
    for i in range(0,len(stocks)):
        Model_throughput_X = Data[i][-1][-window_size:].reshape(1,window_size,7)
        print(Predictor.Predict(Model_throughput_X))