'''Tests the functions in healthdata_module.py'''
import pandas as pd
import healthdata_module
import healthdata_cleanup

#Test data
df1 = pd.read_csv('test_data_1.csv')
df2 = pd.read_csv('test_data_2.csv')

def test_func_changing_names():
    '''Testing the first function, renaming columns.'''
    df_renamed = healthdata_module.changing_col_name(df1, 'Year', 'year')
    assert 'year' in list(df_renamed.columns)
    assert 'Year' not in list(df_renamed.columns)

def test_func_split_col():
    '''Testing the second function, splitting a column value into two strings.'''
    df_split = healthdata_module.split_column(df2, 'County', 'County', 'State Abrev', ',')
    assert 'State Abrev' in list(df_split.columns)
    assert ' WA' in list(df_split['State Abrev'])
    assert 'King' in list(df_split['County'])

def test_func_choose_data():
    '''Testing the third function, choosing data by year.'''
    df_2015 = healthdata_module.choose_data_by_year(healthdata_cleanup.COUNTY_POP_MERGE, 2015)
    assert '2015' in list(df_2015['Year'])
    assert '2001' not in list(df_2015['Year'])

def test_func_concat():
    '''Testing the fourth function, which concatenates the functions vertically.'''
    df_concat = healthdata_module.concat_dfs_vertically(df1, df2)
    assert len(df_concat) == 4
