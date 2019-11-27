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
df_corr = pd.read_csv("export_cor.csv",
                   dtype={"fips": str})

# append a zero infront of dataframe
c_id=[] # convert county ids to strings and append a zero in front of those that are length four
corr=[]
year_corr=[]
for id in range(0,len(df_corr['county_code'])):
    curr_id=str(df_corr['county_code'][id])
    if len(curr_id) < 5:
        append_id='0'+curr_id
        c_id.append(append_id)
        corr.append(df_corr['correlation'][id])
        year_corr.append(df_corr['year'][id])
    else:
        c_id.append(str(df_corr['county_code'][id]))
        corr.append(df_corr['correlation'][id])
        year_corr.append(df_corr['year'][id])

# Sub-dataframe for AQI
df_corr_corrected=pd.DataFrame(data={'fips':c_id,'correlation':corr,'year':year_corr})

# choose a county
fip='25025'

# filter data by that county
df_corr_county=df_corr_corrected[df_corr_corrected['fips']==fip]

# calculate the mean corr for each county
mean_county_corr=[]
county_id=[]
for county in range(0,len(counties['features'])):
    if (counties['features'][county]['id'] in df_corr_corrected['fips']) == True:
        county_id.append(df_corr_corrected['fips'][df_corr_corrected['fips'].index(counties['features'][county]['id'])])
        df_county_corr=df_corr_corrected[df_corr_corrected['fips']==counties['features'][county]['id'] ]
        mean_county_corr.append(np.mean(df_county_corr['correlation']))
    else:
        county_id.append(counties['features'][county]['id'])
        mean_county_corr.append(np.nan)

df_mean_corr=pd.DataFrame(data={'fips':county_id,'mean_correlation':mean_county_corr})
