import pandas as pd
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
import numpy as np

import tensorflow
import time 
import warnings 
import numpy as np 
from numpy import newaxis 
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM 
from keras.models import Sequential 
from sklearn.preprocessing import MinMaxScaler


import time
import math
import matplotlib.pyplot as plt
from keras.models import load_model

import argparse
import pickle
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
import datetime as dt

import warnings
warnings.filterwarnings('ignore')



######### DATA CLEANING + FEATURE ENGINEERING ###############
def read_raw_data(path, list_year):
    """
    This function is used to read all *.csv files and concatinate them into one single dataframe
    @param path: path directory contains raw data
    @param list_year: list containing all years that we are interested in to build model
    @return data_raw: a dataframe containing raw data of all years (concatinate all *.csv file)
    """
    
    try:
        assert path != " "
        assert list_year != []
    except AssertionError as e:
        e.args += ('Path and list_year must not be empty', "check read_raw_data function" )
        raise
    
    all_files = [path + str(year) + ".csv" for year in list_year]

    current_dataframe = []
    for filename in all_files:
        temp = pd.read_csv(filename, index_col=None, header=0)
        current_dataframe.append(temp)
    data_raw = pd.concat(current_dataframe, axis=0, ignore_index=True)
    
    return data_raw


def concat_name_county(name):
    """
    This function is used to concat a string of words by putting underscore between words
    example: "new york steuben" --> "new_york_steuben"
    @param name: string of raw name
    @return concat_name: concated words of string by underscore
    """
    try:
        assert name != ""
    except AssertionError as e:
        e.args += ('input must not be a empty string', "check concat_name_county function" )
        raise
        
    name_vector = str(name).split(" ")
    concat_name = ""
    for i in name_vector:
        if (i == " ") or (i == ""):
            continue
        else:
            concat_name = concat_name + "_" + str(i)
        
    return concat_name[1:].strip()


def compute_lag_time_series_features(df_feature, lag_time = 30):
    
    assert df_feature.shape[0] >= 1
    
    try:
        temps = df_feature.sort_values(by=["date"])["AQI"]
        dataframe = temps
        col_name=['AQI']
        for lag_index in range(1,lag_time):
            dataframe = concat([temps.shift(lag_index), dataframe], axis=1)
            col_name.append('lag_' + str(lag_index))
        dataframe.columns = col_name

        if dataframe.shape[0] < lag_time:
            lag_features = dataframe.iloc[-1:,:]
            lag_features = lag_features.fillna(0)
        else:
            lag_features = dataframe.iloc[lag_time-1:,:]
    except:
        raise AttributeError("FEATURE DATAFRAME IS EMPTY !!!!!")
   
    return lag_features

def data_cleaning(data_raw):
    
    """ Taking raw air pollution data each year and clean it before feature engineering
    """
    try:
        assert data_raw.shape != (0,0)
        assert "State Name" in data_raw.columns
        assert "county Name" in data_raw.columns
        assert "Date" in data_raw.columns
        
    except AssertionError as e:
        e.args += ('data_raw must not be empty or missing columns', "check data_cleaning function" )
        raise
    
    data_raw["State Name"] = data_raw["State Name"].apply(lambda x: x.lower().strip())
    data_raw["State Name"] = data_raw["State Name"].apply(lambda x: concat_name_county(x))
    data_raw["county Name"] = data_raw["county Name"].apply(lambda x: x.lower().strip())
    data_raw["county Name"] = data_raw["county Name"].apply(lambda x: concat_name_county(x))
    data_raw["state_county"] = data_raw["State Name"] + "_" + data_raw["county Name"]
    data_raw["state_county"] = data_raw["state_county"].apply(lambda x: x.lower())
    data_raw["date"] = data_raw["Date"].apply(lambda x: dt.datetime.strptime(x,'%Y-%m-%d').date())
    data_raw = data_raw.rename(columns = {"State Name": "State", "county Name": "County"})
    
    return data_raw


def feature_engineering_for_AQI(data, lag_time = 30, county_name = "", save_path = ""):
    """
    test: make sure save_path is not empty, data row > 10, data have enough columns, 
    """
    
    try:
        df_state = data[data["state_county"] == county_name]
    except:
        raise AttributeError("DATAFRAME IS EMPTY !!!!!")

    try:
        df_state["date"] = df_state["Date"].apply(lambda x: pd.to_datetime(x))
        df_state["current_date"] = df_state["date"].dt.day
        df_state["current_month"] = df_state["date"].apply(lambda x: x.month)
        df_state['day_of_week'] = df_state['date'].dt.weekday_name

        day_df = pd.get_dummies(df_state["day_of_week"], prefix="day")
        df_temp = pd.concat([df_state, day_df], axis = 1)

        df_feature = df_temp[list(day_df.columns) + ["AQI", "current_date", "current_month", "date"]]
        df_feature = df_feature.sort_values(by=["date"])

        df_lag_features = compute_lag_time_series_features(df_feature)
        row = np.min([df_feature.shape[0]-1, lag_time-1])
        df_data = (pd.concat([df_lag_features.drop(["AQI"], axis = 1), 
                         df_feature.drop(["date"], axis = 1).iloc[row:,:]], axis = 1))

        if save_path: 
            path = save_path + county_name + "_feature.csv"
            print("---> Saving features to {}".format(path))
            df_data.to_csv(path, index = False)
            
    except:
        raise AttributeError("DATAFRAME IS EMPTY !!!!!")

    return {"successive code": 1, "save_path": save_path, "feature_names": df_data.columns, "data": df_data}


def data_feature_engineering_for_test(data2019, county, predicted_date):
    
    ## prepare data for specific county and specific date
    try:
        data_state = data2019[data2019["state_county"] == county]
    except:
        raise AttributeError("DATAFRAME IS EMPTY!!! check data_feature_engineering_for_test function")
    
    data_state["predicted_date"] = pd.to_datetime(predicted_date)
    data_state["date_diff"] = (data_state
                               .apply(lambda x: (x["predicted_date"] - pd.to_datetime(x["date"])).days, 
                                      axis = 1))
    data_feature = data_state[data_state["date_diff"] >0]
    data_feature = data_feature.sort_values(by=["date"]).iloc[:30, :]

    ## feature engineering
    data_feature_temp= (helpers
                        .feature_engineering_for_AQI(
                            data_feature, 30, 
                            county, 
                            "../../Data/Air_Pollution/county_features_data/county_features_test/"))
    return data_feature_temp


def clean_county_code_data(county_code):
    """
    This function is used to clean county_code dataframe
    """
        
    county_code['County'].replace(regex=True,inplace=True,to_replace=r' County',value=r'')
    county_code["County"] = county_code["County"].apply(lambda x: str(x).lower().strip())
    county_code["County"] = county_code["County"].apply(lambda x: helpers.concat_name_county(x))
    county_code["State"] = county_code["State"].apply(lambda x: str(x).lower().strip())
    county_code["State"] = county_code["State"].apply(lambda x: helpers.concat_name_county(x))
    county_code["state_county"] = county_code["State"] + "_" + county_code["County"] 
    county_code["state_county"] = county_code["state_county"].apply(lambda x: x.lower())

    return county_code


######### GENERAL HELPER FUNCTIONS ########################

def predict_point_by_point(model, data):
    print('Predicting Single Point ...')
    predicted = model.predict(data)
    predicted = np.reshape(predicted, (predicted.size,))
    return predicted


def plot_results(predicted_data, true_data):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    plt.plot(predicted_data, label='Prediction')
    plt.legend()
    plt.show()
    
    
def load_test_data(dataframe, scaler):
    """
    This function is used to set up 
    """
    
    if dataframe.shape[0] == 1:
        pass
    else:
        raise Exception("Dataframe should be of size 1xn, i.e it should be one row containing all features") 
    
    feature_col = [col for col in dataframe.columns if col != "AQI"]
    label_col = ["AQI"]

    data = dataframe[feature_col + label_col]
    test = scaler.transform(data)
    test = np.array(test)
    x_test = test[:, :-1]
    
    y_test = test[:, -1]
    x_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))
    
    return [x_test, y_test]
    