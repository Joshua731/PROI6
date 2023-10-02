import json
from app import app
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from app.templates.partials.index import navbar

login_page = Dash(__name__, server=app, external_stylesheets=[dbc.themes.LUX], url_base_pathname="/login/")
login_page.layout = dbc.Container(
    [
        # Navbar
        navbar,
        
        dbc.Row([
            dbc.Col([], sm=3),
            dbc.Col([
                dbc.Row([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Login", className="card-title"),
                            html.Label("Username"),
                            dcc.Input(type="text", id="username-input", placeholder="Enter your username", className="form-control"),
                            html.Label("Password"),
                            dcc.Input(type="password", id="password-input", placeholder="Enter your password", className="form-control"),
                            html.Button("Login", id="login-button", className="btn btn-primary btn-block", n_clicks=0),
                            html.Div(id="login-message", className="mt-3"),
                        ])
                    ], color='dark', className='crd'),
                ]),
            ], sm=6),
            dbc.Col([], sm=3),
        ], className="mt-4"),
    ],
    fluid=True,
)

# Callback to handle login logic
@login_page.callback(
    Output("login-message", "children"),
    Input("login-button", "n_clicks"),
    Input("username-input", "value"),
    Input("password-input", "value"),
)
def handle_login(n_clicks, username, password):
    if n_clicks > 0:
        if username == "your_username" and password == "your_password":
            return "Login successful. Redirecting..."
        else:
            return "Login failed. Please check your credentials."
