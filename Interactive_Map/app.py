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

# create pandas dataframe of specified data
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})

# plot us map

f = go.FigureWidget([go.Choroplethmapbox(geojson=counties, locations=df.fips, z=df.unemp,colorscale="Viridis", zmin=0, zmax=12,
                                    marker_opacity=0.5, marker_line_width=0,colorbar_title="% unemployed")])
map=f.data[0]
from plotly.callbacks import Points, InputDeviceState
points, state = Points(), InputDeviceState()

f
f.update_layout(mapbox_style="carto-positron",mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129},
               title_text = 'Unemployment Rate', geo_scope='usa')

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
        dcc.Graph(id='respiratory_death_rate'),
    ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20'}),

    html.Div([
        dcc.Markdown(d("""
            **Click Data**

            Click on points in the graph.
        """)),
        html.Pre(id='click-data', style=styles['pre']),
    ], className='three columns'),

    html.Div(id='fip_ids',children='Hello world')

])

@app.callback(
    dash.dependencies.Output('air_pollution', 'figure'),
    [dash.dependencies.Input('interactive map', 'clickData')])

def update_graph(clickData):
    return f.update_layout(mapbox_style="carto-positron",mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129},
                   title_text = 'hi', geo_scope='usa')
@app.callback(
    dash.dependencies.Output('click-data', 'children'),
    [dash.dependencies.Input('interactive map', 'clickData')])

def display_click_data(clickData):
    return json.dumps(clickData , indent=2)

@app.callback(
    dash.dependencies.Output('fip_ids', 'children'),
    [dash.dependencies.Input('interactive map', 'clickData')])

def display_click_data(clickData):
    fip_id=clickData['points']
    return str(fip_id[0]['location']) # gets the fip id from clicked upon county



if __name__ == '__main__':
    app.run_server(debug=True)
