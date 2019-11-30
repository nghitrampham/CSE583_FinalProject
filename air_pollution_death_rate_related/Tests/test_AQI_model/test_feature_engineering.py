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
from Scripts.Air_Pollution import helpers
# from feature_generating import *
# from helpers import feature_engineering_for_AQI, compute_lag_time_series_features
# from helpers import read_raw_data, data_cleaning, concat_name_county
from pandas import read_csv
from pandas import DataFrame
from pandas import concat

warnings.filterwarnings('ignore')

PATH = r'../../Data/Air_Pollution/data_air_raw/daily_aqi_by_county_'
list_year = [2018]


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
  
