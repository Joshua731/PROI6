from app import app
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

producao_energia = Dash(__name__, server=app, external_stylesheets=[dbc.themes.SOLAR], url_base_pathname='/producao_energia/')

# Dados de exemplo para o gráfico
# Substitua esses dados pelos dados reais da produção de energia ao longo do tempo
dados_grafico = {
    'tempo': [1, 2, 3, 4, 5],
    'producao': [10, 20, 15, 18, 25]
}

# Layout do aplicativo Dash
producao_energia.layout = html.Div([
    html.H1('Gráficos de Produção de Energia'),
    html.Label('Selecione a Usina:'),
    dcc.Dropdown(
        options=[
            {'label': 'Usina A', 'value': 'A'},
            {'label': 'Usina B', 'value': 'B'},
            # Adicione mais usinas, se necessário
        ],
        value='A'
    ),
    dcc.Graph(
        id='grafico-producao-energia',
        figure=px.line(dados_grafico, x='tempo', y='producao', title='Produção de Energia ao Longo do Tempo')
    )
])

