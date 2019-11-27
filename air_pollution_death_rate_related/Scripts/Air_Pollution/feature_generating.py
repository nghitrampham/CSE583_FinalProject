import pandas as pd
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
import datetime as dt

import warnings
import helpers
import pandas as pd
import glob

warnings.filterwarnings('ignore')

if __name__ =='__main__':
    
    path = r'../../AQI_modeling/data/data_air_raw/daily_aqi_by_county_' ### use your path
    data_raw = helpers.read_raw_data(path, [2016,2017,2018]) ### use most recent 3 years to train model
    data = helpers.data_cleaning(data_raw) ### clean data before doing feature engineering
    
    for county_name in list(data["state_county"].unique()):  #### we do feature engineering on each county independently
        
        df = (helpers.feature_engineering_for_AQI(
                  data, 30, 
                  county_name, 
                  "../../AQI_modeling/data/county_features_data/county_features_train/") #### feature engineering for model
             )