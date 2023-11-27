import datetime
import json

import pandas as pd
from screeninfo import get_monitors

from app import app
from app.templates.partials.index import navbar
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

df = pd.read_csv(r"app\files\saida_atualizado.csv")

colorscale = ["#A98AA9", "#FFFFCC"]  # removi "#808080"
with open(r"app\files\geojs-35-mun.json", "r", encoding='utf-8') as e:
    geojson_file = json.load(e)

fig = go.Figure(go.Choroplethmapbox(
    geojson=geojson_file,
    locations=df['id'],
    z=df['value'],
    featureidkey="properties.id",
    colorscale=colorscale,
    showscale=False,
))

fig.update_layout(mapbox=dict(style="carto-darkmatter"), mapbox_zoom=6.66666,
                  mapbox_center={"lat": -23.3055, "lon": -45.967}, margin=dict(l=0, r=0, t=0, b=0))

# Crie uma instância do aplicativo Dash
historico_producao = Dash(__name__, server=app, external_stylesheets=[dbc.themes.SOLAR],
                          url_base_pathname='/historico_producao/')

# Layout do corpo da tela
historico_producao.layout = dbc.Container(
    [
        navbar,
        dcc.Location(id='url', refresh=False),
        html.H1('Histórico de Produção de Energia', className="text-center my-4"),
        dbc.Row(
            [
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Selecione as datas"),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dcc.DatePickerRange(
                                        id='data-producao',
                                        min_date_allowed=datetime.date(1969, 12, 31),
                                        max_date_allowed=datetime.datetime.now().strftime("%Y-%m-%d"),
                                        initial_visible_month=datetime.date(
                                            int(datetime.datetime.now().strftime("%Y")), 3, 17)
                                    )
                                ], sm=6),
                                dbc.Col([
                                    dbc.Button('Gerar Relatório')
                                ], sm=6, style={'text-align': 'center'})
                            ]),
                            dbc.Row(id='output-grafico-historico')
                        ])
                    ])
                ], sm=6),
                dbc.Col(
                    [
                        dbc.Card([
                            dbc.CardHeader("Selecione uma cidade", id='cidade-selecionada'),
                            dbc.CardBody([
                                dcc.Graph(figure=fig, className='map', id='mapa',
                                          style={"height": f"{get_monitors()[0].height * 0.66}px"})
                            ])
                        ])
                    ],
                    sm=6,
                ),
            ],
            className="my-4",
        ),
    ],
    fluid=True,
)


# Callback para atualizar o gráfico com os dados históricos

# Callback para atualizar o gráfico com os dados históricos
@historico_producao.callback(
    Output('output-grafico-historico', 'children'),
    [
        Input('data-producao', 'start_date'),
        Input('data-producao', 'end_date'),
    ]
)
def plota_producao(comeco, fim):
    if comeco and fim:
        figura = go.Figure()
        figura.add_trace(go.Scatter(x=[comeco, fim], y=[10, 15], mode='lines', name='Usina A'))
        figura.update_layout(title='Histórico de Produção de Energia',
                             plot_bgcolor='rgba(0, 0, 0, 0)',
                             paper_bgcolor='rgba(0, 0, 0, 0)',
                             font_color='white',
                             height=get_monitors()[0].height * 0.5975)
        return dcc.Graph(figure=figura, config={'displayModeBar': False})


@historico_producao.callback(
    Output('drop-nav', 'label'),
    Input('url', 'pathname')
)
def mostra_pagina(path):
    print(path)
    return path


@historico_producao.callback(
    Output('cidade-selecionada', 'children'),
    Input('mapa', 'clickData')
)
def mostra_nome_cidade(dados_cidade):
    return f"""Cidade {df.query(f"id == {dados_cidade['points'][0]['location']}")["name"].values[0]} selecionada"""


# autenticacao(historico_producao)
