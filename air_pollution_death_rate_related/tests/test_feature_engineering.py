import pandas as pd
import numpy as np
import time
import warnings
import math
import matplotlib.pyplot as plt
import argparse
import pickle
import datetime as dt
import unittest
import pytest


from numpy import newaxis
from ..Scripts.Air_Pollution import helpers
from pandas import read_csv
from pandas import DataFrame
from pandas import concat

warnings.filterwarnings('ignore')

PATH = r'air_pollution_death_rate_related/Data/air_pollution/data_air_raw/daily_aqi_by_county_'
list_year = [2018]
### use most recent 3 years to train model
RAW_DATA = helpers.read_raw_data(PATH, [2016, 2017, 2018])
DATA = helpers.data_cleaning(RAW_DATA) ### clean data before doing feature engineering


def test_read_raw_data():
    data = helpers.read_raw_data(PATH, list_year)
    lst_col = ['State Name',
               'county Name',
               'State Code',
               'County Code',
               'Date',
               'AQI',
               'Category',
               'Defining Parameter',
               'Defining Site',
               'Number of Sites Reporting']

    assert data.shape == (339479, 10)
    assert list(data.columns) == lst_col
    assert int(data['county Name'].nunique()) > 100
    assert int(data.Date.nunique()) > 100
    data_dub = (data[['State Name', 'county Name']]
                .drop_duplicates()
                .reset_index())
    for state, county in zip(list(data_dub['State Name']),\
                                list(data_dub['county Name'])):
        df = data[(data['State Name'] == state) & (data['county Name'] == county)]
        assert (df.groupby("Date")
                .count().unstack()
                .reset_index()
                .rename(columns={0: "count"})["count"].max() == 1) ## make sure there is only one AQI 
                                                               ## for each county for each day 

def test_data_cleaning():
    cols = ['State',
            'County',
            'State Code',
            'County Code',
            'Date',
            'AQI',
            'Category',
            'Defining Parameter',
            'Defining Site',
            'Number of Sites Reporting',
            'state_county',
            'date']
    data_raw = helpers.read_raw_data(PATH, list_year)
    data = helpers.data_cleaning(data_raw)
    assert len(list(data.columns)) == 12
    assert data.shape[0] > 100
    assert np.sum([data[x].map(type).nunique() -1 for x in data.columns]) == 0
    assert np.sum([data[x].isnull().sum() for x in data.columns]) == 0
    assert int(data.state_county.nunique()) > 100
    assert list(data.columns) == cols
    
    
def test_feature_engineering_for_AQI():
    
    feature_names = ['lag_1', 'lag_2', 'lag_3', 
                     'lag_4', 'lag_5', 'lag_6', 
                     'lag_7', 'lag_8', 'lag_9', 
                     'lag_10', 'lag_11', 'lag_12', 
                     'lag_13', 'lag_14', 'lag_15',
                     'lag_16', 'lag_17', 'lag_18',
                     'lag_19', 'lag_20', 'lag_21',
                     'lag_22', 'lag_23', 'lag_24', 
                     'lag_25', 'lag_26', 'lag_27', 
                     'lag_28', 'lag_29',
                     'day_Friday', 'day_Monday', 
                     'day_Saturday', 'day_Sunday',
                     'day_Thursday', 'day_Tuesday', 
                     'day_Wednesday', 'AQI', 'current_date',
                     'current_month']
    
    data_raw = helpers.read_raw_data(PATH, list_year)
    data_cleaned = helpers.data_cleaning(data_raw)
    features = helpers.feature_engineering_for_AQI(data_cleaned, 30, "alabama_baldwin", "")
    
    assert len(features) == 4
    assert len(features['feature_names']) == 39
    assert list(features["data"].columns) == feature_names
    assert features["data"].shape[0] >= 1

def test_concat_name_county():

    case1 = "louisiana east baton    rouge"
    result1 = "louisiana_east_baton_rouge"
    concated_name1 = helpers.concat_name_county(case1)

    case2 = "alabama baldwin"
    result2 = "alabama_baldwin"
    concated_name2 = helpers.concat_name_county(case2)


    assert concated_name1 == result1
    assert concated_name2 == result2



def test_compute_lag_time_series_features():

    df_state = DATA[DATA["state_county"] == "alabama_baldwin"]
    df_state["date"] = df_state["Date"].apply(lambda x: pd.to_datetime(x))
    df_state["current_date"] = df_state["date"].dt.day
    df_state["current_month"] = df_state["date"].apply(lambda x: x.month)
    df_state['day_of_week'] = df_state['date'].dt.weekday_name

    day_df = pd.get_dummies(df_state["day_of_week"], prefix="day")
    df_temp = pd.concat([df_state, day_df], axis = 1)

    df_feature = df_temp[list(day_df.columns) + ["AQI", "current_date", "current_month", "date"]]
    df_feature = df_feature.sort_values(by=["date"])

    df_lag_features = helpers.compute_lag_time_series_features(df_feature)

    cols = ['AQI', 'lag_1', 'lag_2', 'lag_3',
            'lag_4', 'lag_5', 'lag_6', 'lag_7',
            'lag_8', 'lag_9', 'lag_10', 'lag_11', 
            'lag_12', 'lag_13', 'lag_14',
            'lag_15', 'lag_16', 'lag_17', 
            'lag_18', 'lag_19', 'lag_20', 'lag_21', 
            'lag_22', 'lag_23', 'lag_24', 'lag_25', 
            'lag_26', 'lag_27', 'lag_28',
            'lag_29']

    assert list(df_lag_features.columns) == cols
    assert df_lag_features.shape[0] >= 1
    assert df_lag_features.isnull().sum().sum() == 0
    assert df_lag_features.max().max() < 400
    assert df_lag_features.min().min() > 0




