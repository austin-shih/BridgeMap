from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
#import geopandas as gpd
import shapely.geometry
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# import bridge dataframe
df = pd.read_csv('data/processed/nbi_clean.csv')
# change county FIPS to string and pad string
df['fips'] = df['fips'].map(str)
df['fips'] = df['fips'].str.zfill(5)
state = np.append(df['state_name'].unique(), 'All')          # initial state options
route = np.append(df['route_type'].unique(), 'All')     # inital route options


app.layout = dbc.Container([
    html.H1("US Highway Bridge Map", style={'textAlign': 'start'}),
    dcc.Tabs([
        dcc.Tab(label='Heatmap', children=[
            dbc.Row(
                dbc.Col([html.H4("Heatmap Bridge Evaluation by County", style={'textAlign': 'start'}),
                html.P("Dashboard to Visualize US Interstate, Numbered, and State highway bridges", 
                        style={'textAlign': 'start'})
                ], width=12)
            ),
            dbc.Row([
                dbc.Col([
                    html.Label('State'),
                    dcc.Dropdown(state, 'All', id='state_sel1'),

                    html.Br(),
                    html.Label('Highway'),
                    dcc.Dropdown(route, 'All', id='highway_sel1'),

                ], width=3, style={"height": "100%"}),
                dbc.Col([
                    dcc.Graph(id='us_map_heatmap', figure={})
                ], width=9, style={"height": "100%"})  
            ], className="h-75")
        ]),

        dcc.Tab(label='Scatterplot', children=[
            dbc.Row(
                dbc.Col([html.H4("Scatterplot", style={'textAlign': 'start'}),
                html.P("Dashboard to Visualize US Interstate, Numbered, and State highway bridges", 
                        style={'textAlign': 'start'})
                ], width=12)
            ),
            dbc.Row([
                dbc.Col([
                    html.Label('State'),
                    dcc.Dropdown(state, 'All', id='state_sel2'),

                    html.Br(),
                    html.Label('Highway'),
                    dcc.Dropdown(route, 'All', id='highway_sel2'),

                ], width=3, style={"height": "100%"}),
                dbc.Col([
                    dcc.Graph(id='us_map_scatter', figure={})
                ], width=9, style={"height": "100%"})  
            ], className="h-75")
        ])#, style={"height": "100vh"})
    ])
])

@app.callback(
    Output('us_map_heatmap', 'figure'),
    Input('state_sel1', 'value'),
    Input('highway_sel1', 'value')
)
def update_map(state, route):
    # filter dataframe
    dff = df

    # df with state lat long centres
    df_state_cen = dff.loc[:,('state_name', 'longitude', 'latitude')]
    df_state_cen = df_state_cen.groupby(['state_name'], as_index=False).mean()

    if state != 'All':
        dff = df[df['state_name']== state]
        df_state_cen = df_state_cen[df_state_cen['state_name']==state]
        if route != 'All':
            dff = dff[dff['route_type'] == route]
    elif route != 'All':
        dff = dff[dff['route_type'] == route]

    # summary df
    df_sum = dff.drop(dff[(dff['eval_rating'] == -1)].index)
    df_sum = df_sum.loc[:, ('fips', 'state_abv', 'state_name', 'eval_rating', 'latitude', 'longitude')]
    df_sum = df_sum.groupby(['fips', 'state_abv', 'state_name'], as_index=False).mean()
    df_sum['count'] = dff.loc[:,('fips', 'eval_rating')].groupby('fips', as_index=False).count().iloc[:,1].tolist()

    if state == 'All':
        lat = 38
        long = -95.7129
        centre = {"lat": lat, "lon": long}
        zoom = 3
    else:
        lat = df_state_cen.iloc[0]['latitude']
        long = df_state_cen.iloc[0]['longitude']
        centre = {"lat": lat, "lon": long}
        zoom = 5

    fig = px.choropleth_mapbox(df_sum, 
                                geojson=counties, 
                                locations='fips', 
                                color='eval_rating',
                                color_continuous_scale="RdBu",
                                range_color=(4, 9),
                                mapbox_style="carto-positron",
                                zoom=zoom, 
                                center = centre,
                                hover_name='fips',
                                hover_data=['eval_rating', 'count'],
                                height = 600
                                #labels={'unemp':'unemployment rate'}
    )

    fig.update_layout(
        title_text = 'Mean Highway Bridge Evaluation Rating',
        coloraxis_colorbar=dict(title="Bridge Evaluation Rate", 
                                thicknessmode="pixels", 
                                lenmode="pixels", 
                                yanchor="top",y=1, 
                                ticks="outside", 
                                tickvals=[0,1,2,3,4,5,6,7,8,9],
                                ticktext=['0-Failed', '1-"Imminent" Failure', 
                                            '2-Critical', '3-Serious',
                                            '4-Poor', '5-Fair', '6-Satisfactory',
                                            '7-Good', '8-Very Good', '9-Excellent'],
                                dtick=10
                                ),
        margin={"r":0,"t":60,"l":0,"b":0}
    )

    return fig

@app.callback(
    Output('us_map_scatter', 'figure'),
    Input('state_sel2', 'value'),
    Input('highway_sel2', 'value')
)
def update_map(state, route):
    # filter dataframe
    dff = df

    # df with state lat long centres
    df_state_cen = dff.loc[:,('state_name', 'longitude', 'latitude')]
    df_state_cen = df_state_cen.groupby(['state_name'], as_index=False).mean()

    # dff_geo = df_geo
    if state != 'All':
        dff = df[df['state_name']== state]
        df_state_cen = df_state_cen[df_state_cen['state_name']==state]
        if route != 'All':
            dff = dff[dff['route_type'] == route]
    elif route != 'All':
        dff = dff[dff['route_type'] == route]

    # summary df
    df_sum = dff.drop(dff[(dff['eval_rating'] == -1)].index)
    df_sum = df_sum.loc[:, ('fips', 'state_abv', 'state_name', 'eval_rating', 'latitude', 'longitude')]
    df_sum = df_sum.groupby(['fips', 'state_abv', 'state_name'], as_index=False).mean()
    df_sum['count'] = dff.loc[:,('fips', 'eval_rating')].groupby('fips', as_index=False).count().iloc[:,1].tolist()

    if state == 'All':
        lat = 38
        long = -95.7129
        centre = {"lat": lat, "lon": long}
        zoom = 3
    else:
        lat = df_state_cen.iloc[0]['latitude']
        long = df_state_cen.iloc[0]['longitude']
        centre = {"lat": lat, "lon": long}
        zoom = 5

    # scatter plot
    fig = px.scatter_mapbox(dff, 
                            lat='latitude', lon='longitude', 
                            hover_name="feature_intersect", 
                            hover_data=['eval_rating', 
                                        "eval_rating_v", 
                                        "bridge_material", 
                                        "bridge_type",
                                        'appr_material',
                                        'appr_type',
                                        'num_span',
                                        'num_appr',
                                        'max_span',
                                        'bridge_length',
                                        'bridge_width'],
                            color='eval_rating',
                            size=dff['bridge_length']*50,
                            size_max=30,
                            range_color = [0, 9],
                            color_continuous_scale="rdbu", 
                            opacity=1,
                            zoom=zoom,
                            height=800,
                            mapbox_style="open-street-map"
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        title_text = 'Highway Bridges by State',
        coloraxis_colorbar=dict(title="Bridge Evaluation Rate", 
                                thicknessmode="pixels", 
                                lenmode="pixels", 
                                yanchor="top",y=1, 
                                ticks="outside", 
                                tickvals=[0,1,2,3,4,5,6,7,8,9],
                                ticktext=['0-Failed', '1-"Imminent" Failure', 
                                            '2-Critical', '3-Serious',
                                            '4-Poor', '5-Fair', '6-Satisfactory',
                                            '7-Good', '8-Very Good', '9-Excellent'],
                                dtick=10
                                ),
        margin={"r":0,"t":50,"l":0,"b":0}
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
