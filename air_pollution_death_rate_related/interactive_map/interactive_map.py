'''
Interactive map of repiratory deaths and air pollution across U.S. counties
Note: naming conventions confirmed by pylint
'''

import json
from urllib.request import urlopen
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from plotly.callbacks import Points, InputDeviceState
import plotly.graph_objects as go
import load_data
POINTS, STATE = Points(), InputDeviceState()

def county(counties, fip_curr):
    '''
    Determine county name
    Input: county information and fip ID
    Output: county name
    '''
    # find county name associated with fip
    for name in range(0, len(counties['features'])):
        if fip_curr == counties['features'][name]['id']:
            county_name = counties['features'][name]['properties']['NAME']
        else:
            pass
    return county_name

# Load in county geographic data
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    COUNTIES = json.load(response)
# load all datasets
# predicted aqi
DF_ALL_AQI = load_data.load_predicted_aqi(COUNTIES)

# correlation between respiratory deaths and air pollution
DF_CORR_CORRECTED = load_data.load_correlation(COUNTIES)

# calculate mean correlation
DF_MEAN_CORR = load_data.calc_mean_corr(COUNTIES, DF_CORR_CORRECTED)

# respiratory death rate
DF_DEATH_RATE = load_data.load_deathrate(COUNTIES)

# air pollution
DF_AIR_CORRECTED = load_data.load_air_pollution(COUNTIES)

# choose an initial county
FIP = '25025'

# filter data by that county
DF_CORR_COUNTY = DF_CORR_CORRECTED[DF_CORR_CORRECTED['fips'] == FIP]

# correlation figure
FIG_CORR = go.Figure(data=go.Scatter(x=DF_CORR_COUNTY['year'], y=DF_CORR_COUNTY['correlation'], mode='lines+markers', name='lines+markers'))

# find county name associated with fip
COUNTY_NAME = county(COUNTIES, FIP)
TITLE_NAME = 'Correlation between respiratory deaths and air pollution, County: ' + COUNTY_NAME
FIG_CORR.update_layout(title=TITLE_NAME, xaxis_title='Year', yaxis_title='Correlation')
FIG_CORR.update_yaxes(range=[-1, 1])

# respiratory deaths figure
COUNTY_DEATH_RATE = []
COUNTY_YEAR = []
for ID in range(0, len(DF_DEATH_RATE['fips'])):
    if FIP == DF_DEATH_RATE['fips'][ID]:
        COUNTY_DEATH_RATE.append(DF_DEATH_RATE['death rate'][ID])
        COUNTY_YEAR.append(DF_DEATH_RATE['year'][ID])
    else:
        pass

DF_ADJUSTED_DEATH_RATE = pd.DataFrame({'year': COUNTY_YEAR, 'death rate': COUNTY_DEATH_RATE})
DF_SORTED_DEATH_RATE = DF_ADJUSTED_DEATH_RATE.sort_values(by=['year'])

TITLE_NAME = 'Respiratory Deaths, County: ' + COUNTY_NAME
FIG_DEATHRATE = go.Figure(data=go.Scatter(x=DF_SORTED_DEATH_RATE['year'], y=DF_SORTED_DEATH_RATE['death rate'], mode='lines+markers', name='lines+markers'))
FIG_DEATHRATE.update_layout(title=TITLE_NAME, xaxis_title='Year', yaxis_title='% of Total Deaths')

# air pollution figure
DF_COUNTY_AIR_POLLUTION = DF_AIR_CORRECTED[DF_AIR_CORRECTED['fips'] == FIP]

# create the air pollution figure
FIG_AIR_POLLUTION = go.Figure(data=go.Scatter(x=DF_COUNTY_AIR_POLLUTION['year'], y=DF_COUNTY_AIR_POLLUTION['AQI'], mode='lines+markers', name='lines+markers'))
TITLE_NAME = 'Air Pollution, County: ' + COUNTY_NAME
FIG_AIR_POLLUTION.update_layout(title=TITLE_NAME, xaxis_title='Year', yaxis_title='Air Quality Index')

# Display mean correlation across U.S. counties
F = go.FigureWidget([go.Choroplethmapbox(geojson=COUNTIES, locations=DF_MEAN_CORR['fips'], z=DF_MEAN_CORR['mean_correlation'], colorscale="Reds", zmin=min(DF_MEAN_CORR['mean_correlation']), zmax=max(DF_MEAN_CORR['mean_correlation']), marker_opacity=0.5, marker_line_width=0, colorbar_title="Mean Correlation")])
F.update_layout(mapbox_style="carto-positron", mapbox_zoom=3, mapbox_center={"lat": 37.0902, "lon": -95.7129}, title_text='Correlation Between Air Pollution and Respiratory Deaths', geo_scope='usa')

# Interactive interface global parameters
STYLES = {'pre': {'border': 'thin lightgrey solid', 'overflowX': 'scroll'}}

EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

APP = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)

COLORS = {'background': '#111111', 'text': '#ffffff'}

# Base Text for initialized county for predicted aqi
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

def update_air_graph(click_data):
    '''
    Update air pollution graph upon clicking on a U.S. county
    Input: FIP ID
    Output: Updated county name and air pollution time series
    '''
    # clicked upon fip id
    fip_curr = str(click_data['points'][0]['location'])
    df_air = DF_AIR_CORRECTED[DF_AIR_CORRECTED['fips'] == fip_curr]

    # create the air pollution figure
    fig_air = go.Figure(data=go.Scatter(x=df_air['year'], y=df_air['AQI'], mode='lines+markers', name='lines+markers'))
    county_name = county(COUNTIES, fip_curr)
    title_name = 'Air Pollution, County: ' + county_name
    fig_air.update_layout(title=title_name, xaxis_title='Year', yaxis_title='Air Quality Index')

    return fig_air

# Update the predicted aqi for a county
@APP.callback(dash.dependencies.Output('predicted_aqi', 'children'), [dash.dependencies.Input('correlation map', 'clickData')])

def update_aqi_graph(click_data):
    '''
    Update predicted AQI text
    Input: FIP ID
    Output: Updated county name and predicted AQI value
    '''
    # clicked upon fip id
    fip_curr = str(click_data['points'][0]['location'])

    # get the county name
    county_name = county(COUNTIES, fip_curr)

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

def update_corr_graph(click_data):
    '''
    Update time series correlation graph
    Input: FIP ID
    Output: Updated county name and correlation
    '''
    # clicked upon fip id
    fip_curr = str(click_data['points'][0]['location'])
    # filter data by that county
    # filter data by that county
    df_corr = DF_CORR_CORRECTED[DF_CORR_CORRECTED['fips'] == fip_curr]

    fig_corr = go.Figure(data=go.Scatter(x=df_corr['year'], y=df_corr['correlation'], mode='lines+markers', name='lines+markers'))
    county_name = county(COUNTIES, fip_curr)
    title_name = 'Correlation between respiratory deaths and air pollution, County: ' + county_name
    fig_corr.update_layout(title=title_name, xaxis_title='Year', yaxis_title='Correlation')
    fig_corr.update_yaxes(range=[-1, 1])
    return fig_corr

# call back for updating the death rate graph
@APP.callback(dash.dependencies.Output('respiratory_death_rate', 'figure'), [dash.dependencies.Input('correlation map', 'clickData')])

def update_death_graph(click_data):
    '''
    Update time series of respiratory death rates graph
    Input: FIP ID
    Output: Updated county name and percent deaths time series
    '''
    # clicked upon fip id
    fip_curr = str(click_data['points'][0]['location'])
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
    county_name = county(COUNTIES, fip_curr)
    title_name = 'Respiratory Deaths, County: ' + county_name
    fig_dr.update_layout(title=title_name, xaxis_title='Year', yaxis_title='% of Total Deaths')
    return fig_dr

if __name__ == '__main__':
    APP.run_server(debug=False)
