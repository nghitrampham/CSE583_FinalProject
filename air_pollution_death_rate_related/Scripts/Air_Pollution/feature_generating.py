"""
This module is used to perform feature engineering on air pollution data
"""
import warnings
import helpers

warnings.filterwarnings('ignore')

if __name__ == '__main__':
    PATH = r'../../AQI_modeling/data/data_air_raw/daily_aqi_by_county_'
    ### use most recent 3 years to train model
    RAW_DATA = helpers.read_raw_data(PATH, [2016, 2017, 2018])
    DATA = helpers.data_cleaning(RAW_DATA) ### clean data before doing feature engineering

    for county_name in list(DATA["state_county"].unique()): #### we do feature engineering
    																#### on each county independently
    	#### feature engineering for model							
        df = (helpers.feature_engineering_for_AQI(DATA, 30, county_name,\
        "../../AQI_modeling/data/county_features_data/county_features_train/"))
            