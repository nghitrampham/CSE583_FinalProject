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
from Scripts.Air_Pollution import main_AQI
from pandas import read_csv
from pandas import DataFrame
from pandas import concat

warnings.filterwarnings('ignore')

PATH = r'../../Data/Air_Pollution/data_air_raw/daily_aqi_by_county_'
root = r'../../Data/Air_Pollution/county_features_data/county_features_train/florida_bay_feature.csv'
list_year = [2018]

def test_load_data()

	[X_train, y_train, X_test, y_test], scaler = main_AQI.load_data(filename)

	assert X_train.shape == (,)
	assert y_train.shape == (,)
	assert X_test.shape == (,)
	assert y_test.shape == (,)

	