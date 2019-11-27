'''
This code generates the interactive map of the average correlation between repiratory deaths and air pollution across U.S. counties along with the assoicated time series data
'''
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
from plotly.callbacks import Points, InputDeviceState
points, state = Points(), InputDeviceState()

from ipywidgets import Output, VBox
from urllib.request import urlopen


# Load in county geographic data
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# create pandas dataframe of Predicted AQI data
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

# create adjusted aqi dataframe
df_all_aqi={'fips':county_id ,'aqi': county_aqi}

# read in respiratory death and air pollution correlation data
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

fig_corr = go.Figure(data=go.Scatter(x=df_corr_county['year'], y=df_corr_county['correlation'],mode='lines+markers',name='lines+markers'))
# find county name associated with fip
for name in range(0,len(counties['features'])):
    if fip == counties['features'][name]['id']:
        county_name=counties['features'][name]['properties']['NAME']
    else:
        pass
title_name='Correlation between respiratory deaths and air pollution, County: ' + county_name
fig_corr.update_layout(title=title_name,
               xaxis_title='Year',
               yaxis_title='Correlation')


# calculate the mean corr for each county
mean_county_corr=[]
county_id=[]
for county in range(0,len(counties['features'])):
    if (counties['features'][county]['id'] in np.array(df_corr_corrected['fips'])) == True:
        county_id.append(counties['features'][county]['id'])
        df_county_corr=df_corr_corrected[df_corr_corrected['fips']==counties['features'][county]['id']]
        mean_county_corr.append(np.mean(np.array(df_county_corr['correlation'])))
    else:
        county_id.append(counties['features'][county]['id'])
        mean_county_corr.append(np.nan)

df_mean_corr=pd.DataFrame(data={'fips':county_id,'mean_correlation':mean_county_corr})

f = go.FigureWidget([go.Choroplethmapbox(geojson=counties, locations=df_mean_corr['fips'], z=df_mean_corr['mean_correlation'],colorscale="Reds", zmin=min(df_mean_corr['mean_correlation']), zmax=max(df_mean_corr['mean_correlation']),
                                    marker_opacity=0.5, marker_line_width=0,colorbar_title="Mean Correlation")])

# Death Rate dataframe
df_dr = pd.read_csv("deathrate_countydata.csv",
                   dtype={"fips": str})
# append a zero infront of dataframe
str_id=[] # convert county ids to strings and append a zero in front of those that are length four
death_rate=[]
year=[]
for id in range(0,len(df_dr['County Code'])):
    curr_id=str(df_dr['County Code'][id])
    if len(curr_id) < 5:
        append_id='0'+curr_id
        str_id.append(append_id)
        death_rate.append(df_dr['% of Total Deaths'][id])
        adj_year=round((df_dr['Year'][id])+(df_dr['Month'][id]/13),2)
        year.append(adj_year)
        #year.append(round(df['Year'][id]+((df['Month'][id]/13))*df['Month'][id],2)) # adjust for month
    else:
        str_id.append(str(df_dr['County Code'][id]))
        death_rate.append(df_dr['% of Total Deaths'][id])
        adj_year=round((df_dr['Year'][id])+(df_dr['Month'][id]/13),2)
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
fig_deathrate = go.Figure(data=go.Scatter(x=df_sorted_death_rate['year'], y=df_sorted_death_rate['death rate'],mode='lines+markers',name='lines+markers'))
# find county name associated with fip
for name in range(0,len(counties['features'])):
    if fip == counties['features'][name]['id']:
        county_name=counties['features'][name]['properties']['NAME']
    else:
        pass
title_name='Respiratory Deaths, County: ' + county_name
fig_deathrate.update_layout(title=title_name,
               xaxis_title='Year',
               yaxis_title='% of Total Deaths')


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

f
f.update_layout(mapbox_style="carto-positron",mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129},
               title_text = 'Correlation Between Air Pollution and Respiratory Deaths', geo_scope='usa')

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#ffffff'
}

# Base Text for initialized county
# get the county name
for name in range(0,len(counties['features'])):
    if fip == counties['features'][name]['id']:
        county_name=counties['features'][name]['properties']['NAME']
    else:
        pass

# Get the AQI for that county
for id in range(0,len(df_all_aqi['fips'])):
    if fip == df_all_aqi['fips'][id]:
        aqi_val=str(df_all_aqi['aqi'][id])
    else:
        pass

updated_text='''
#### Predicted Air Quality Index (AQI)
###### A Keras Sequential model predicted the air quaity index for one day into the future given the prior air pollution and respiratory deaths.
###### AQI Ranges: (0-50: Good, 51-100: Moderate, 101-150: Unhealthy for sensitive groups, 151-200: Unhealthy, 201-300: Very unhealthy, 301-500: Hazardous)
County: ''' + county_name +'''

\n Predicted AQI: ''' + aqi_val+'''

\n Predicted Date: 11/21/2019 '''

app_text='''
Instructions: locate a U.S. county by panning and zooming on the U.S. map that displays the average correlation between repiratory deaths and air pollution in the upper left. Note that counties that did not have data avaliable are not included in the map.
Once a county is located, click on that county to display 1) the correlation between respiratory deaths and air pollution since 2000 (upper right), 2) the predicted air quality index given the prior respiratory deaths and air pollution (text under interactive map),
3) the air quality index (measure of air pollution) since 2000 (lower left), and 4) the percent of respiratory deaths since 2000 (lower right) for that county.

'''
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Correlation and predictive modeling between air pollution and respiratory death rates',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children=app_text, style={
        'textAlign': 'center',
        'color': colors['text'],
        'font-size': 14
    }),

    html.Div([
        dcc.Graph(id='correlation map',figure=f)
    ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20','height':'200%'}),

        html.Div([
            dcc.Graph(id='correlation',figure=fig_corr)
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20','height':'200%'}),

    html.Div([
        dcc.Markdown(id='predicted_aqi',children=updated_text)
    ],style={'width': '100%', 'display': 'inline-block', 'padding': '0 20','textAlign': 'center',
    'color': colors['text']}),

    html.Div([
        dcc.Graph(id='air_pollution',figure=fig_air_pollution),
    ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20'}),

    html.Div([
        dcc.Graph(id='respiratory_death_rate', figure=fig_deathrate),
    ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20'})


])

# callback for updating air pollution graph
@app.callback(
    dash.dependencies.Output('air_pollution', 'figure'),
    [dash.dependencies.Input('correlation map', 'clickData')])

def update_graph(clickData):
    # clicked upon fip id
    fip=str(clickData['points'][0]['location'])
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
    return fig_air_pollution

# Update the predicted aqi for a county
@app.callback(
   dash.dependencies.Output('predicted_aqi', 'children'),
   [dash.dependencies.Input('correlation map', 'clickData')])

def update_graph(clickData):
    # clicked upon fip id
    fip=str(clickData['points'][0]['location'])
    # get the county name
    for name in range(0,len(counties['features'])):
        if fip == counties['features'][name]['id']:
            county_name=counties['features'][name]['properties']['NAME']
        else:
            pass

    # Get the AQI for that county
    for id in range(0,len(df_all_aqi['fips'])):
        if fip == df_all_aqi['fips'][id]:
            aqi_val=str(df_all_aqi['aqi'][id])
        else:
            pass

    updated_text='''
    ## Predicted Air Quality Index (AQI)
    #### A Keras Sequential model predicted the air quaity index for one day into the future given the prior air pollution and respiratory deaths.
    ##### AQI Ranges: (0-50: Good, 51-100: Moderate, 101-150: Unhealthy for sensitive groups, 151-200: Unhealthy, 201-300: Very unhealthy, 301-500: Hazardous)
    County: ''' + county_name +'''

    \n Predicted AQI: ''' + aqi_val+'''

    \n Predicted Date: 11/21/2019 '''

    return updated_text

# call back for updating the correlation graph
@app.callback(
    dash.dependencies.Output('correlation', 'figure'),
    [dash.dependencies.Input('correlation map', 'clickData')])

def update_graph(clickData):
    # Use a fip code to filter the data by county
    county_death_rate=[]
    county_year=[]
    fip=str(clickData['points'][0]['location'])

    # filter data by that county
    df_corr_county=df_corr_corrected[df_corr_corrected['fips']==fip]

    fig_corr = go.Figure(data=go.Scatter(x=df_corr_county['year'], y=df_corr_county['correlation'],mode='lines+markers',name='lines+markers'))
    # find county name associated with fip
    for name in range(0,len(counties['features'])):
        if fip == counties['features'][name]['id']:
            county_name=counties['features'][name]['properties']['NAME']
        else:
            pass
    title_name='Correlation between respiratory deaths and air pollution, County: ' + county_name
    fig_corr.update_layout(title=title_name,
                   xaxis_title='Year',
                   yaxis_title='Correlation')
    return fig_corr

# call back for updating the death rate graph
@app.callback(
    dash.dependencies.Output('respiratory_death_rate', 'figure'),
    [dash.dependencies.Input('correlation map', 'clickData')])

def update_graph(clickData):
    # Use a fip code to filter the data by county
    county_death_rate=[]
    county_year=[]
    fip=str(clickData['points'][0]['location'])

    # update death rate data
    for id in range(0,len(df_death_rate['fips'])):
        if fip ==df_death_rate['fips'][id]:
            county_death_rate.append(df_death_rate['death rate'][id])
            county_year.append(df_death_rate['year'][id])
        else:
            pass

    # find county name associated with fip
    for name in range(0,len(counties['features'])):
        if fip == counties['features'][name]['id']:
            county_name=counties['features'][name]['properties']['NAME']
        else:
            pass
    title_name='Respiratory Deaths, County: ' + county_name

    # sort data so that it plots in ascending order
    df_adjusted_death_rate=pd.DataFrame({'year':county_year,'death rate':county_death_rate})
    df_sorted_death_rate=df_adjusted_death_rate.sort_values(by=['year'])
    fig_deathrate = go.Figure(data=go.Scatter(x=df_sorted_death_rate['year'], y=df_sorted_death_rate['death rate'],mode='lines+markers',name='lines+markers'))
    fig_deathrate.update_layout(title=title_name,
                   xaxis_title='Year',
                   yaxis_title='% of Total Deaths')
    return fig_deathrate


if __name__ == '__main__':
    app.run_server(debug=False)
