from app import app
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

from app.templates.partials.index import navbar

status_tempo_real = Dash(__name__, server=app, external_stylesheets=[dbc.themes.SOLAR],
                         url_base_pathname='/status_tempo_real/')

# Dados de exemplo em tempo real
dados_status = {
    'potencia': '50 kW',
    'carga_bateria': '80%',
    'radiacao_solar': '800 W/m²',
    'temperatura': '25°C',
    'velocidade_vento': '5 m/s'
}

# Layout da tela de status em tempo real
status_tempo_real.layout = dbc.Container(
    [
        navbar,
        dcc.Location(id='url', refresh=False),
        dbc.Row(
            dbc.Col(html.H2("Status em Tempo Real", className="status-title text-center"), sm=12),
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Informações de Potência"),
                            dbc.CardBody(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(html.P("Potência Atual"), width=6),
                                            dbc.Col(html.Span("50 kW", className="info-value"), width=6),
                                        ],
                                        className="info-item",
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(html.P("Carga da Bateria"), width=6),
                                            dbc.Col(html.Span("80%", className="info-value"), width=6),
                                        ],
                                        className="info-item",
                                    ),
                                ]
                            ),
                        ]
                    ),
                    sm=6,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Condições Meteorológicas"),
                            dbc.CardBody(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(html.P("Radiação Solar"), width=6),
                                            dbc.Col(html.Span("800 W/m²", className="info-value"), width=6),
                                        ],
                                        className="info-item",
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(html.P("Temperatura"), width=6),
                                            dbc.Col(html.Span("28°C", className="info-value"), width=6),
                                        ],
                                        className="info-item",
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(html.P("Velocidade do Vento"), width=6),
                                            dbc.Col(html.Span("12 km/h", className="info-value"), width=6),
                                        ],
                                        className="info-item",
                                    ),
                                ]
                            ),
                        ]
                    ),
                    sm=6,
                ),
            ],
            className="info-section",
        ),
    ],
    fluid=True,
)


@status_tempo_real.callback(
    Output('drop-nav', 'label'),
    Input('url', 'pathname')
)
def mostra_pagina(path):
    print(path)
    return path