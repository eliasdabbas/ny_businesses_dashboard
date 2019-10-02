import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Output, Input

data = pd.read_csv('data.csv', parse_dates=['License Creation Date',
                                            'License Expiration Date'])
boroughs = data['Address Borough'].dropna().unique().tolist()
industries = data['Industry'].dropna().unique().tolist()


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

app.layout = html.Div([
    html.Br(),
    html.H1('New York Businesses Dashboard',
            style={'text-align': 'center', 'color': '#eeeeee'}),
    html.Br(),
    dbc.Row([
        dbc.Col(lg=3),
        dbc.Col([
            dcc.Dropdown(id='borough_dropdown',
                         value='Manhattan',
                         options=[{'label': b, 'value': b}
                                  for b in boroughs]),
        ], lg=6)
    ]),
    dcc.Graph(id='annual_by_borough_chart'),
    html.Hr(),
    dbc.Row([
        dbc.Col(lg=3),
        dbc.Col([
            dcc.Dropdown(id='industry_dropdown',
                 multi=True,
                 value=['Car Wash'],
                 options=[{'label': i, 'value': i}
                          for i in industries])
            ], lg=6)
    ]),
    dcc.Graph(id='by_industry_map_chart')
], style={'background-color': 'black'})

@app.callback(Output('annual_by_borough_chart', 'figure'),
              [Input('borough_dropdown', 'value')])
def plot_annual_by_borogh(borough):
    df = data[data['Address Borough'] == borough]
    timeseries = df.set_index('License Creation Date').resample('A').count()['Industry']
    fig = go.Figure()
    fig.add_bar(x=timeseries.index, y=timeseries.values,
                marker={'color': '#eeeeee'})
    fig.layout.title = 'Businesses Established by Year: ' + borough
    fig.layout.font = {'color': '#eeeeee'}
    fig.layout.xaxis.title = 'Year'
    fig.layout.yaxis.title = 'Number of Businesses Established'
    fig.layout.paper_bgcolor = 'black'
    fig.layout.plot_bgcolor = 'black'
    return fig.to_dict()


@app.callback(Output('by_industry_map_chart', 'figure'),
              [Input('industry_dropdown', 'value')])
def plot_businesses_by_industry_on_map(industries):
    fig = go.Figure()
    for industry in industries:
        df = data[data['Industry'] == industry]
        fig.add_scattermapbox(lat=df['Latitude'],
                              lon=df['Longitude'],
                              name=industry, marker={'size': 8})
    fig.layout.title = ('Business Locations: ' + ', '.join(industries) +
                        '<br>double-click to get back to original zoom')
    fig.layout.font = {'color': '#eeeeee'}
    fig.layout.paper_bgcolor = 'black'
    fig.layout.plot_bgcolor = 'black'
    fig.layout.mapbox.style = 'stamen-toner'
    fig.layout.mapbox.center = {'lat': 40.64925, 'lon': -74.0055}
    fig.layout.mapbox.zoom = 8
    fig.layout.geo.lataxis = go.layout.geo.Lataxis(range=[40.4, 40.8985])
    fig.layout.geo.lonaxis = go.layout.geo.Lonaxis(range=[-74.3, -73.711])
    fig.layout.height = 700

    return fig.to_dict()

if __name__ == '__main__':
    app.run_server(debug=True)
