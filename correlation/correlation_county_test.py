import pandas as pd
import os
from itertools import chain

pd_death_rate = pd.read_csv("death_rate.cvs")
pd_data_airquality = pd.read_csv("daily_aqi_by_county_2010.csv")

air_dict = dict()
DIR = "air_data"
'''
This python document is used to find the correlation
between air-polutions and the death rate
index is the mean value per month
the correlation method is by pearson
'''

def get_data_from_specifc_state(df, state_code):
    try:
        assert (state_code >= 0) & (state_code <= 100)
    except AssertionError as e:
        e.args += ('invalid state code', "check get_data_from_specifc_state function")
        raise

    try:
        assert 'County Code' in list(df.columns)
    except AssertionError as e:
        e.args += ('wrong data frame', "check get_data_from_specifc_state function")
        raise

    b = state_code*1000
    df2 = df.loc[(df["County Code"] > b) & (pd_death_rate["County Code"] < b+999)]
    return df2


def get_the_county_code_list(df):#for death data
    #get the county code list
    try:
        assert 'County Code' in list(df.columns)
    except AssertionError as e:
        e.args += ('wrong data frame', "check get_the_county_code_list function")
        raise

    a = df['County Code'].unique()
    return [x % 1000 for x in a]


def get_the_county_code_air_list(df, state):
    #for air data
    try:
        assert 'State Code' in list(df.columns)
    except AssertionError as e:
        e.args += ('Dataframe has no attribute called state Code', "check get_the_county_code_list function")
        raise
    df2 = df.loc[(df['State Code'] == state)]
    return df2['County Code'].unique()


def get_the_county_code_death_list(df, state):
    # get the air data list from the county code
    return get_the_county_code_list(get_data_from_specifc_state(df, state))


def get_county_code_common(df1, df2, state):
    '''
    df1:_air //for a specific year
    df2:_death
    output: the intersect between the two list
    '''
    try:
        assert type(state) is int
    except AssertionError as e:
        e.args += ('Wrong in put type (int expected)', "check get_county_code_common function")
        raise

    set1 = set(get_the_county_code_air_list(df1, state))
    set2 = set(get_the_county_code_death_list(df2, state))  # 与年无关
    return set1 & set2


def convert_county_code(digit5_2_two):
    '''
    input 5 digits
    return state & county seperately
    '''
    try:
        assert type(digit5_2_two) is int
        assert digit5_2_two >= 1000
    except AssertionError as e:
        e.args += ('Wrong input', "check convert_county_code function")
        raise
    state=int(digit5_2_two/1000)
    county = digit5_2_two%1000
    return state,county


def convert_county_code_2_2_5(state,county):
    '''
    input state & county seperately
    return 5 digits int
    '''
    try:
        assert state <= 100
        assert type(county) is int
        assert county <= 1000
    except AssertionError as e:
        e.args += ('Wrong input', "check convert_county_code function")
        raise
    digit2_2_5=state*1000+county
    return digit2_2_5


def get_the_month_air_data(df, countyCode, statecode, month, year):
    # year input type should be int, but when u do the test  it should be str
    #     code=statecode*1000+countyCode
    #     print(code)
    '''
    return:
    df2: orgnized data looked by the county code and the state code
    mean: the corresponding meanresult of the the year
    '''
    try:
        assert countyCode is int
        assert statecode <= 1000
        assert month <= 12
        assert year is int
    except AssertionError as e:
        e.args += ('Wrong input condition', "check get_the_month_air_data function")
        raise

    try:
        assert 'County Code' in list(df.columns)
        assert 'Date' in list(df.columns)
        assert 'AQI' in list(df.columns)
    except AssertionError as e:
        e.args += ('Wrong dataframe', "check get_the_month_air_data function")
        raise
    df2 = df.loc[(df["County Code"] == countyCode) & (df["State Code"] == statecode)]
    #   print(df2)
    if month >= 10:
        month_str = str(month)
    else:
        month_str = '0' + str(month)
    time = str(year) + '-' + month_str
    df2 = df2.loc[df2['Date'].str.match(time)]  #
    mean = df2['AQI'].mean()
    return df2, mean


def convert_int_5tostring(int_result):
    '''convert the 5 bit int digits to string type'''
    try:
        assert type(int_result) is int
    except AssertionError as e:
        e.args += ('Wrong in put type (int expected)', "check convert_int_5tostring function")
        raise
    if int_result<10000:
        res = '0'+str(int_result)
    else :
        res = str(int_result)
    return res


def find_cor_given_state(state):
    '''
    state is a number
    计算依据：mean()
    '''
    try:
        assert type(state) is int
    except AssertionError as e:
        e.args += ('Wrong in put type (int expected)', "check find_cor_given_state function")
        raise
    air_cor_list=[]
    year_list=[]
    list_county=[]
    list_state=[]

    for year in list_year:
        list_death_test=[]
        list_air_test=[]
        coun = get_county_code_common(air_dict[year],pd_death_rate,state)
        for kc in coun:#county loop
            for i in range(12):
                month=i+1;
                death_data=get_the_month_death_data(pd_death_rate, kc, state,month, year)

                _,air_data=get_the_month_air_data(air_dict[year], kc, state,month, year)
                if not death_data.empty:
                    if not np.isnan(air_data):
                        list_death_test.append(death_data.values[0])
                        list_air_test.append(air_data)
            if len(list_death_test) != 0:
                death = pd.Series(list_death_test)
                air = pd.Series(list_air_test)
                cor = air.corr(death,method="pearson")
                if not np.isnan(cor):
                    air_cor_list.append(cor)#append the valid correlation
                    year_list.append(year)
                    list_county.append(kc)
                    list_state.append(state)

    return air_cor_list, year_list, list_county, list_state


def throu_the_country():
    # get the result through out the country
    air_cor_list = []
    year_list = []
    county_list = []
    state_list = []

    for state in set_state_death:
        a, b, c, d = find_cor_given_state(state)
        air_cor_list.append(a)
        year_list.append(b)
        county_list.append(c)
        state_list.append(d)

    return air_cor_list, year_list, county_list, state_list


for year in list_year:
    # get all the datas in the dict
    assert "daily_aqi_by_county_"+str(year)+".csv" in os.listdir(DIR)
    air_dict[year] = pd.read_csv(DIR+"/daily_aqi_by_county_"+str(year)+".csv")


a1,b1,c1,d1 = throu_the_country()


a_chain = list(chain(*a1))
b_chain = list(chain(*b1))
c_chain = list(chain(*c1))
d_chain = list(chain(*d1))

count_code_list = []

for i in range(len(a_chain)):
    code = convert_county_code_2_2_5(d_chain[i], c_chain[i])
    count_code_list.append(conver_int_5tostring(code))

res=pd.DataFrame(list(zip(count_code_list,b_chain,a_chain)),
                 columns=['county_code', 'year', 'correlation'])
