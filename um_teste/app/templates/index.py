from app import app
from dash import Dash, html
import dash_bootstrap_components as dbc

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

title = None
index = Dash(__name__, server=app, external_stylesheets=[dbc.themes.CYBORG], url_base_pathname='/index/')
index.title = f'{title} - SunDataHub' if title else 'Welcome to SunDataHub'
user = {'username': 'Joshua'}
index.layout = dbc.Container([
    dbc.Row([
        html.H1(f"Hello, {user['username']}"),
    ]),
    dbc.Row([
        dbc.Col(psts, sm=5)
    ])
], fluid=True)
