import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd

data = pd.read_csv('data.csv', parse_dates=['License Creation Date',
                                            'License Expiration Date'])
boroughs = data['Address Borough'].dropna().unique().tolist()


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('New York Businesses Dashboard'),
    dcc.Dropdown(id='borough_dropdown',
                 options=[{'label': b, 'value': b}
                          for b in boroughs]),
    dcc.Graph()
])

if __name__ == '__main__':
    app.run_server(debug=True)