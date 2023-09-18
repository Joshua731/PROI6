from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np

posts = [
    {
        'author': {'username': 'Joshua da Silva Cavazzani'},
        'body': 'Beautiful day in Portland!'
    },
    {
        'author': {'username': 'Susan'},
        'body': 'The Avengers movie was so cool!'
    }
]

psts = []

for post in posts:
    psts.append(
        dbc.Row([
            dbc.Col([
                html.P(f"{post['author']['username']} says: ")
            ], sm=6),
            dbc.Col([
                html.B(post['body'])
            ], sm=6)
        ])
    )


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__)

title = None
index = Dash(__name__, server=app, external_stylesheets=[dbc.themes.CYBORG], url_base_pathname='/index/')
index.title = f'{title} - SunDataHub' if title else 'Welcome to SunDataHub'
user = {'username': 'Joshua'}

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    html.H1(f"Hello, {user['username']}"),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content'),
    dbc.Col(psts, sm=5)
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
    app.run(debug=True)
