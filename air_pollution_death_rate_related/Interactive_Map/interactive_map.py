'''
Interactive map of repiratory deaths and air pollution across U.S. counties
'''

import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.callbacks import Points, InputDeviceState
from urllib.request import urlopen
POINTS, STATE = Points(), InputDeviceState()

# Load in county geographic data
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    COUNTIES = json.load(response)

# create pandas dataframe of Predicted AQI data
DF = pd.read_csv("predicted_AQI2019-03-12.csv", dtype={"fips": str})

# append a zero infront of dataframe
STRID = [] # convert county ids to strings and append a zero in front of those that are length four
AQI = []
for ID in range(0, len(DF['County Code'])):
    CURR = str(DF['County Code'][ID])
    if len(CURR) < 5:
        APPEND_ID = '0' + CURR
        STRID.append(APPEND_ID)
        AQI.append(DF['AQI'][ID])
    else:
        STRID.append(str(DF['County Code'][ID]))
        AQI.append(DF['AQI'][ID])

# Sub-dataframe for AQI
DF_AQI = {'fips':STRID, 'aqi':AQI}

COUNTY_ID = []
COUNTY_AQI = []

for COUNTY in range(0, len(COUNTIES['features'])):
    if (COUNTIES['features'][COUNTY]['id'] in DF_AQI['fips']):
        COUNTY_ID.append(DF_AQI['fips'][DF_AQI['fips'].index(COUNTIES['features'][COUNTY]['id'])])
        COUNTY_AQI.append(DF_AQI['aqi'][DF_AQI['fips'].index(COUNTIES['features'][COUNTY]['id'])])
    else:
        COUNTY_ID.append(COUNTIES['features'][COUNTY]['id'])
        COUNTY_AQI.append(0)

# create adjusted aqi dataframe
DF_ALL_AQI = {'fips': COUNTY_ID, 'aqi': COUNTY_AQI}

# read in respiratory death and air pollution correlation data
DF_CORR = pd.read_csv("export_cor.csv", dtype={"fips": str})

# append a zero infront of dataframe
C_ID = [] # convert county ids to strings and append a zero in front of those that are length four
CORR = []
YEAR_CORR = []
for ID in range(0, len(DF_CORR['county_code'])):
    CURR = str(DF_CORR['county_code'][ID])
    if len(CURR) < 5:
        APPEND_ID = '0' + CURR
        C_ID.append(APPEND_ID)
        CORR.append(DF_CORR['correlation'][ID])
        YEAR_CORR.append(DF_CORR['year'][ID])
    else:
        C_ID.append(str(DF_CORR['county_code'][ID]))
        CORR.append(DF_CORR['correlation'][ID])
        YEAR_CORR.append(DF_CORR['year'][ID])

# Sub-dataframe for orrelation results between respiratory death rates and air pollution
DF_CORR_CORRECTED = pd.DataFrame(data={'fips': C_ID, 'correlation': CORR, 'year': YEAR_CORR})

# choose an initial county
FIP = '25025'

# filter data by that county
DF_CORR_COUNTY = DF_CORR_CORRECTED[DF_CORR_CORRECTED['fips'] == FIP]

FIG_CORR = go.Figure(data=go.Scatter(x=DF_CORR_COUNTY['year'], y=DF_CORR_COUNTY['correlation'], mode='lines+markers', name='lines+markers'))

# find county name associated with fip
for NAME in range(0, len(COUNTIES['features'])):
    if FIP == COUNTIES['features'][NAME]['id']:
        COUNTY_NAME = COUNTIES['features'][NAME]['properties']['NAME']
    else:
        pass
TITLE_NAME = 'Correlation between respiratory deaths and air pollution, County: ' + COUNTY_NAME
FIG_CORR.update_layout(title=TITLE_NAME, xaxis_title='Year', yaxis_title='Correlation')
FIG_CORR.update_yaxes(range=[-1, 1])

# calculate the mean corr for each county
MEAN_COUNTY_CORR = []
COUNTY_ID = []
for COUNTY in range(0, len(COUNTIES['features'])):
    if (COUNTIES['features'][COUNTY]['id'] in np.array(DF_CORR_CORRECTED['fips'])):
        COUNTY_ID.append(COUNTIES['features'][COUNTY]['id'])
        DF_COUNTY_CORR = DF_CORR_CORRECTED[DF_CORR_CORRECTED['fips'] == COUNTIES['features'][COUNTY]['id']]
        MEAN_COUNTY_CORR.append(np.mean(np.array(DF_COUNTY_CORR['correlation'])))
    else:
        COUNTY_ID.append(COUNTIES['features'][COUNTY]['id'])
        MEAN_COUNTY_CORR.append(np.nan)

DF_MEAN_CORR = pd.DataFrame(data={'fips': COUNTY_ID, 'mean_correlation': MEAN_COUNTY_CORR})

F = go.FigureWidget([go.Choroplethmapbox(geojson=COUNTIES, locations=DF_MEAN_CORR['fips'], z=DF_MEAN_CORR['mean_correlation'], colorscale="Reds", zmin=min(DF_MEAN_CORR['mean_correlation']), zmax=max(DF_MEAN_CORR['mean_correlation']), marker_opacity=0.5, marker_line_width=0, colorbar_title="Mean Correlation")])

# Death Rate dataframe
DF_DR = pd.read_csv("deathrate_countydata.csv", dtype={"fips": str})
# append a zero infront of dataframe
STR_ID = [] # convert county ids to strings and append a zero in front of those that are length four
DEATH_RATE = []
YEAR = []
for ID in range(0, len(DF_DR['County Code'])):
    CURR = str(DF_DR['County Code'][ID])
    if len(CURR) < 5:
        APPEND_ID = '0' + CURR
        STR_ID.append(APPEND_ID)
        DEATH_RATE.append(DF_DR['% of Total Deaths'][ID])
        ADJ_YEAR = round((DF_DR['Year'][ID]) + (DF_DR['Month'][ID] / 13), 2)
        YEAR.append(ADJ_YEAR)
    else:
        STR_ID.append(str(DF_DR['County Code'][ID]))
        DEATH_RATE.append(DF_DR['% of Total Deaths'][ID])
        ADJ_YEAR = round((DF_DR['Year'][ID]) + (DF_DR['Month'][ID] / 13), 2)
        YEAR.append(ADJ_YEAR)

# Sub-dataframe for deathrate
DF_DEATH_RATE = pd.DataFrame({'fips': STR_ID, 'death rate': DEATH_RATE, 'year': YEAR})

# Use a fip code to filter the data by county
COUNTY_DEATH_RATE = []
COUNTY_YEAR = []
FIP = '25025'
for ID in range(0, len(DF_DEATH_RATE['fips'])):
    if FIP == DF_DEATH_RATE['fips'][ID]:
        COUNTY_DEATH_RATE.append(DF_DEATH_RATE['death rate'][ID])
        COUNTY_YEAR.append(DF_DEATH_RATE['year'][ID])
    else:
        pass

DF_ADJUSTED_DEATH_RATE = pd.DataFrame({'year': COUNTY_YEAR, 'death rate': COUNTY_DEATH_RATE})
DF_SORTED_DEATH_RATE = DF_ADJUSTED_DEATH_RATE.sort_values(by=['year'])
FIG_DEATHRATE = go.Figure(data=go.Scatter(x=DF_SORTED_DEATH_RATE['year'], y=DF_SORTED_DEATH_RATE['death rate'], mode='lines+markers', name='lines+markers'))

# find county name associated with fip
for NAME in range(0, len(COUNTIES['features'])):
    if FIP == COUNTIES['features'][NAME]['id']:
        COUNTY_NAME = COUNTIES['features'][NAME]['properties']['NAME']
    else:
        pass

TITLE_NAME = 'Respiratory Deaths, County: ' + COUNTY_NAME
FIG_DEATHRATE.update_layout(title=TITLE_NAME, xaxis_title='Year', yaxis_title='% of Total Deaths')

# read in air pollution data
DF_AIR = pd.read_csv("combined_air_data_2000_2019.csv", dtype={"fips": str})

# append a zero infront of dataframe
STR_ID = [] # convert county ids to strings and append a zero in front of those that are length four
AQI = []
YEAR = []
for ID in range(0, len(DF_AIR['county_code'])):
    CURR = str(DF_AIR['county_code'][ID])
    if len(CURR) < 5:
        APPEND_ID = '0' + CURR
        STR_ID.append(APPEND_ID)
        AQI.append(DF_AIR['AQI'][ID])
        ADJ_YEAR = round((DF_AIR['year'][ID]) + (DF_AIR['month'][ID]/13), 2)
        YEAR.append(ADJ_YEAR)
    else:
        STR_ID.append(str(DF_AIR['county_code'][ID]))
        AQI.append(DF_AIR['AQI'][ID])
        ADJ_YEAR = round((DF_AIR['year'][ID]) + (DF_AIR['month'][ID]/13), 2)
        YEAR.append(ADJ_YEAR)

# Sub-dataframe for air pollution data
DF_AIR_CORRECTED = pd.DataFrame(data={'fips': STR_ID, 'AQI': AQI, 'year': YEAR})

# Initialize with a particular fip id
FIP = '25025'
DF_COUNTY_AIR_POLLUTION = DF_AIR_CORRECTED[DF_AIR_CORRECTED['fips'] == FIP]

# create the air pollution figure
FIG_AIR_POLLUTION = go.Figure(data=go.Scatter(x=DF_COUNTY_AIR_POLLUTION['year'], y=DF_COUNTY_AIR_POLLUTION['AQI'], mode='lines+markers', name='lines+markers'))

# find county name associated with fip
for NAME in range(0, len(COUNTIES['features'])):
    if FIP == COUNTIES['features'][NAME]['id']:
        COUNTY_NAME = COUNTIES['features'][NAME]['properties']['NAME']
    else:
        pass

TITLE_NAME = 'Air Pollution, County: ' + COUNTY_NAME
FIG_AIR_POLLUTION.update_layout(title=TITLE_NAME, xaxis_title='Year', yaxis_title='Air Quality Index')

# Display mean correlation across U.S. counties
F.update_layout(mapbox_style="carto-positron", mapbox_zoom=3, mapbox_center={"lat": 37.0902, "lon": -95.7129}, title_text='Correlation Between Air Pollution and Respiratory Deaths', geo_scope='usa')

# Interactive interface global parameters
STYLES = {'pre': {'border': 'thin lightgrey solid', 'overflowX': 'scroll'}}

EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

APP = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)

COLORS = {'background': '#111111', 'text': '#ffffff'}

# Base Text for initialized county
# get the county name
for NAME in range(0, len(COUNTIES['features'])):
    if FIP == COUNTIES['features'][NAME]['id']:
        COUNTY_NAME = COUNTIES['features'][NAME]['properties']['NAME']
    else:
        pass

# Get the AQI for that county
for ID in range(0, len(DF_ALL_AQI['fips'])):
    if FIP == DF_ALL_AQI['fips'][ID]:
        AQI_VAL = str(DF_ALL_AQI['aqi'][ID])
    else:
        pass

UPDATED_TEXT = '''
#### Predicted Air Quality Index (AQI)
###### A Keras Sequential model predicted the air quaity index for one day into the future given the prior air pollution and respiratory deaths.
###### AQI Ranges: (0-50: Good, 51-100: Moderate, 101-150: Unhealthy for sensitive groups, 151-200: Unhealthy, 201-300: Very unhealthy, 301-500: Hazardous)
County: ''' + COUNTY_NAME +'''

\n Predicted AQI: ''' + AQI_VAL +'''

\n Predicted Date: 03/19/2019 '''

APP_TEXT = '''
Instructions: locate a U.S. county by panning and zooming on the U.S. map that displays the average correlation between respiratory deaths and air pollution in the upper left. Note that counties that did not have data available are not included in the map.
Once a county is located, click on that county to display 1) the correlation between respiratory deaths and air pollution since 2000 (upper right), 2) the predicted air quality index given the prior respiratory deaths and air pollution (text under interactive map),
3) the air quality index (measure of air pollution) since 2000 (lower left), and 4) the percent of respiratory deaths since 2000 (lower right) for that county.

'''
APP.layout = html.Div(style={'backgroundColor': COLORS['background']}, children=[
    # Title of interactive interface
    html.H1(
        children='Correlation and predictive modeling of air pollution and respiratory deaths',
        style={'textAlign': 'center', 'color': COLORS['text']}
    ),

    # Sub heading describing the interface
    html.Div(children=APP_TEXT, style={
        'textAlign': 'center',
        'color': COLORS['text'],
        'font-size': 14
    }),

    # Interactive map of the mean correlation across U.S. counties
    html.Div([
        dcc.Graph(id='correlation map', figure=F)
    ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20', 'height':'200%'}),

    # Time series of the correlation of a U.S. country
    html.Div([
        dcc.Graph(id='correlation', figure=FIG_CORR)
    ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20', 'height':'200%'}),

    # Descriptive text of the predicted AQI
    html.Div([
        dcc.Markdown(id='predicted_aqi', children=UPDATED_TEXT)
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20', 'textAlign': 'center', 'color': COLORS['text']}),

    # Time Series of the air pollution of a U.S. county
    html.Div([
        dcc.Graph(id='air_pollution', figure=FIG_AIR_POLLUTION),
    ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20'}),

    # Time series of the respiratory death rate of a U.S. county
    html.Div([
        dcc.Graph(id='respiratory_death_rate', figure=FIG_DEATHRATE),
    ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20'})
])

# callback for updating air pollution graph
@APP.callback(dash.dependencies.Output('air_pollution', 'figure'), [dash.dependencies.Input('correlation map', 'clickData')])

def update_graph(clickData):
    '''
    Update air pollution graph upon clicking on a U.S. county
    '''
    # clicked upon fip id
    fip_curr = str(clickData['points'][0]['location'])
    df_air = DF_AIR_CORRECTED[DF_AIR_CORRECTED['fips'] == fip_curr]

    # create the air pollution figure
    fig_air = go.Figure(data=go.Scatter(x=df_air['year'], y=df_air['AQI'], mode='lines+markers', name='lines+markers'))

    # find county name associated with fip
    for name in range(0, len(COUNTIES['features'])):
        if fip_curr == COUNTIES['features'][name]['id']:
            county_name = COUNTIES['features'][name]['properties']['NAME']
        else:
            pass

    title_name = 'Air Pollution, County: ' + county_name
    fig_air.update_layout(title=title_name, xaxis_title='Year', yaxis_title='Air Quality Index')

    return fig_air

# Update the predicted aqi for a county
@APP.callback(dash.dependencies.Output('predicted_aqi', 'children'), [dash.dependencies.Input('correlation map', 'clickData')])

def update_graph(clickData):
    '''
    Update predicted AQI text
    '''
    # clicked upon fip id
    fip_curr = str(clickData['points'][0]['location'])

    # get the county name
    for name in range(0, len(COUNTIES['features'])):
        if fip_curr == COUNTIES['features'][name]['id']:
            county_name = COUNTIES['features'][name]['properties']['NAME']
        else:
            pass

    # Get the AQI for that county
    for curr_id in range(0, len(DF_ALL_AQI['fips'])):
        if fip_curr == DF_ALL_AQI['fips'][curr_id]:
            aqi_val = str(DF_ALL_AQI['aqi'][curr_id])
        else:
            pass

    txt = '''
    #### Predicted Air Quality Index (AQI)
    ###### A Keras Sequential model predicted the air quality index for one day into the future given the prior air pollution and respiratory deaths.
    ###### AQI Ranges: (0-50: Good, 51-100: Moderate, 101-150: Unhealthy for sensitive groups, 151-200: Unhealthy, 201-300: Very unhealthy, 301-500: Hazardous)
    County: ''' + county_name +'''

    \n Predicted AQI: ''' + aqi_val +'''

    \n Predicted Date: 03/19/2019 '''

    return txt

# call back for updating the correlation graph
@APP.callback(dash.dependencies.Output('correlation', 'figure'), [dash.dependencies.Input('correlation map', 'clickData')])

def update_graph(clickData):
    '''
    Update time series correlation graph
    '''
    # clicked upon fip id
    fip_curr = str(clickData['points'][0]['location'])
    # filter data by that county
    # filter data by that county
    df_corr = DF_CORR_CORRECTED[DF_CORR_CORRECTED['fips'] == fip_curr]

    fig_corr = go.Figure(data=go.Scatter(x=df_corr['year'], y=df_corr['correlation'], mode='lines+markers', name='lines+markers'))

    # find county name associated with fip
    for name in range(0, len(COUNTIES['features'])):
        if fip_curr == COUNTIES['features'][name]['id']:
            county_name = COUNTIES['features'][name]['properties']['NAME']
        else:
            pass
    title_name = 'Correlation between respiratory deaths and air pollution, County: ' + county_name
    fig_corr.update_layout(title=title_name, xaxis_title='Year', yaxis_title='Correlation')
    fig_corr.update_yaxes(range=[-1, 1])
    return fig_corr

# call back for updating the death rate graph
@APP.callback(dash.dependencies.Output('respiratory_death_rate', 'figure'), [dash.dependencies.Input('correlation map', 'clickData')])

def update_graph(clickData):
    '''
    Update time series of respiratory death rates graph
    '''
    # clicked upon fip id
    fip_curr = str(clickData['points'][0]['location'])
    # Use a fip code to filter the data by county
    death_rate = []
    county_year = []
    for curr_id in range(0, len(DF_DEATH_RATE['fips'])):
        if fip_curr == DF_DEATH_RATE['fips'][curr_id]:
            death_rate.append(DF_DEATH_RATE['death rate'][curr_id])
            county_year.append(DF_DEATH_RATE['year'][curr_id])
        else:
            pass

    adjusted_dr = pd.DataFrame({'year': county_year, 'death rate': death_rate})
    sorted_dr = adjusted_dr.sort_values(by=['year'])
    fig_dr = go.Figure(data=go.Scatter(x=sorted_dr['year'], y=sorted_dr['death rate'], mode='lines+markers', name='lines+markers'))

    # find county name associated with fip
    for name in range(0, len(COUNTIES['features'])):
        if fip_curr == COUNTIES['features'][name]['id']:
            county_name = COUNTIES['features'][name]['properties']['NAME']
        else:
            pass

    title_name = 'Respiratory Deaths, County: ' + county_name
    fig_dr.update_layout(title=title_name, xaxis_title='Year', yaxis_title='% of Total Deaths')
    return fig_dr


if __name__ == '__main__':
    APP.run_server(debug=False)
