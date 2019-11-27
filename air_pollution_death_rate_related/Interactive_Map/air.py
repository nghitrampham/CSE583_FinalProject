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



# read in respiratory death and air pollution correlation data
df_air= pd.read_csv("combined_air_data_2000_2019.csv",
                   dtype={"fips": str})
# append a zero infront of dataframe
str_id=[] # convert county ids to strings and append a zero in front of those that are length four
aqi=[]
year=[]
for id in range(0,len(df_air['county_code'])):
    curr_id=str(df_air['county_code'][id])
    if len(curr_id) < 5:
        append_id='0'+curr_id
        str_id.append(append_id)
        aqi.append(df_air['AQI'][id])
        adj_year=round((df_air['year'][id])+(df_air['month'][id]/13),2)
        year.append(adj_year)
        #year.append(round(df['Year'][id]+((df['Month'][id]/13))*df['Month'][id],2)) # adjust for month
    else:
        str_id.append(str(df_air['county_code'][id]))
        aqi.append(df_air['AQI'][id])
        adj_year=round((df_air['year'][id])+(df_air['month'][id]/13),2)
        year.append(adj_year)
        #year.append(round(df['Year'][id]+((df['Month'][id]/13))*df['Month'][id],2))
# Sub-dataframe for deathrate
df_air_corrected=pd.DataFrame(data={'fips':str_id,'AQI':aqi, 'year': year})

# Use a fip code to filter the data by county

fip='25025'
df_county_air_pollution=df_air_corrected[df_air_corrected['fips']==fip]

# create the air pollution figure
fig_air_pollution = go.Figure(data=go.Scatter(x=df_county_air_pollution['year'], y=df_county_air_pollution['AQI'],mode='lines+markers',name='lines+markers'))
# find county name associated with fip
for name in range(0,len(counties['features'])):
    if fip == counties['features'][name]['id']:
        county_name=counties['features'][name]['properties']['NAME']
    else:
        pass
title_name='Air Pollution, County: ' + county_name
fig_air_pollution.update_layout(title=title_name,
               xaxis_title='Year',
               yaxis_title='Air Quality Index')
