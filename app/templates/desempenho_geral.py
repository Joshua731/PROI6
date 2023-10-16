from dash import html, dcc, Dash, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from app import app
from app.templates.partials.index import navbar

# Crie uma instância do aplicativo Dash
desempenho_geral = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR], server=app,
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
                navbar
            ],
                sm=12,
                class_name='remover-padding'
            )
        ]),
        dcc.Location(id='url', refresh=False),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    html.H2("Visão Geral da UFV"),
                                ]),
                                dbc.Row([
                                    dbc.CardGroup([
                                        dbc.Card([
                                            dbc.CardBody([
                                                dbc.Row([
                                                    html.P("Nome da Usina"),
                                                    html.H3("Usina Solar ABC"),
                                                ]),
                                            ], class_name='nome-usina'),
                                        ]),
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
                                                    style_data_conditional=[
                                                        {
                                                            'if': {'row_index': 'odd'},
                                                            # Você pode ajustar esta condição conforme necessário
                                                            'backgroundColor': '#073038',
                                                            # Define a cor de fundo para linhas ímpares
                                                        },
                                                        {
                                                            'if': {'row_index': 'even'},
                                                            # Você pode ajustar esta condição conforme necessário
                                                            'backgroundColor': '#073038',
                                                            # Define a cor de fundo para linhas pares
                                                        },
                                                    ],
                                                    style_header={
                                                        'backgroundColor': '#073038',
                                                        # Define a cor de fundo para o cabeçalho
                                                        'color': 'white',  # Define a cor do texto no cabeçalho
                                                    },
                                                    style_cell={'textAlign': 'center'},
                                                    id='tabela'),
                                            ]),
                                        ]),
                                    ])

                                ]),
                                dbc.Row([
                                    dbc.CardGroup([
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.H4("Capacidade Total"),
                                                html.P("100 kW"),
                                            ]),
                                        ]),
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.H4("Data da Instalação"),
                                                html.P("01 de Janeiro de 2023"),
                                            ])
                                        ])
                                    ])
                                ]),
                            ])
                        ]),
                    ], sm=12),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
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
                                        ])
                                    ])
                                ]),
                            ])
                        ]),
                    ], sm=12)
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    html.H2("Estado dos Painéis"),
                                ]),
                                dbc.Row([
                                    dbc.CardGroup([
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.P("Funcionando"),
                                                html.Span('80%'),
                                            ])
                                        ]),
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.P("Em manutenção"),
                                                html.Span('5%'),
                                            ])
                                        ]),
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.P("Offline"),
                                                html.Span('15%'),
                                            ])
                                        ]),
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.P("Eficiência Atual"),
                                                html.Span('90%'),
                                            ])
                                        ]),
                                    ])
                                ])
                            ])
                        ])
                    ], sm=12),
                ])
            ], sm=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            html.H2('Gráficos de Desempenho', className="titulo-desempenho")
                        ]),
                        dbc.Row([
                            dbc.Tabs(id="tabs", active_tab="tempo-real", children=[
                                dbc.Tab(label="Tempo Real", tab_id="tempo-real"),
                                dbc.Tab(label="Diário", tab_id="diario"),
                                dbc.Tab(label="Mensal", tab_id="mensal"),
                                dbc.Tab(label="Anual", tab_id="anual"),
                            ], className='tab-desempenho'),
                        ]),
                        dbc.Row([
                            html.Div(id="tab-content")
                        ]),
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    html.H2("Condições Ambientais")
                                ]),
                                dbc.Row([
                                    dbc.CardGroup([
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.P("Radiação Solar"),
                                                html.Span('800 W/m²'),  # Valor de exemplo, substitua pelo valor real
                                            ])
                                        ]),
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.P("Temperatura"),
                                                html.Span('30°C'),  # Valor de exemplo, substitua pelo valor real
                                            ])
                                        ]),
                                        dbc.Card([
                                            dbc.CardBody([
                                                html.P("Velocidade do Vento"),
                                                html.Span('10 m/s'),  # Valor de exemplo, substitua pelo valor real
                                            ])
                                        ]),
                                    ])
                                ])
                            ])
                        ])
                    ], sm=12),
                ]),
                dbc.Row([
                    dbc.CardGroup([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        html.H5("Alertas:")
                                    ], sm=2),
                                    dbc.Col([
                                        html.H6("Nenhum")
                                    ], sm=10, class_name='mt-1')
                                ])

                            ])
                        ])
                    ])
                ])
            ], sm=6),
        ]),
        dcc.Interval(id='intervalo-atualizacao', interval=10000, n_intervals=0)
    ],
    fluid=True,
)


# Callback para atualizar o conteúdo da aba
@desempenho_geral.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'active_tab')
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
    figura.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font_color="white",
        height=313
    )
    return dcc.Graph(figure=figura, config={'displayModeBar': False})


@desempenho_geral.callback(
    Output('drop-nav', 'label'),
    Input('url', 'pathname')
)
def mostra_pagina(path):
    print(path)
    return path
