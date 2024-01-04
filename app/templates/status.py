import dash
from dash.exceptions import PreventUpdate

from app import app
from app.templates.partials.index import navbar
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

status = Dash(__name__, url_base_pathname='/status/', server=app, external_stylesheets=[dbc.themes.SOLAR])
status.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            navbar
        ], sm=12)
    ]),
    dbc.Row([
       dbc.Col([
           dbc.Card([
               dbc.CardBody([
                   dbc.Row([
                       dbc.Col([
                           html.H1('Status dos Inversores', className='status-titulo')
                       ], sm=12)
                   ]),
                   dbc.Row([
                       dbc.Col([
                           dbc.CardGroup([
                               dbc.Card([
                                   dbc.CardHeader('Nenhuma usina foi adicionada', className='status-titulo'),
                                   dbc.CardBody([
                                       dbc.Row([
                                           dbc.Col(sm=5),
                                           dbc.Col([
                                               dbc.Button('+', id='add-usina', color='dark')
                                           ], sm=2, className='status-botao'),
                                           dbc.Col(sm=5),
                                       ])
                                   ])
                               ], color='dark')
                           ])
                       ], sm=12)
                   ])
               ])
           ], color='dark'),
       ], sm=12)
    ]),
    dcc.Location(id='url')
], fluid=True)


@status.callback(
    Output('url', 'pathname'),
    Input('add-usina', 'n_clicks')
)
def redirecionar_para_edicao_da_tela_de_status_dos_inversores(cliques):
    id_atual = dash.ctx.triggered_id
    if id_atual == 'add-usina':
        return '/editar_status'
    raise PreventUpdate
