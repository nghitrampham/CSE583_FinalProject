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
from ..Scripts.Air_Pollution import main_AQI
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from keras.models import load_model

warnings.filterwarnings('ignore')

root = r'air_pollution_death_rate_related/Data/Air_Pollution/county_features_data/county_features_train/florida_bay_feature.csv'

def test_load_data():

	[X_train, y_train, X_test, y_test], scaler = main_AQI.load_data(root)

	assert X_train.shape == (821, 1, 38)
	assert y_train.shape == (821,)
	assert X_test.shape == (205, 1, 38)
	assert y_test.shape == (205,)


# def test_predict_point_by_point():

# 	model_path = "../../Trained_model/county_AQI_model/florida_bay_model.h5"
# 	model = load_model(model_path)
# 	[X_train, y_train, X_test, y_test], scaler = main_AQI.load_data(root)
# 	predictions = helpers.predict_point_by_point(model, X_test)
# 	assert predictions.shape == (205,)


