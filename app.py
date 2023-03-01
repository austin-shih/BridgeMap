from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# import df
df = pd.read_csv('data/processed/nbi_clean.csv')
df = df.drop(df[(df['eval_rating'] == -1)].index)
state = df['state'].unique()
route = np.append(df['route_type'].unique(), 'All')

# summary df
df_sum = df.loc[:,('state_code', 'eval_rating')]
df_sum = df_sum.groupby(['state_code'], as_index=False).mean()
df_sum['count'] = df.loc[:,('state_code', 'eval_rating')].groupby('state_code', as_index=False).count().iloc[:,1].tolist()

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col([html.H1("US Highway Bridge Map", style={'textAlign': 'start'}),
                 html.P("Dashboard to Visualize US Interstate, Numbered, and State highway bridges", 
                        style={'textAlign': 'start'})
        ], width=12)
    ),

    dbc.Row([
        dbc.Col([
            html.Label('State'),
            dcc.Dropdown(state, 'Alabama', id='state_sel'),

            html.Br(),
            html.Label('Highway'),
            dcc.Dropdown(route, 'All', id='highway_sel'),

            html.Br(),
            html.Label('Map Type'),
            dcc.Dropdown(['Heatmap', 'Scatterplot'], 'Heatmap', id='map_sel')
        ], width=3, style={"height": "100%"}),

        dbc.Col([
            dcc.Graph(id='us_map', figure={})
        ], width=9, style={"height": "100%"})  
    ], className="h-75")
], style={"height": "100vh"})

@app.callback(
    Output('us_map', 'figure'),
    Input('state_sel', 'value'),
    Input('highway_sel', 'value'),
    Input('map_sel', 'value')
)


def update_map(state, route, map):
    if map == 'Heatmap':
        fig = px.choropleth(df_sum, 
                            locations='state_code',
                            locationmode='USA-states',
                            scope='usa',
                            color='eval_rating',
                            color_continuous_scale="RdBu",
                            range_color=(4, 9),
                            center = {"lat": 38, "lon": -95.7129},
                            labels={'eval_rating':'Mean Bridge Rating'},
                            height = 600
        )
        
        fig.update_layout(
            title_text = 'Mean Highway Bridge Evaluation Rating',
            margin={"r":0,"t":60,"l":0,"b":0}
        )

    else:
        dff = df[df['state']== state]
        if route != 'All':
            dff = dff[dff['route_type'] == route]

        fig = px.scatter_mapbox(dff, 
                                lat="latitude", lon="longitude", 
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
                                range_color = [0, 9],
                                color_continuous_scale="rdbu", 
                                opacity=1,
                                zoom=5, height=800)

        fig.update_layout(
            mapbox_style="open-street-map",
            title_text = 'Highway Bridges by State',
            margin={"r":0,"t":50,"l":0,"b":0}
        )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
