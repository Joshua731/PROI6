import dash_table
from dash import html, dcc, Dash, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from app import app
from app.templates.partials.partials import navbar

# Crie uma instância do aplicativo Dash
desempenho_geral = Dash(__name__, external_stylesheets=[dbc.themes.LUX],
                        server=app,
                        url_base_pathname="/desempenho-geral/")


# Gere dados de exemplo para os gráficos
def gerar_dados_graficos():
    tempo_real = [datetime.now() - timedelta(hours=i) for i in range(24)]
    tempo_diario = [datetime.now() - timedelta(days=i) for i in range(30)]
    tempo_mensal = [datetime.now() - relativedelta(month=i) for i in range(12)]
    tempo_anual = [datetime.now() - relativedelta(year=i) for i in range(5)]
    producao_tempo_real = [random.uniform(10, 50) for _ in range(24)]
    producao_diaria = [random.uniform(1000, 2000) for _ in range(30)]
    producao_mensal = [random.uniform(25000, 35000) for _ in range(12)]
    producao_anual = [random.uniform(300000, 400000) for _ in range(5)]
    return tempo_real, tempo_diario, tempo_mensal, tempo_anual, producao_tempo_real, producao_diaria, producao_mensal, producao_anual


# Defina o layout do corpo da tela
desempenho_geral.layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col([
                # navbar
            ], sm=12)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    html.H2("Visão Geral da Usina Fotovoltaica"),
                                ]),
                                dbc.Row([
                                    dbc.CardGroup([
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.Label("Nome da Usina"),
                                                html.P("Usina Solar ABC"),
                                            ])
                                        ]),
                                        dbc.Card([
                                            dbc.CardBody([
                                                dbc.Card([
                                                    dbc.CardBody([
                                                        html.H4("Localização"),
                                                        dash_table.DataTable(
                                                            columns=[
                                                                {"name": "Latitude", "id": "Latitude"},
                                                                {"name": "Longitude", "id": "Longitude"},
                                                            ],
                                                            data=[
                                                                {"Latitude": "40.7128", "Longitude": "-74.0060"},
                                                            ],
                                                            style_table={"height": "auto", "width": "auto"},
                                                        ),
                                                    ]),
                                                ]),
                                            ])
                                        ]),
                                    ]),
                                ]),
                                dbc.Row([
                                    dbc.CardGroup([
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.Label("Data da Instalação"),
                                                html.P("01 de Janeiro de 2023"),
                                            ])
                                        ]),
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.Label("Capacidade Total"),
                                                html.P("100 kW"),
                                            ])
                                        ])
                                    ])
                                ])
                                # ])
                            ])
                        ]),
                    ], sm=12),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Row([
                            html.H2("Métricas de Desempenho"),
                        ]),
                        dbc.Row([
                            dbc.CardGroup([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.Label("Prod. Atual"),
                                        html.P("50 kW"),
                                    ])
                                ]),
                                dbc.Card([
                                    dbc.CardBody([
                                        html.Label("Prod. Diária"),
                                        html.P("1200 kWh"),
                                    ])
                                ]),
                                dbc.Card([
                                    dbc.CardBody([
                                        html.Label("Prod. Mensal"),
                                        html.P("35000 kWh"),
                                    ])
                                ]),
                                dbc.Card([
                                    dbc.CardBody([
                                        html.Label("Prod. Anual"),
                                        html.P("420000 kWh"),
                                    ])
                                ]),
                            ])
                        ])

                    ], sm=12)

                ])
            ], sm=6),
            dbc.Col([
                dcc.Tabs(id="tabs", value="tempo-real", children=[
                    dcc.Tab(label="Tempo Real", value="tempo-real"),
                    dcc.Tab(label="Diário", value="diario"),
                    dcc.Tab(label="Mensal", value="mensal"),
                    dcc.Tab(label="Anual", value="anual"),
                ]),
                html.Div(id="tab-content")
            ], sm=6),
        ]),

        dcc.Interval(id='intervalo-atualizacao', interval=10000, n_intervals=0)
    ],
    fluid=True,
)


# Callback para atualizar o conteúdo da aba
@desempenho_geral.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)
def render_tab_content(value):
    tempo_real, tempo_diario, tempo_mensal, tempo_anual, producao_tempo_real, producao_diaria, producao_mensal, producao_anual = gerar_dados_graficos()

    if value == "tempo-real":
        figura = px.line(x=tempo_real, y=producao_tempo_real, labels={"x": "Tempo", "y": "Produção (kW)"})
    elif value == "diario":
        figura = px.bar(x=tempo_diario, y=producao_diaria, labels={"x": "Dia", "y": "Produção Diária (kWh)"})
    elif value == "mensal":
        figura = px.bar(x=tempo_mensal, y=producao_mensal, labels={"x": "Mês", "y": "Produção Mensal (kWh)"})
    elif value == "anual":
        figura = px.bar(x=tempo_anual, y=producao_anual, labels={"x": "Ano", "y": "Produção Anual (kWh)"})

    return dcc.Graph(figure=figura, config={'displayModeBar': False})
