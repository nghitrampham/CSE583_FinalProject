'''
This loads previously curated and tested data into the interactive interface
'''
import numpy as np
import pandas as pd

# load in predicted aqi data
def load_predicted_aqi(counties):
    '''
    loads the predicted aqi data
    Input: County geographical information
    Output: Dataframe of predicted aqi

    '''
    # create pandas dataframe of Predicted AQI data
    df = pd.read_csv("predicted_AQI2019-03-12.csv", dtype={"fips": str})

    # append a zero infront of dataframe
    strid = [] # convert county ids to strings and append a zero in front of those that are length four
    aqi = []
    for curr_id in range(0, len(df['County Code'])):
        curr = str(df['County Code'][curr_id])
        if len(curr) < 5:
            append_id = '0' + curr
            strid.append(append_id)
            aqi.append(df['AQI'][curr_id])
        else:
            strid.append(str(df['County Code'][curr_id]))
            aqi.append(df['AQI'][curr_id])

    # Sub-dataframe for AQI
    df_aqi = {'fips':strid, 'aqi':aqi}

    county_id = []
    county_aqi = []

    for county in range(0, len(counties['features'])):
        if (counties['features'][county]['id'] in df_aqi['fips']):
            county_id.append(df_aqi['fips'][df_aqi['fips'].index(counties['features'][county]['id'])])
            county_aqi.append(df_aqi['aqi'][df_aqi['fips'].index(counties['features'][county]['id'])])
        else:
            county_id.append(counties['features'][county]['id'])
            county_aqi.append(0)

    # create adjusted aqi dataframe
    df_all_aqi = {'fips': county_id, 'aqi': county_aqi}
    return df_all_aqi

def load_correlation(counties):
    '''
    loads the correlation results between air pollution and resipratory Deaths
    Input: County geographical information
    Output: Dataframe of correlation data
    '''
    # read in respiratory death and air pollution correlation data
    df_corr = pd.read_csv("export_cor.csv", dtype={"fips": str})

    # append a zero infront of dataframe
    c_id = [] # convert county ids to strings and append a zero in front of those that are length four
    corr = []
    year_corr = []
    for curr_id in range(0, len(df_corr['county_code'])):
        curr = str(df_corr['county_code'][curr_id])
        if len(curr) < 5:
            append_id = '0' + curr
            c_id.append(append_id)
            corr.append(df_corr['correlation'][curr_id])
            year_corr.append(df_corr['year'][curr_id])
        else:
            c_id.append(str(df_corr['county_code'][curr_id]))
            corr.append(df_corr['correlation'][curr_id])
            year_corr.append(df_corr['year'][curr_id])

    # Sub-dataframe for orrelation results between respiratory death rates and air pollution
    df_corr_corrected = pd.DataFrame(data={'fips': c_id, 'correlation': corr, 'year': year_corr})
    return df_corr_corrected

# calculate the mean corr for each county
def calc_mean_corr(counties, df_corr_corrected):
    '''
    Calculate the mean correlation between respiratory deaths and air pollution
    Input: County geographical information and loaded correlation data
    Output: Dataframe of mean correlation data
    '''

    mean_county_corr = []
    county_id = []
    for county in range(0, len(counties['features'])):
        if (counties['features'][county]['id'] in np.array(df_corr_corrected['fips'])):
            county_id.append(counties['features'][county]['id'])
            df_county_corr = df_corr_corrected[df_corr_corrected['fips'] == counties['features'][county]['id']]
            mean_county_corr.append(np.mean(np.array(df_county_corr['correlation'])))
        else:
            county_id.append(counties['features'][county]['id'])
            mean_county_corr.append(np.nan)

    df_mean_corr = pd.DataFrame(data={'fips': county_id, 'mean_correlation': mean_county_corr})
    return df_mean_corr

def load_deathrate(counties):
    '''
    load respiratory death rate data
    Input: County geographical information
    Output: Dataframe of respiratory deaths data
    '''
    # Death Rate dataframe
    df_dr = pd.read_csv("deathrate_countydata.csv", dtype={"fips": str})
    # append a zero infront of dataframe
    str_id = [] # convert county ids to strings and append a zero in front of those that are length four
    death_rate = []
    year = []
    for curr_id in range(0, len(df_dr['County Code'])):
        curr = str(df_dr['County Code'][curr_id])
        if len(curr) < 5:
            append_id = '0' + curr
            str_id.append(append_id)
            death_rate.append(df_dr['% of Total Deaths'][curr_id])
            adj_year = round((df_dr['Year'][curr_id]) + (df_dr['Month'][curr_id] / 13), 2)
            year.append(adj_year)
        else:
            str_id.append(str(df_dr['County Code'][curr_id]))
            death_rate.append(df_dr['% of Total Deaths'][curr_id])
            adj_year = round((df_dr['Year'][curr_id]) + (df_dr['Month'][curr_id] / 13), 2)
            year.append(adj_year)

    # Sub-dataframe for deathrate
    df_death_rate = pd.DataFrame({'fips': str_id, 'death rate': death_rate, 'year': year})
    return df_death_rate

def load_air_pollution(counties):
    '''
    load air pollution data
    Input: County geographical information
    Output: Dataframe of air pollution data
    '''
    # read in air pollution data
    df_air = pd.read_csv("combined_air_data_2000_2019.csv", dtype={"fips": str})

    # append a zero infront of dataframe
    str_id = [] # convert county ids to strings and append a zero in front of those that are length four
    aqi = []
    year = []
    for curr_id in range(0, len(df_air['county_code'])):
        curr = str(df_air['county_code'][curr_id])
        if len(curr) < 5:
            append_id = '0' + curr
            str_id.append(append_id)
            aqi.append(df_air['AQI'][curr_id])
            adj_year = round((df_air['year'][curr_id]) + (df_air['month'][curr_id]/13), 2)
            year.append(adj_year)
        else:
            str_id.append(str(df_air['county_code'][curr_id]))
            aqi.append(df_air['AQI'][curr_id])
            adj_year = round((df_air['year'][curr_id]) + (df_air['month'][curr_id]/13), 2)
            year.append(adj_year)

    # Sub-dataframe for air pollution data
    df_air_corrected = pd.DataFrame(data={'fips': str_id, 'AQI': aqi, 'year': year})
    return df_air_corrected
