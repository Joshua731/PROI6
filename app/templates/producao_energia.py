from app import app
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from app.templates.partials.index import navbar

producao_energia = Dash(__name__, server=app, external_stylesheets=[dbc.themes.SOLAR],
                        url_base_pathname='/producao_energia/')

# Dados de exemplo para o gráfico
# Substitua esses dados pelos dados reais da produção de energia ao longo do tempo
dados_usina_a = {
    'tempo': [1, 2, 3, 4, 5],
    'producao': [10, 20, 15, 18, 25]
}

dados_usina_b = {
    'tempo': [1, 2, 3, 4, 5],
    'producao': [15, 10, 20, 15, 30]
}

# Layout do aplicativo Dash
producao_energia.layout = dbc.Container([
    navbar,
    dcc.Location(id='url', refresh=False),
    html.H1('Gráficos de Produção de Energia', className='mt-4 mb-4 text-center'),
    dbc.Row([
        dbc.Col([
            html.Label('Selecione a Usina:', className='mb-2'),
            dcc.Dropdown(
                id='dropdown-usina',
                options=[
                    {'label': 'Usina A', 'value': 'A'},
                    {'label': 'Usina B', 'value': 'B'},
                    # Adicione mais usinas, se necessário
                ],
                value='A'
            ),
        ], width=6),
        dbc.Col([
            html.Label('Selecione o Tipo de Gráfico:', className='mb-2'),
            dcc.Dropdown(
                id='dropdown-tipo-grafico',
                options=[
                    {'label': 'Linha', 'value': 'linha'},
                    {'label': 'Barra', 'value': 'barra'},
                    {'label': 'Área', 'value': 'area'},
                ],
                value='linha'
            ),
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='grafico-producao-energia', config={'displayModeBar': False})
                ])
            ], className='mt-4')
        ], width=12)
    ]),
], fluid=True)


@producao_energia.callback(
    Output('grafico-producao-energia', 'figure'),
    [Input('dropdown-tipo-grafico', 'value'),
     Input('dropdown-usina', 'value')]
)
def atualizar_grafico(tipo_grafico, usina_selecionada):
    if usina_selecionada == 'A':
        dados_grafico = dados_usina_a
        nome_usina = 'Usina A'
    elif usina_selecionada == 'B':
        dados_grafico = dados_usina_b
        nome_usina = 'Usina B'

    if tipo_grafico == 'linha':
        figura = go.Figure(data=go.Scatter(x=dados_grafico['tempo'], y=dados_grafico['producao'], mode='lines', name=nome_usina))
    elif tipo_grafico == 'barra':
        figura = go.Figure(data=go.Bar(x=dados_grafico['tempo'], y=dados_grafico['producao'], name=nome_usina))
    elif tipo_grafico == 'area':
        figura = go.Figure(data=go.Scatter(x=dados_grafico['tempo'], y=dados_grafico['producao'], fill='tozeroy', mode='none', name=nome_usina))

    figura.update_layout(
        title='Produção de Energia ao Longo do Tempo',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font_color='white',
        xaxis=dict(
            title='Data',
            tickformat='%Y-%m-%d',  # Formato de exibição da data no eixo x
            tickangle=45,  # Ângulo dos rótulos de data para melhor legibilidade
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='white',
            ),
        ),
        yaxis=dict(
            title='Produção de Energia',
            showline=True,
            showgrid=True,
            gridcolor='rgb(204, 204, 204)',
            gridwidth=1,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='white',
            ),
        )
    )

    return figura


@producao_energia.callback(
    Output('drop-nav', 'label'),
    Input('url', 'pathname')
)
def mostra_pagina(path):
    print(path)
    return path