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

# create adjusted aqi dataframe
df_all_aqi={'fips':county_id ,'aqi': county_aqi}

f = go.FigureWidget([go.Choroplethmapbox(geojson=counties, locations=df_all_aqi['fips'], z=df_all_aqi['aqi'],colorscale="Reds", zmin=0, zmax=max(df_all_aqi['aqi']),
                                    marker_opacity=0.5, marker_line_width=0,colorbar_title="AQI")])


# Death Rate dataframe
# create pandas dataframe of AQI data
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
title_name='County: ' + county_name
fig_deathrate.update_layout(title=title_name,
               xaxis_title='Year',
               yaxis_title='% of Total Deaths')


from plotly.callbacks import Points, InputDeviceState
points, state = Points(), InputDeviceState()


f
f.update_layout(mapbox_style="carto-positron",mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129},
               title_text = 'Air Quality Index Per U.S. County', geo_scope='usa')

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
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='U.S. Map',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='emplyment rate map', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='interactive map',
        figure=f
    ),

    html.Div([
        dcc.Graph(id='air_pollution'),
    ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20'}),

    html.Div([
        dcc.Graph(id='respiratory_death_rate', figure=fig_deathrate),
    ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20'})


])

@app.callback(
    dash.dependencies.Output('air_pollution', 'figure'),
    [dash.dependencies.Input('interactive map', 'clickData')])

def update_graph(clickData):
    return f.update_layout(mapbox_style="carto-positron",mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129},
                   title_text = 'hi', geo_scope='usa')

# call back for updating the death rate graph
@app.callback(
    dash.dependencies.Output('respiratory_death_rate', 'figure'),
    [dash.dependencies.Input('interactive map', 'clickData')])

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
    title_name='County: ' + county_name

    # sort data so that it plots in ascending order
    df_adjusted_death_rate=pd.DataFrame({'year':county_year,'death rate':county_death_rate})
    df_sorted_death_rate=df_adjusted_death_rate.sort_values(by=['year'])
    fig_deathrate = go.Figure(data=go.Scatter(x=df_sorted_death_rate['year'], y=df_sorted_death_rate['death rate'],mode='lines+markers',name='lines+markers'))
    fig_deathrate.update_layout(title=title_name,
                   xaxis_title='Year',
                   yaxis_title='% of Total Deaths')
    return fig_deathrate


if __name__ == '__main__':
    app.run_server(debug=True)
