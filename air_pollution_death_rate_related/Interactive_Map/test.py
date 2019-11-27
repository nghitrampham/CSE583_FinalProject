import dash
import dash_core_components as dcc
import dash_html_components as html
import chart_studio
import json

from textwrap import dedent as d
import chart_studio.plotly as py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from ipywidgets import Output, VBox
from urllib.request import urlopen


# Load in county geographic data
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# create pandas dataframe of AQI data
df = pd.read_csv("AQI_sample.csv",
                   dtype={"fips": str})

# append a zero infront of dataframe
str_id=[] # convert county ids to strings and append a zero in front of those that are length four
aqi=[]
for id in range(0,len(df['County Code'])):
    curr_id=str(df['County Code'][id])
    if len(curr_id) < 5:
        append_id='0'+curr_id
        str_id.append(append_id)
        aqi.append(df['AQI'][id])
    else:
        str_id.append(str(df['County Code'][id]))
        aqi.append(df['AQI'][id])

# Sub-dataframe for AQI
df_aqi={'fips':str_id,'aqi':aqi}

county_id=[]
county_aqi=[]

for county in range(0,len(counties['features'])):
    if (counties['features'][county]['id'] in df_aqi['fips']) == True:
        county_id.append(df_aqi['fips'][df_aqi['fips'].index(counties['features'][county]['id'])])
        county_aqi.append(df_aqi['aqi'][df_aqi['fips'].index(counties['features'][county]['id'])])
    else:
        county_id.append(counties['features'][county]['id'])
        county_aqi.append(0)

# create adjusted ai dataframe
df_all_aqi={'fips':county_id ,'aqi': county_aqi}
