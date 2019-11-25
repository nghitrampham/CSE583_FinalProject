'''Tests the health data files'''
import os
import pandas as pd
import numpy as np
import healthdata_cleanup

#Checking the data files
#Check the individual health data files downloaded from the CDC
#Check that dataframe has at least one row
def test_rows():
    '''Testing that each dataframe has at least one row'''
    for file in os.listdir('county_data'):
        new_year = pd.read_csv('county_data/' + file, sep='\t', na_filter=False)
        assert len(new_year.index) >= 1

#Testing that the relevant columns are in the dataframe
def test_correct_columns():
    '''Testing that the relevant columns are in the dataframe'''
    col_names = ['County', 'County Code', 'Deaths', 'Month', 'Month Code']
    for file in os.listdir('county_data'):
        new_year = pd.read_csv('county_data/' + file, sep='\t', na_filter=False)
        for name in col_names:
            assert name in list(new_year.columns)

#Check the state abbrevs data
#Check whether 50 states are present plus DC
def test_states():
    '''Testing that there are the correct number of rows'''
    assert len(healthdata_cleanup.STATE_ABREVS.index) == 51

#Check the population data
#Check whether every column has same type throughout
def test_every_col_2000():
    '''Testing that each column has the same type throughout'''
    for col in healthdata_cleanup.STATE_POPS_2000:
        type0 = type(healthdata_cleanup.STATE_POPS_2000[col][0])
        for row in healthdata_cleanup.STATE_POPS_2000.index:
            assert isinstance(healthdata_cleanup.STATE_POPS_2000[col][row]) == type0

def test_every_col_2010():
    '''Testing that each column has the same type throughout'''
    for col in healthdata_cleanup.STATE_POPS_2010:
        type0 = type(healthdata_cleanup.STATE_POPS_2010[col][0])
        for row in healthdata_cleanup.STATE_POPS_2010.index:
            assert isinstance(healthdata_cleanup.STATE_POPS_2010[col][row]) == type0

#Testing the final .csv file of integrated data
#Check for nan values
def test_nan_check():
    '''Testing for nans'''
    assert healthdata_cleanup.ALL_YEARS.isnull().values.any() == False

def test_every_col_final():
    '''Testing that every column has the same type throughout'''
    for col in healthdata_cleanup.ALL_YEARS:
        type0 = type(healthdata_cleanup.ALL_YEARS[col][0])
        for row in healthdata_cleanup.ALL_YEARS.index:
            assert isinstance(healthdata_cleanup.ALL_YEARS[col][row]) == type0

#Testing that specific columns have a specific type
def test_correct_type_code():
    '''Testing taht specific columns have a specific type'''
    type0 = str
    for row in healthdata_cleanup.ALL_YEARS.index:
        asserttype(healthdata_cleanup.ALL_YEARS['County Code'][row]) == type0

#Testing that specific columns have a specific type
def test_correct_type_deaths():
    '''Testing that columns have a specific type'''
    type0 = np.float64
    for row in healthdata_cleanup.ALL_YEARS.index:
        assert type(healthdata_cleanup.ALL_YEARS['% of Total Deaths'][row]) == type0
