import pandas as pd
import numpy as np
import tensorflow
import time
import warnings
import math
import matplotlib.pyplot as plt
import argparse
import pickle
import helpers

from keras.models import load_model
from numpy import newaxis
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
from pandas import read_csv
from pandas import DataFrame
from pandas import concat

warnings.filterwarnings("ignore")

def load_data(filename):
    """
    AQI = Air Quality Index
    This function is used to load training data set for deep learning AQI model.
    @param filename: .csv file containing features for specific county
    @param seq_len: len of the features, will be the input to neural net model.
    @return [x_train, y_train, x_test, y_test]: [training testing data]
    @return scaler: applying min-max scaler model to normalize data
    """
    
    f = pd.read_csv(filename)
    if f.shape[0] < 10:
        return [[], [], [], []], None
    
    feature_col = [col for col in f.columns if col != "AQI"]
    label_col = ["AQI"]
    data = f[feature_col + label_col]
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    row = round(0.8*data.shape[0])
    train = data.iloc[:row, :]
    train = scaler.fit_transform(train)
    
    
    np.random.shuffle(train)
    train = np.array(train)
    x_train = train[:row, :-1]
    y_train = train[:row, -1]
    test = data.iloc[row:, :]
    test = scaler.transform(test)
    test = np.array(test)
    x_test = test[:, :-1]
    y_test = test[:, -1]
    x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
    x_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))
    
    return [x_train, y_train, x_test, y_test], scaler

def build_model(layers):
    """
    This function is used to build deep neural network to predict time series values
    @param layers: containing number of hidden unit at different layers
    @return model: return defined model.
    """
    model = Sequential()
    
    model.add(LSTM(4, input_shape=(1, 38), return_sequences = True))
    model.add(Dropout(0.2))

    model.add(LSTM(4, return_sequences = False))
    model.add(Dropout(0.2))

    model.add(Dense(output_dim = layers[3]))

    model.add(Activation("linear"))


    start  = time.time()
    model.compile(loss = "mse", optimizer = "rmsprop")
    print("Compilation Time", time.time() - start)

    return model


if __name__ =='__main__':

    root = "../../Data/Air_Pollution/county_features_data/county_features_train/"
    
    county_df = pd.read_csv("../../Data/Air_Pollution/data_misc/all_county_names.csv")
    county_list = list(county_df["state_county"].unique())
    
    epochs = 100
    seq_len = 38
    
    for county in county_list:
    
        global_time = time.time()
        [X_train, y_train, X_test, y_test], scaler = load_data(root + county + "_feature.csv")
     
        pickle.dump(scaler, open("../../Trained_Model/MinMax_scaler_model/" + county + "_scaler.pickle", "wb"))
       
        if X_train == []:
            continue

        model = build_model([1, 38, 100, 1])

        model.fit(
            X_train, 
            y_train,
            batch_size = 16, 
            nb_epoch = epochs,
            validation_split = 0.1
            )
        
        model_name = str(county) + "_model.h5"
        
        model.save('../../Trained_Model/county_AQI_model/' + model_name)  # creates a HDF5 file 'my_model.h5'
        predictions = helpers.predict_point_by_point(model, X_test)
        helpers.plot_results(predictions, y_test)
        
        del model, X_train, y_train, X_test, y_test, model_name, predictions  # deletes the existing model

