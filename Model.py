# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 16:26:49 2020

@author: Pranav Devarinti
"""

import numpy as np
from keras.models import Sequential
from keras.layers import *
from keras.models import load_model
from sklearn.model_selection import KFold
import tensorflow as tf
#Trend Data Soruce: Google Trends
#Stock Data Source: Yahoo Finance


# This is a class with all extra fuctions of the stock predicting model as well as the model itself
# Note: This is not a subclass of keras.models.Sequential(), but instead its own class
# The way its setup here, If a thing better than a NN comes along later we chan swap it out here
class StockPredictingModel():
    # The shape parameter is the input shape of the mode
    # Try setting up cuda version of model
    # Note: cuda and normal models got combined and CuDNNLSTM is now depracated Switching from CuDNNLSTM to just LSTM
    
    
    def __init__(self,shape):
        """
        The constructor, sets up the machine learning model
        
        Parameters
        ----------
        shape : tuple
            The Shape of the ML Model

        Returns
        -------
        None.

        """
        #Lets Start By Setting Up the Keras Model
        self.model = Sequential()
        #The input layer parameter is used here to futureproof, NOTE THAT IT ISN'T NEEDED
        
        self.model.add(InputLayer(input_shape=shape))
        #LSTM's Used to remeber past events and make furture predictions based on it
        self.model.add(Bidirectional(GRU(180,return_sequences=True)))
        self.model.add(Bidirectional(GRU(40,return_sequences=True)))
        self.model.add(TimeDistributed(Dense(45,activation='selu')))
        self.model.add((Dense(35,activation='selu')))
        #No Flattening, so predictions are done timestep by timestep instead of simply being read off
        self.model.add(Flatten())
        self.model.add(Dense(50,activation='tanh'))
        self.model.add(Dropout(.3))
        self.model.add(Dense(1,activation='sigmoid'))
        print("Attempting build")
        self.model.compile(loss='mse', optimizer='adam',metrics=['mae'])
        #Finished Setting Up Keras Model with all the layers, compiling the model worked1
        print("ML Model Loaded")
            
    

    # CVTrain uses a method called cross-validation to more effectivley train the model
    # X = Stock,Trend Data| Y=Was the best option to Buy or Sell|Splits = Crossval Parameter|Epochs:More = better but will take longer|batch_size:Less = better but takes longer
    
    def CVTrain(self,x,y,splits,epochs,batch_size):
        """
        Cross-Validation Training method

        Parameters
        ----------
        x : np.array
            inputs
        y : np.array
            outputs
        splits : int
            The number of splits in the cross-validation
        epochs : int
            The number epochs in a keras model
        batch_size : int
            the batch_size training parameters

        Returns
        -------
        None.

        """
        #We use sk-learns kfold here to split the dataset for us
        kfold = KFold(splits, True, 1)  
        data = []
        for i in range(len(x)):
            data.append(i)
        #Here kfold tells us what indicies to look for the right data at, we go there, get the data, and train the model with it
        for train, test in kfold.split(data):
            trainx = []
            trainy = []
            testx = []
            testy =[]
            for i in train:
                trainx.append(x[i])
                trainy.append(y[i])
            for i in test:
                testx.append(x[i])
                testy.append(y[i])
            #Training the model here
            self.model.fit(np.array(trainx),np.array(trainy),epochs=epochs,batch_size=batch_size,validation_data=(np.array(testx),np.array(testy)))
            
    #Saves the model
    def Save(self):
        """
        Saves the model

        Returns
        -------
        None.

        """
        self.model.save('PredictorTrainedModel.h5')
        self.model.save_weights('PredictorTrainedModelWeights.h5')
    #Loads the model
    def Load(self):
        """
        Loads the model

        Returns
        -------
        None.

        """
        self.model.load_weights('PredictorTrainedModelWeights.h5')
    #Predicts Based on the data given
    def Predict(self,x):
        """
        Predicts Based on given data

        Parameters
        ----------
        x : np.array
            Input Data

        Returns
        -------
        np.array
            the output from the ML model

        """
        return self.model.predict(x)