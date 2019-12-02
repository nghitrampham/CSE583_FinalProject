'''Imports the death rate, population, and state name datasets and merges them. '''
import os
import pandas as pd
import numpy as np
from . import healthdata_module as hm

##Importing datasets as dataframes

#dataframe of state names and abbreviations
STATE_ABREVS = pd.read_csv(r'../Data/state_abrevs/state_abrevs.csv', sep=',')

#Dataframe of state populations from 2000-2010
STATE_POPS_2000 = pd.read_csv('../Data/population_data/co-est00int-tot.csv', encoding='latin-1')
#Dataframe of state populations from 2010-2018
STATE_POPS_2010 = pd.read_csv('../Data/population_data/co-est2018-alldata.csv', encoding='latin-1')

#Importing the .csv files for death rates from each year and merging them into one df
COUNTIES_DATA = pd.DataFrame()
for file in os.listdir('../Data/county_data'):
    new_year = pd.read_csv('../Data/county_data/' + file, sep='\t', na_filter=False)
    COUNTIES_DATA = pd.concat([COUNTIES_DATA, new_year], axis=0, sort=True)

#Getting rid of extra columns in death rates df
COL_NAMES = ['Notes', 'Population', 'Crude Rate', '% of Total Deaths']
COUNTIES_DATA = COUNTIES_DATA.drop(columns=COL_NAMES)

#Splitting up column values into two columns in death rates df
COUNTIES_DATA = hm.split_column(COUNTIES_DATA, 'County', 'County', 'State Abr', ',')
COUNTIES_DATA = hm.split_column(COUNTIES_DATA, 'Month Code', 'Year', 'Month', '/')

#Changing the column name to match in the health data frame
STATE_ABREVS = hm.changing_col_name(STATE_ABREVS, 'State Abrev', 'State Abr')

#removing the extra space from before the string in the state abrevs column
COUNTIES_DATA['State Abr'] = COUNTIES_DATA['State Abr'].str.lstrip()

#Making both the state abbreviation columns utf-8 encoding
COUNTIES_DATA['State Abr'] = COUNTIES_DATA['State Abr'].str.encode('utf-8')
STATE_ABREVS['State Abr'] = STATE_ABREVS['State Abr'].str.encode('utf-8')

#Merging the county health data and the state abbreviations
COUNTY_DATA_MERGE = pd.merge(COUNTIES_DATA, STATE_ABREVS, on=['State Abr'])

#Dropping extra State column that contains Nans
COUNTY_DATA_MERGE = COUNTY_DATA_MERGE.drop(columns=['State_x', 'State Code'])

#Change column name
COUNTY_DATA_MERGE = hm.changing_col_name(COUNTY_DATA_MERGE, 'State_y', 'State')

#Changing column names to match between death rates and population dataframes
STATE_POPS_2010 = hm.changing_col_name(STATE_POPS_2010, 'CTYNAME', 'County')
STATE_POPS_2000 = hm.changing_col_name(STATE_POPS_2000, 'CTYNAME', 'County')
STATE_POPS_2010 = hm.changing_col_name(STATE_POPS_2010, 'STNAME', 'State')
STATE_POPS_2000 = hm.changing_col_name(STATE_POPS_2000, 'STNAME', 'State')

#Merging county population data for 2000 and 2010 with county death rates
COUNTY_POP_MERGE = pd.merge(STATE_POPS_2010, COUNTY_DATA_MERGE, on=['County', 'State'])
COUNTY_POP_MERGE_2000 = pd.merge(STATE_POPS_2000, COUNTY_DATA_MERGE, on=['County', 'State'])

#Getting all the data for each year in individual dataframes and then combining the new data frames
ALL_YEARS = pd.DataFrame()
for year in range(2010, 2018):
    new_df = hm.choose_data_by_year(COUNTY_POP_MERGE, year)
    ALL_YEARS = hm.concat_dfs_vertically(ALL_YEARS, new_df)
for year in range(2000, 2010):
    new_df = hm.choose_data_by_year(COUNTY_POP_MERGE_2000, year)
    all_years = hm.concat_dfs_vertically(ALL_YEARS, new_df)

#Calculating the % of total deaths
ALL_YEARS['% of Total Deaths'] = np.int64(ALL_YEARS['Deaths'])/ALL_YEARS['Population']

#Creating a new column that changes the units to make them easier to deal with
ALL_YEARS['% of Total Deaths (x10^6)'] = ALL_YEARS['% of Total Deaths'] * 1000000

#Save file  to a .csv file
ALL_YEARS.to_csv('deathrate_countydata.csv', index=None, header=True)
