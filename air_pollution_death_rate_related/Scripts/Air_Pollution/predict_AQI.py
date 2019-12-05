"""
This module is used to predict Air Quality Index for all available counties in 2019.
"""
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
# from . import helpers
import helpers
import time
import math
import matplotlib.pyplot as plt
from keras.models import load_model
import argparse
import pickle

warnings.filterwarnings("ignore")

def main():
    
    data2019_raw = pd.read_csv("air_pollution_death_rate_related/data/Air_Pollution/data_air_raw/daily_aqi_by_county_2019.csv")
    data2019 = helpers.data_cleaning(data2019_raw)
    
    ## initialization 
    predicted_AQI = []
    predicted_date = "2019-03-12"
    predicted_county = []

    f = open("temp.csv","w")
    f.write("date,state_county,AQI\n")

    # for county in list(data2019["state_county"].unique()):
    for county in list(data2019["state_county"].unique())[:5]:
   
        ## load model to predict AQI
        print("---> Loading model for county {} ...".format(county))
        # scaler_path = "../../Trained_model/MinMax_scaler_model/" + county + "_scaler.pickle"
            
        # model_path = "../../Trained_model/county_AQI_model/" + county + "_model.h5"
        
        # mm_scaler = pickle.load(open( scaler_path, "rb" ))
        # model = load_model(model_path)

        try:
            scaler_path = "air_pollution_death_rate_related/Trained_model/MinMax_scaler_model/" + county + "_scaler.pickle"

            model_path = "air_pollution_death_rate_related/Trained_model/county_AQI_model/" + county + "_model.h5"
            
            model = load_model(model_path)
            mm_scaler = pickle.load(open( scaler_path, "rb" ))

            ### feature engineering for model
            data_feature_temp = helpers.data_feature_engineering_for_test(data2019, county, predicted_date)
            X_test, y_test = helpers.load_test_data(data_feature_temp["data"], mm_scaler)

            ## predicting AQI
            predictions = helpers.predict_point_by_point(model, X_test)
            # helpers.plot_results(predictions, y_test)

            ## keep prediction for all counties
            print("Predicting ....")
            y = np.append(X_test, predictions.reshape( 1, 1, 1)).reshape(1,39)
            y_scale = mm_scaler.inverse_transform(y)[-1][-1]
            # predicted_AQI.append(mm_scaler.inverse_transform(y)[-1][-1])
            # predicted_county.append(county)
            f.write(predicted_date+","+county+","+str(y_scale)+"\n")

            del data_feature_temp, scaler_path,\
                model_path, model, mm_scaler, X_test, y_test, predictions, y, y_scale
        
        except Exception as e:
            print(e)
            e.args += ('Path and list_year must not be empty', "check read_raw_data function" )

    f.close()
 
    ## creating dataframe containing county, state, predicted AQI, predicted date for interactive visualization map 
    county_code = pd.read_csv("air_pollution_death_rate_related/data/Air_Pollution/data_misc/county_with_code.csv")
    df_prediction = pd.read_csv("temp.csv")
    # df_prediction = pd.DataFrame({"date": pd.to_datetime(predicted_date), 
    #                               "state_county": predicted_county,
    #                               "AQI": predicted_AQI,
    #                              })
    df_result = (pd.merge(county_code, df_prediction,
                          how='inner', 
                          left_on=["state_county"], 
                          right_on = ["state_county"])
                )
    df_result.to_csv("predicted_AQI" + predicted_date + ".csv", index=False)
    
    
if __name__ =='__main__':
    main()
    
    
