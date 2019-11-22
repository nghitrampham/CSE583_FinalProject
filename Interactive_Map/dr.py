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

print(counties['features'][1]['properties']['NAME'])
print(counties['features'][:]['id'])

# create pandas dataframe of AQI data
df = pd.read_csv("deathrate_countydata.csv",
                   dtype={"fips": str})
# append a zero infront of dataframe
str_id=[] # convert county ids to strings and append a zero in front of those that are length four
death_rate=[]
year=[]
for id in range(0,len(df['County Code'])):
    curr_id=str(df['County Code'][id])
    if len(curr_id) < 5:
        append_id='0'+curr_id
        str_id.append(append_id)
        death_rate.append(df['% of Total Deaths'][id])
        adj_year=round((df['Year'][id])+(df['Month'][id]/13),2)
        year.append(adj_year)
        #year.append(round(df['Year'][id]+((df['Month'][id]/13))*df['Month'][id],2)) # adjust for month
    else:
        str_id.append(str(df['County Code'][id]))
        death_rate.append(df['% of Total Deaths'][id])
        adj_year=round((df['Year'][id])+(df['Month'][id]/13),2)
        year.append(adj_year)
        #year.append(round(df['Year'][id]+((df['Month'][id]/13))*df['Month'][id],2))
# Sub-dataframe for deathrate
df_death_rate=pd.DataFrame({'fips':str_id,'death rate':death_rate, 'year': year})

# Use a fip code to filter the data by county
county_death_rate=[]
county_year=[]
fip='25025'
for id in range(0,len(df_death_rate['fips'])):
    if fip ==df_death_rate['fips'][id]:
        county_death_rate.append(df_death_rate['death rate'][id])
        county_year.append(df_death_rate['year'][id])
    else:
        pass

df_adjusted_death_rate=pd.DataFrame({'year':county_year,'death rate':county_death_rate})
df_sorted_death_rate=df_adjusted_death_rate.sort_values(by=['year'])
fig = go.Figure(data=go.Scatter(x=df_sorted_death_rate['year'], y=df_sorted_death_rate['death rate'],mode='lines+markers',name='lines+markers'))
fig.show()
