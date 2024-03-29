from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# # load json county file
# j = pd.read_json('data/processed/geojson-counties-fips.json')
# counties = {
#     'type': 'FeatureCollection',
#     'features': j['features'].to_list()
# }

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server 

# import bridge dataframe
df = pd.read_csv('https://raw.githubusercontent.com/austin-shih/bridgemap_data/main/data/processed/nbi_clean.csv', 
                        dtype = {"eval_rating_v":'category', "route_type":"category", 'eval_rating': np.int8, 'deck_condition': np.int8,
                                   'superstructure_condition': np.int8, 'substructure_condition': np.int8, 'fips': np.int32,
                                   'year_built': np.int16, 'num_span': np.int16, 'max_span': np.float16, 'bridge_length':np.float32,
                                   'bridge_width': np.float16})

# df = pd.read_csv('data/processed/nbi_clean.csv')
# change county FIPS to string and pad string
df['fips'] = df['fips'].map(str)
df['fips'] = df['fips'].str.zfill(5)
state = np.append(df['state_name'].unique(), 'All')             # initial state options
route = np.append(df['route_type'].unique(), 'All')             # initial route options
route_num = np.append(df['route_num'].unique(), 'All')          # initial route number options
bridge_type = np.append(df['bridge_type'].unique(), 'All')      # initial bridge type options
bridge_mat = np.append(df['bridge_material'].unique(), 'All')   # initial bridge material options

# function to update length slide to log scale
def transform_value(value):
    if value == 0:
        val_tran = 0
    else:
        val_tran = 10**value
    return val_tran

# about evaulation tables
table_header1 = [
html.Thead(html.Tr([html.Th("Code"), html.Th("Verbose"), html.Th("Description")]))
]
row11 = html.Tr([html.Td("9"), html.Td("Excellent"), html.Td("Excellent Condition")])
row12 = html.Tr([html.Td("8"), html.Td("Very Good"), html.Td("No problems noted")])
row13 = html.Tr([html.Td("7"), html.Td("Good"), html.Td("Some minor problems")])
row14 = html.Tr([html.Td("6"), html.Td("Satisfactory"), html.Td("Structural elements show some minor deterioration.")])
row15 = html.Tr([html.Td("5"), html.Td("Fair"), html.Td("All primary structural elements are sound but may have minor section loss, cracking, spalling or scour.")])
row16 = html.Tr([html.Td("4"), html.Td("Poor"), html.Td("Advanced section loss, deterioration, spalling or scour.")])
row17 = html.Tr([html.Td("3"), html.Td("Serious"), html.Td("Loss of section, deterioration, spalling or scour have seriously affected primary structural components. Local failures are possible. Fatigue cracks in steel or shear cracks in concrete may be present.")])
row18 = html.Tr([html.Td("2"), html.Td("Critical"), html.Td("Advanced deterioration of primary structural elements. Fatigue cracks in steel or shear cracks in concrete may be present or scour may have removed substructure support. Unless closely monitored it may be necessary to close the bridge until corrective action is taken.")])
row19 = html.Tr([html.Td("1"), html.Td("'IMMINENT' Failure"), html.Td("Major deterioration or section loss present in critical structural components or obvious vertical or horizontal movement affecting structure stability. Bridge is closed to traffic but corrective action may put back in light service.")])
row10 = html.Tr([html.Td("0"), html.Td("Failed"), html.Td("Out of service - beyond corrective action.")])
table_body1 = [html.Tbody([row11, row12, row13, row14, row15, row16, row17, row18, row19, row10])]

table_header2 = [
html.Thead(html.Tr([html.Th("Code"), html.Th("Description")]))
]
row21 = html.Tr([html.Td("9"), html.Td("Superior to present desirable criteria")])
row22 = html.Tr([html.Td("8"), html.Td("Equal to present desirable criteria")])
row23 = html.Tr([html.Td("7"), html.Td("Better than present minimum criteria")])
row24 = html.Tr([html.Td("6"), html.Td("Equal to present minimum criteria")])
row25 = html.Tr([html.Td("5"), html.Td("Somewhat better than minimum adequacy to tolerated being left in place as is")])
row26 = html.Tr([html.Td("4"), html.Td("Meets minimum tolerable limits to be left in place as is")])
row27 = html.Tr([html.Td("3"), html.Td("Basically intolerable requiring high priority of corrective action")])
row28 = html.Tr([html.Td("2"), html.Td("Basically intolerable requiring high priority of replacement")])
row29 = html.Tr([html.Td("1"), html.Td("This value of rating code not used")])
row20 = html.Tr([html.Td("0"), html.Td("Bridge closed")])
table_body2 = [html.Tbody([row21, row22, row23, row24, row25, row26, row27, row28, row29, row20])]

app.layout = dbc.Container([
    html.H1("US Highway Bridge Map", style={'textAlign': 'start'}),
    html.P("Dashboard to Visualize US Interstate, Numbered, and State highway bridges from the National Bridge Inventory Database", 
           style={'textAlign': 'start'}),

    dcc.Tabs([
        dcc.Tab(label='Scatterplot', children=[
            dbc.Row([
                dbc.Col([
                    # count of bridges from filter
                    html.Br(),
                    html.Div(id='bridge_count2'),
                    html.Div(id='eval_avg2'),
                    # dropdown for states
                    html.Br(),
                    html.Label('State'),
                    dcc.Dropdown(state, 'All', id='state_sel2', clearable=False, multi=True),
                    # dropdown for highway type
                    html.Br(),
                    html.Label('Highway'),
                    dcc.Dropdown(route, 'Interstate highway', id='highway_sel2', clearable=False),
                    # dropdown for highway number
                    html.Br(),
                    html.Label('Highway Number'),
                    dcc.Dropdown(route_num, 'All', id='hwy_num2'),
                    # dropdown for bridge type
                    html.Br(),
                    html.Label('Bridge Type'),
                    dcc.Dropdown(bridge_type, 'All', id='type_sel2', clearable=False),
                    # slider for year built
                    html.Br(),
                    html.Label('Year Built'),
                    dcc.RangeSlider(1697, 2023,
                                    id='year_slider2',
                                    marks=None,
                                    value=[1697, 2023],
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    dots=False,
                                    step=1,
                                    allowCross=False),
                    # slider for bridge length
                    html.Br(),
                    html.Label('Bridge length (m)'),
                    dcc.RangeSlider(0, 5,
                                    id='length_slider2',
                                    marks={i: '{}'.format(transform_value(i)) for i in range(6)},
                                    value=[0, 5],
                                    dots=False,
                                    step=0.01,
                                    allowCross=False),
                    html.Div(id='bridge_length2',  style={'font-size': 10}),
                    # slider for number of spans
                    html.Br(),
                    html.Label('Number of Spans'),
                    dcc.RangeSlider(0, 771,
                                    id='span_slider2',
                                    marks=None,
                                    value=[0, 771],
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    dots=False,
                                    step=1,
                                    allowCross=False),
                    # slider for evaluation rating
                    html.Br(),
                    html.Label('Evaluation Rating'),
                    dcc.RangeSlider(-1, 9, 1, value=[-1, 9], id='eval_slider2', allowCross=False),
                    html.Div('* -1 for bridges without rating', style={'font-size': 10})

                ], width=3, style={"height": "100%"}),   
                dbc.Col([
                    html.Br(),
                    html.H4("Highway Bridges Scatterplot (bubble size by length)", style={'textAlign': 'start'}),
                    dcc.Graph(id='us_map_scatter', figure={}, style={'height':'70vh'}),
                    html.Div('Data accessed January 13, 2023. Latest version can be found below:', style={'font-size': 12}),
                    dcc.Link(html.A('USDOT BTS'), id='data_link2',  href="https://geodata.bts.gov/datasets/national-bridge-inventory/about", style={'font-size': 12})
                ], width=9, style={"height": "100%"})  
            ], className="h-75")
        ]),

        dcc.Tab(label='Heatmap', children=[
            dbc.Row([
                dbc.Col([
                    # count of bridges from filter
                    html.Br(),
                    html.Div(id='bridge_count1'),
                    html.Div(id='eval_avg1'),
                    # dropdown for states
                    html.Br(),
                    html.Label('State'),
                    dcc.Dropdown(state, 'All', id='state_sel1', clearable=False, multi=True),
                    # dropdown for highway type
                    html.Br(),
                    html.Label('Highway'),
                    dcc.Dropdown(route, 'State highway', id='highway_sel1', clearable=False),
                    # dropdown for highway number
                    html.Br(),
                    html.Label('Highway Number'),
                    dcc.Dropdown(route_num, 'All', id='hwy_num1'),
                    # dropdown for bridge type
                    html.Br(),
                    html.Label('Bridge Type'),
                    dcc.Dropdown(bridge_type, 'All', id='type_sel1', clearable=False),
                    # slider for year built
                    html.Br(),
                    html.Label('Year Built'),
                    dcc.RangeSlider(1697, 2023,
                                    id='year_slider1',
                                    marks=None,
                                    value=[1697, 2023],
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    dots=False,
                                    step=1,
                                    allowCross=False),
                    # slider for bridge length
                    html.Br(),
                    html.Label('Bridge length (m)'),
                    dcc.RangeSlider(0, 5,
                                    id='length_slider1',
                                    marks={i: '{}'.format(transform_value(i)) for i in range(6)},
                                    value=[0, 5],
                                    dots=False,
                                    step=0.01,
                                    allowCross=False),
                    html.Div(id='bridge_length1',  style={'font-size': 10}),
                    # slider for number of spans
                    html.Br(),
                    html.Label('Number of Spans'),
                    dcc.RangeSlider(0, 771,
                                    id='span_slider1',
                                    marks=None,
                                    value=[0, 771],
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    dots=False,
                                    step=1,
                                    allowCross=False),
                    # slider for evaluation rating
                    html.Br(),
                    html.Label('Evaluation Rating'),
                    dcc.RangeSlider(-1, 9, 1, value=[-1, 9], id='eval_slider1', allowCross=False),
                    html.Div('* -1 for bridges without rating', style={'font-size': 10})

                ], width=3, style={"height": "100%"}),
                dbc.Col([
                    html.Br(),
                    html.H4('Mean Highway Bridge Evaluation Rating by County', style={'textAlign': 'start'}),
                    dcc.Graph(id='us_map_heatmap', figure={}, style={'height':'70vh'}),
                    html.Div('Data accessed January 13, 2023. Latest version can be found below:', style={'font-size': 12}),
                    dcc.Link(html.A('USDOT BTS'), id='data_link1',  href="https://geodata.bts.gov/datasets/national-bridge-inventory/about", style={'font-size': 12})
                ], width=9, style={"height": "80%"})  
            ], className="h-75")
        ]),

        dcc.Tab(label='About', children=[
            html.Br(),
            html.H2("About", style={'textAlign': 'start'}),
            html.P([
                'This dashboard aims to create a tool to allow users to visualize ' 
                'US Interstate, US Numbered, and State highway bridges as either a heatmap showing the '
                'evaluation statistics by county or scatterplot of individual bridges from the "National Bridge Inventory" dataset, accessed on January 13, 2023. '
                'This dataset is maintained by the US Federal Highway Administration and the latest version can '
                'be found ', html.A('here', href='https://geodata.bts.gov/datasets/national-bridge-inventory/about'), '. '
                'Detailed descriptions of all the features included in this dataset can be found '
                "in the ", html.A("Recording and Coding Guide for the Structural Inventory and Appraisal of the Nation's Bridge", href='https://www.fhwa.dot.gov/bridge/nbi.cfm'), '.'
            ], style={'textAlign': 'start'}),
            html.Br(),
            html.H2("Evaluation Rating", style={'textAlign': 'start'}),
            html.P([
                "The evaulation ratings used in the dashboard comes from Items 58 through 60 ",
                "and Item 67 for overall 'Structural Evaluation' as outline in 'Recording and Coding Guide for the Structural Inventory and Appraisal of the Nation's Bridge'. ",
                "Structural components 'Deck', 'Superstructure' and 'Substructure' are evaluated ",
                "on a 10 point scale as outlined below:"
            ]),
            dbc.Table(dbc.Table(table_header1 + table_body1, bordered=True)),
            html.Br(),
            html.P([
            "The evaulation rating used for the overall 'Structural Evaluation' (Item 67) can be described using the below table:"
            ]),
            dbc.Table(dbc.Table(table_header2 + table_body2, bordered=True))
            
        ])
    ])
])

@app.callback(
    Output('us_map_heatmap', 'figure'),
    Output('bridge_count1', 'children'),
    Output('bridge_length1', 'children'),
    Output('eval_avg1', 'children'),
    Output('hwy_num1', 'options'),
    Input('state_sel1', 'value'),
    Input('highway_sel1', 'value'),
    Input('type_sel1', 'value'),
    Input('year_slider1', 'value'),
    Input('length_slider1', 'value'),
    Input('span_slider1', 'value'),
    Input('eval_slider1', 'value'),
    Input('hwy_num1', 'value')
)
def update_heatmap(state, route, b_type, year, length_range, span_num, eval, hwy_num):
    dff = df

    # update length range
    transformed_value_len = [transform_value(v) for v in length_range]
    low_len = transformed_value_len[0]
    high_len = transformed_value_len[1]

    # update span range
    low_span = span_num[0]
    high_span = span_num[1]

    # update eval rating
    low_eval = eval[0]
    high_eval = eval[1]

    # update year range
    low_year = year[0]
    high_year = year[1]

    # filter dataframe
    if state == 'All':
        pass
    elif not state:
        pass
    elif ('All' in state):
        pass
    else:
        dff = dff[dff['state_name'].isin(state)]
    if route != 'All':
        dff = dff[dff['route_type'] == route]
    if b_type != 'All':
        dff = dff[dff['bridge_type'] == b_type]
    dff = dff.query('year_built >= @low_year & year_built <= @high_year')
    dff = dff.query('bridge_length >= @low_len & bridge_length <= @high_len')
    dff = dff.query('num_span >= @low_span & num_span <= @high_span')
    dff = dff.query('eval_rating >= @low_eval & eval_rating <= @high_eval')

    # update route number dropdown
    route_list = np.append(dff['route_num'].unique(), 'All')
    if hwy_num == 'None':
        pass
    if hwy_num != 'All':
        dff = dff[dff['route_num'] == hwy_num]
    
    # summary dff
    df_sum = dff.drop(dff[(dff['eval_rating'] == -1)].index).loc[:, ('fips', 'state_abv', 'state_name', 'eval_rating', 'latitude', 'longitude')].groupby(['fips', 'state_abv', 'state_name'], as_index=False).mean()
    df_sum['count'] = dff.loc[:,('fips', 'eval_rating')].groupby('fips', as_index=False).count().iloc[:,1].tolist()
    avg_total = df_sum['eval_rating'].mean()

    # update figure zoom and location
    if state == 'All':
        lat = 38
        long = -95.7129
        centre = {"lat": lat, "lon": long}
        zoom = 3
    elif not state:
        lat = 38
        long = -95.7129
        centre = {"lat": lat, "lon": long}
        zoom = 3
    else:
        lat = df_sum['latitude'].mean()
        long = df_sum['longitude'].mean()
        centre = {"lat": lat, "lon": long}
        zoom = 4

    fig = px.choropleth_mapbox(df_sum, 
                                geojson=counties, 
                                locations='fips', 
                                color='eval_rating',
                                color_continuous_scale="RdBu",
                                range_color=(0, 9),
                                mapbox_style="carto-positron",
                                zoom=zoom, 
                                center = centre,
                                hover_name='fips',
                                hover_data=['state_name', 'eval_rating', 'count'],
                                height = 700
    )

    fig.update_layout(
        coloraxis_colorbar=dict(title="Bridge Evaluation Rate", 
                                thicknessmode="pixels", 
                                lenmode="pixels", 
                                yanchor="top",y=1, 
                                ticks="outside", 
                                tickvals=[0,1,2,3,4,5,6,7,8,9],
                                ticktext=['0-Closed', '1-N/A', 
                                            '2-Intolerable, replacement', '3-Intolerable, corrective',
                                            '4-Meets tolerable crit.', '5-Above tolerable crit.', '6-Equal min. crit.',
                                            '7-Above min. crit.', '8-Equal desirable crit.', '9-Superior desirable crit.'],
                                dtick=10
                                ),
        margin={"r":0,"t":60,"l":0,"b":0}
    )

    return fig, 'Number of Bridges Selected: {}'.format(dff.shape[0]), 'Selected length range: [{:0.2f}, {:0.2f}]'.format(low_len, high_len), 'Mean evaluation rating: {:0.2f}'.format(avg_total), route_list


@app.callback(
    Output('us_map_scatter', 'figure'),
    Output('bridge_count2', 'children'),
    Output('bridge_length2', 'children'),
    Output('eval_avg2', 'children'),
    Output('hwy_num2', 'options'),
    Input('state_sel2', 'value'),
    Input('highway_sel2', 'value'),
    Input('type_sel2', 'value'),
    Input('year_slider2', 'value'),
    Input('length_slider2', 'value'),
    Input('span_slider2', 'value'),
    Input('eval_slider2', 'value'),
    Input('hwy_num2', 'value')
)
def update_scattermap(state, route, b_type, year, length_range, span_num, eval, hwy_num):
    dff = df
    # filter dataframe

    # update length range
    transformed_value_len = [transform_value(v) for v in length_range]
    low_len = transformed_value_len[0]
    high_len = transformed_value_len[1]

    # update span range
    low_span = span_num[0]
    high_span = span_num[1]

    # update eval rating
    low_eval = eval[0]
    high_eval = eval[1]

    # update year range
    low_year = year[0]
    high_year = year[1]

    # filter dataframe
    if state == 'All':
        pass
    elif not state:
        pass
    elif ('All' in state):
        pass
    else:
        dff = dff[dff['state_name'].isin(state)]
    if route != 'All':
        dff = dff[dff['route_type'] == route]
    if b_type != 'All':
        dff = dff[dff['bridge_type'] == b_type]
    dff = dff.query('year_built >= @low_year & year_built <= @high_year')
    dff = dff.query('bridge_length >= @low_len & bridge_length <= @high_len')
    dff = dff.query('num_span >= @low_span & num_span <= @high_span')
    dff = dff.query('eval_rating >= @low_eval & eval_rating <= @high_eval')

    # update route number dropdown
    route_list = np.append(dff['route_num'].unique(), 'All')
    if hwy_num == 'None':
        pass
    if hwy_num != 'All':
        dff = dff[dff['route_num'] == hwy_num]

    # summary dff
    df_sum = dff.drop(dff[(dff['eval_rating'] == -1)].index).loc[:, ('fips', 'state_abv', 'state_name', 'eval_rating', 'latitude', 'longitude')].groupby(['fips', 'state_abv', 'state_name'], as_index=False).mean()
    df_sum['count'] = dff.loc[:,('fips', 'eval_rating')].groupby('fips', as_index=False).count().iloc[:,1].tolist()
    avg_total = df_sum['eval_rating'].mean()

    # update figure zoom and location
    if state == 'All':
        lat = 38
        long = -95.7129
        zoom = 3
    elif not state:
        lat = 38
        long = -95.7129
        zoom = 3
    else:
        lat = df_sum['latitude'].mean()
        long = df_sum['longitude'].mean()
        zoom = 4

    # scatter plot
    fig = px.scatter_mapbox(dff, 
                            lat='latitude', lon='longitude', 
                            size=dff['bridge_length']*50,
                            size_max=30,
                            hover_name="feature_intersect", 
                            hover_data={'state_name': True,
                                        'eval_rating': True, 
                                        "eval_rating_v": True,
                                        'deck_condition': True,
                                        'superstructure_condition':True,
                                        'substructure_condition': True, 
                                        "bridge_material": True, 
                                        "bridge_type": True,
                                        'year_built': True,
                                        'num_span':True,
                                        'max_span':':.3f',
                                        'bridge_length': ':.3f',
                                        'bridge_width': ':.3f'},
                            color='eval_rating',
                            range_color = [0, 9],
                            color_continuous_scale="rdbu", 
                            opacity=1,
                            zoom=zoom,
                            height=700,
                            mapbox_style="open-street-map"
    )

    fig.update_layout(
        mapbox_style="open-street-map",
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

    return fig, 'Number of Bridges Selected: {}'.format(dff.shape[0]), 'Selected length range: [{:0.2f}, {:0.2f}]'.format(low_len, high_len), 'Mean evaluation rating: {:0.2f}'.format(avg_total), route_list

if __name__ == '__main__':
    app.run_server(debug=True)
