import json
from app import app
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from app.templates.partials.index import navbar

custom_css = {
    'text-light': {'color': 'white'},
    'bg-light': {'background-color': 'white'},
    '.body': {'background-color': '#A9A9A9'},
    'font': 'dict(color='  # cccccc)',
}

login_page = Dash(__name__, server=app, external_stylesheets=[dbc.themes.SOLAR], url_base_pathname="/login/")
login_page.layout = dbc.Container(
    [
        # Navbar
        navbar,
        dcc.Location(id='url', refresh=False),
        dbc.Row([
            dbc.Col([], sm=3),
            dbc.Col([
                dbc.Row([
                    dbc.Card([
                        dbc.CardHeader('Cadastro do Usuário', class_name='card-title'),
                        dbc.CardBody([
                            html.Label("Nome Completo"),
                            dcc.Input(type="text", id="username-input", placeholder="Entre com seu Usuario",
                                      className="form-control"),
                            html.Label('Empresa'),
                            dcc.Input(type="text", id="company-input", placeholder="Entre com a sua Empresa",
                                      className="form-control"),
                            html.Label('Email'),
                            dcc.Input(type="email", id="email-input", placeholder="Entre com o seu Email",
                                      className="form-control"),
                            html.Label("Senha"),
                            dcc.Input(type="password", id="password-input", placeholder="Entre com a sua Senha",
                                      className="form-control"),

                            html.Div(id="signup-message", className="mt-3"),
                        ]),
                        dbc.CardFooter(html.A('Concluir', id='redirecionar-home'))
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
    Output("signup-message", "children"),
    Input("redirecionar-home", "n_clicks"),
    Input("username-input", "value"),
    Input("company-input", "value"),
    Input("email-input", "value"),
    Input("password-input", "value"),
)
def handle_login(n_clicks, username, password):
    if n_clicks > 0:
        if username == "your_username" and password == "your_password":
            return "Login successful. Redirecting..."
        else:
            return "Login failed. Please check your credentials."


@login_page.callback(
    Output('drop-nav', 'label'),
    Input('url', 'pathname')
)
def mostra_pagina(path):
    print(path)
    return path
