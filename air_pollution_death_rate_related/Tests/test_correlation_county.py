'''
This module is used for the test for the correlation_county.py
pylint 8.06/10
'''

import pandas as pd
import numpy as np
from ..Scripts import correlation_county

DF_TEST_DEATH = pd.read_csv("air_pollution_death_rate_related/Data/deathrate_countydata.csv")
DF_TEST_AIR = pd.read_csv("air_pollution_death_rate_related/Data/" +
                          "Air_Pollution/data_air_raw/daily_aqi_by_county_2010.csv")


def test_get_data_from_specifc_state():
    # :return: test get_data_from_specifc_state()

    res = correlation_county.get_data_from_specifc_state(DF_TEST_DEATH, 12)
    assert len(res.columns) == 10


def test_get_the_county_code_list():
    # :return: test result for test_get_the_county_code_list()
    df2 = correlation_county.get_data_from_specifc_state(DF_TEST_DEATH, 12)
    testdata = correlation_county.get_the_county_code_list(df2)
    for ele in testdata:
        assert isinstance(ele, np.int64)
        assert ele < 1000


def test_get_the_county_code_air_list():
    testdata = correlation_county.get_the_county_code_air_list(DF_TEST_AIR, 12)
    for data in testdata:
        assert isinstance(data, type(testdata[0]))


def test_get_the_county_code_death_list():
    df2 = correlation_county.get_data_from_specifc_state(DF_TEST_DEATH, 12)
    testdata = correlation_county.get_the_county_code_death_list(df2, 12)
    for data in testdata:
        assert isinstance(data, type(testdata[0]))
        assert not np.isnan(data)


def test_get_county_code_common():
    res = correlation_county.get_county_code_common(DF_TEST_AIR, DF_TEST_DEATH, 13)
    assert isinstance(res, set)
    for element in res:
        assert isinstance(element, np.int64)
        assert not np.isnan(element)


def test_convert_county_code():
    df1 = correlation_county.get_data_from_specifc_state(DF_TEST_DEATH, 13)
    for element in df1['County Code']:
        res1, res2 = correlation_county.convert_county_code(element)
        assert res1 < 100
        assert res2 < 1000


def test_convert_county_code_2_2_5():
    res = correlation_county.convert_county_code_2_2_5(12, 530)
    assert res > 1000
    assert res == 12530


def test_get_the_month_air_data():
    res1, res2 = correlation_county.get_the_month_air_data(DF_TEST_AIR, 21, 12, 2, 2010)
    assert len(res1.columns) == 10
    assert not np.isnan(res2)
    assert res2 > 0


def test_get_the_month_death_data():
    res = correlation_county.get_the_month_death_data(DF_TEST_DEATH, 21, 12, 2, 2010)
    assert isinstance(res.values[0], np.float64)


def test_convert_int_5tostring():
    df1 = correlation_county.get_data_from_specifc_state(DF_TEST_DEATH, 13)
    for ele in df1['County Code']:
        res = correlation_county.convert_int_5tostring(ele)
        assert isinstance(res, str)
        assert len(res) == 4 | len(res) == 5


def test_find_cor_given_state():
    res1, res2, res3, res4 = correlation_county.find_cor_given_state(DF_TEST_AIR,
                                                                     DF_TEST_DEATH, 2010, 12)
    assert len(res1) == len(res2) == len(res3) == len(res4)
    for ele in range(len(res1)):
        assert isinstance(res1[ele], type(res1[0]))
        assert isinstance(res2[ele], type(res2[0]))
        assert isinstance(res3[ele], type(res3[0]))
        assert isinstance(res4[ele], type(res4[0]))
