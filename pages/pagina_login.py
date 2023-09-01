import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash import Dash, html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
from flask import Flask, redirect, request, session
import jwt
import datetime
import functools
from flask import request, redirect

from app import pagina_login

layout_login = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Tabs([
                dbc.Tab(label="Login", tab_id="login-tab", className='tab-style'),
                dbc.Tab(label="Cadastro", tab_id="cadastro-tab", className='tab-style'),
            ],
                id="tabs",
                active_tab="login-tab"),
        ], sm=12)
    ]),
    dbc.Row([
        dbc.Col([], id='tabs-content', width=12, className="tabs-content-container"),
        # Use a classe CSS para centralizar
    ]),
    dbc.Row([
        pop_up
    ])
], fluid=True, className="container-fluid")