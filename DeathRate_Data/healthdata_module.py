'''This module contains the functions used to clean up and merge the death rate data.'''
import pandas as pd

def changing_col_name(dataframe, name_before, name_after):
    '''This function changes the name of one column in an input dataframe and returns the dataframe.

    The column names must be input as strings.
    '''
    return dataframe.rename(columns={name_before: name_after})

def split_column(dataframe, column1, column2, column3, splitter):
    '''This function splits a column of strings into two columns with parts of each string.

    First this function creates a new dataframe that has one specified column..
    Then it adds two new columns to the original dataframe with the split values.
    (or replaces one of the original columns if the names are the same).
    The column name inputs must be strings.
    The splitter is the symbol or letter that is used to split the string.
    '''
    new_df = dataframe[column1].str.split(splitter, n=1, expand=True)
    dataframe[column2] = new_df[0]
    dataframe[column3] = new_df[1]
    return dataframe

def choose_data_by_year(dataframe, year):
    '''This function returns a dataframe that only contains data from a specified year.

    This function takes a dataframe as an input and the target year as an integer.
    It outputs a dataframe that contains only that specific year.
    It also specifies which columns we want to keep in the final dataframe.
    It renames the population column so that it does not have a year-specific name.
    '''
    return dataframe[['County', 'POPESTIMATE'+str(year), 'County Code', 'Deaths', 'Month', 'Month Code', 'State', 'Year']].loc[dataframe["Year"] == str(year)].rename(columns={'POPESTIMATE'+str(year):'Population'})

def concat_dfs_vertically(dataframe1, dataframe2):
    '''This function merges two dataframes vertically.
    It assumes they have the same column names already.
    '''
    return pd.concat([dataframe1, dataframe2])
