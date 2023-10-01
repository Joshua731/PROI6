from app import app
from dash import Dash, html
import dash_bootstrap_components as dbc
from app.templates.partials.index import sidebar, navbar

colorscale = ["#A98AA9", "#FFFFCC"]

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
index = Dash(__name__, server=app, external_stylesheets=[dbc.themes.LUX], url_base_pathname='/index/')
index.title = f'{title} - SunDataHub' if title else 'Welcome to SunDataHub'
user = {'username': 'Joshua'}
index.layout = dbc.Container(
    [
        # Navbar
        navbar,

        dbc.Row([
            dbc.Col([], sm=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("SunDataHub", className="card-title"),
                        html.P("Bem vindo(a) ao Sun Data Hub."),
                    ])
                ], color='dark', className='crd'),
            ], sm=6)
        ], className="mt-4"),
    ],
    fluid=True,
)