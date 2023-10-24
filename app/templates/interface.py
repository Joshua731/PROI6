import json
from app import app
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np
from app.templates.partials.index import sidebar, navbar
from screeninfo import get_monitors

# Obtém a informação do monitor
monitors = get_monitors()

# Itera sobre os monitores (em caso de vários monitores)
for m in monitors:
    print("Largura:", m.width, "Altura:", m.height)

df = pd.read_csv(r"app\files\saida_atualizado.csv")

colorscale = ["#A98AA9", "#FFFFCC"]
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

x = ['IDGT']
y = [100]

# Crie o gráfico de barras
fig3 = go.Figure(data=[go.Bar(x=x, y=y, text=y, textposition='inside', marker_color='#cccccc')])
fig3.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',  # Fundo transparente
                   paper_bgcolor='rgba(0, 0, 0, 0)',
                   margin=dict(l=0, r=0, t=0, b=0),
                   font=dict(color='#cccccc'),
                   yaxis_showgrid=False,
                   yaxis_showticklabels=False)

# Crie um array de valores x de 0 a 23 representando as horas do dia
x = np.arange(24)

# Crie dois arrays de valores de "ruído" para y, um indo de 0 a 100 e o outro de 0 a 50
y1 = np.random.normal(50, 10, 24) + np.linspace(0, 100, 24)
y2 = np.random.normal(25, 5, 24) + np.linspace(0, 50, 24)

# Crie os gráficos Scatter
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=x, y=y1, mode='lines+markers', name='Irradiação Solar (Local 1)'))
fig2.add_trace(go.Scatter(x=x, y=y2, mode='lines+markers', name='Irradiação Solar (Local 2)'))

fig2.update_layout(title=None, xaxis_title='Intervalo de Tempo (Horas)',
                   yaxis_title='Irradiâncias',
                   legend=dict(orientation='h', y=1.175, x=0.1),
                   plot_bgcolor='rgba(0, 0, 0, 0)',  # Fundo transparente
                   paper_bgcolor='rgba(0, 0, 0, 0)',
                   margin=dict(l=0, r=0, t=0, b=0),
                   font=dict(color='#cccccc')
                   )

interface = Dash(__name__, server=app, external_stylesheets=[dbc.themes.SOLAR], url_base_pathname="/interface/")
interface.layout = dbc.Container(
    [
        # Navbar
        navbar,
        dcc.Location(id='url', refresh=False),
        # Conteúdo da página
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig, className='map',
                          style={"height": f"{([m.width for m in get_monitors()][0] * 0.49)}px"})
            ], sm=6),
            dbc.Col([
                dbc.Row([
                    dbc.Card([
                        dbc.Row([
                            html.Fieldset([
                                dbc.Row([
                                    html.Legend("PRODUÇÃO USINA", className='prod-u'),
                                ]),
                                dbc.Row([
                                    dbc.CardGroup([
                                        dbc.Card([
                                            dbc.CardBody([
                                                dbc.Row([
                                                    html.Label("DD"),
                                                ]),
                                                dbc.Row([
                                                    html.Span("100 kW")
                                                ])
                                            ])
                                        ]),
                                        dbc.Card([
                                            dbc.CardBody([
                                                dbc.Row([
                                                    html.Label("MM"),
                                                ]),
                                                dbc.Row([
                                                    html.Span("30 MW")
                                                ])
                                            ])
                                        ]),
                                        dbc.Card([
                                            dbc.CardBody([
                                                dbc.Row([
                                                    html.Label("YYYY"),
                                                ]),
                                                dbc.Row([
                                                    html.Span("360 MV")
                                                ])
                                            ])
                                        ])
                                    ])
                                ])
                            ]),
                        ])

                    ], color='dark', className='crd'),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.Row([
                                html.Legend("Irradiação Diária", className='leg-irr')
                            ]),
                            dbc.Row([
                                dcc.Graph(figure=fig2, className='graph',
                                          style={"height": f"{([m.width for m in get_monitors()][0] * 0.2)}px"}
                                          )
                            ]),
                        ], color='dark', className='crd-g'),
                    ], sm=10),
                    dbc.Col([
                        dbc.Card([
                            dcc.Graph(figure=fig3, className='idgt',
                                      style={"height": f"{([m.width for m in get_monitors()][0] * 0.25)}px"})
                        ], color='dark', class_name='crd-i'),
                    ], sm=2)
                ])
            ], sm=6)
        ], className="mt-4"),
    ],
    fluid=True,
)

@interface.callback(
    Output('drop-nav', 'label'),
    Input('url', 'pathname')
)
def mostra_pagina(path):
    print(path)
    return path