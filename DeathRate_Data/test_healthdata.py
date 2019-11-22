'''Tests the health data files'''
import pandas as pd
import numpy as np
import os
import healthdata_cleanup

#Checking the data files
#Check the individual health data files downloaded from the CDC
#Check that dataframe has at least one row
def test_rows():
     for file in os.listdir('county_data'):
        new_year = pd.read_csv('county_data/' + file, sep='\t', na_filter = False)
        assert(len(new_year.index)>=1)

#Testing that the relevant columns are in the dataframe
def test_correct_columns():
    col_names = ['County', 'County Code', 'Deaths', 'Month', 'Month Code']
    for file in os.listdir('county_data'):
        new_year = pd.read_csv('county_data/' + file, sep='\t', na_filter = False)
        for name in (col_names):
            assert (name in list(new_year.columns))

#Check the state abbrevs data
#Check whether 50 states are present plus DC
def test_states():
    assert (len(healthdata_cleanup.STATE_ABREVS.index) == 51)

#Check the population data
#Check whether every column has same type throughout
def test_every_col_2000():
    for col in healthdata_cleanup.STATE_POPS_2000:
        type0 = type(healthdata_cleanup.STATE_POPS_2000[col][0])
        for row in healthdata_cleanup.STATE_POPS_2000.index:
            assert (type(healthdata_cleanup.STATE_POPS_2000[col][row]) == type0)

def test_every_col_2010():
    for col in healthdata_cleanup.STATE_POPS_2010:
        type0 = type(healthdata_cleanup.STATE_POPS_2010[col][0])
        for row in healthdata_cleanup.STATE_POPS_2010.index:
            assert (type(healthdata_cleanup.STATE_POPS_2010[col][row]) == type0)

#Testing the final .csv file of integrated data
#Check for nan values
def test_nan_check():
    assert (healthdata_cleanup.ALL_YEARS.isnull().values.any() == False)

def test_every_col_final():
    for col in healthdata_cleanup.ALL_YEARS:
        type0 = type(healthdata_cleanup.ALL_YEARS[col][0])
        for row in healthdata_cleanup.ALL_YEARS.index:
            assert (type(healthdata_cleanup.ALL_YEARS[col][row]) == type0)

#Testing that specific columns have a specific type
def test_correct_type_code():
    type0 = str
    for row in healthdata_cleanup.ALL_YEARS.index:
        assert(type(healthdata_cleanup.ALL_YEARS['County Code'][row]) == type0)

#Testing that specific columns have a specific type
def test_correct_type_deaths():
    type0 = np.float64
    for row in healthdata_cleanup.ALL_YEARS.index:
        assert(type(healthdata_cleanup.ALL_YEARS['% of Total Deaths'][row]) == type0)
