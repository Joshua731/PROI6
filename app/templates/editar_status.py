from app import app
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

edit_status = Dash(__name__, url_base_pathname='/editar_status/', server=app, external_stylesheets=[dbc.themes.SOLAR])
edit_status.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.A('Adicionar cidade', id='add-cidade', className='edit-status-add-cidade')
                ])
            ], color='dark')
        ], sm=12)
    ])
])