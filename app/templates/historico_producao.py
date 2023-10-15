from app import app
from app.templates.partials.index import navbar
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Crie uma instância do aplicativo Dash
historico_producao = Dash(__name__, server=app, external_stylesheets=[dbc.themes.SOLAR],
                          url_base_pathname='/historico_producao/')

# Layout do corpo da tela
historico_producao.layout = dbc.Container(
    [
        navbar,
        html.H1('Histórico de Produção de Energia', className="text-center my-4"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label('Filtrar por Data:', className="mr-2"),
                        dcc.Input(type='date', className="form-control mb-2")
                    ],
                    sm=6,
                ),
                dbc.Col(
                    [
                        html.Label('Selecione uma Usina:', className="mr-2"),
                        dcc.Dropdown(options=[
                            {'label': 'Usina A', 'value': 'A'},
                            {'label': 'Usina B', 'value': 'B'},
                            {'label': 'Usina C', 'value': 'C'}
                        ], className="mb-2")
                    ],
                    sm=6,
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            'Filtrar',
                            id='filtrar-button',
                            color="primary",
                            className="mb-2",
                            outline=True
                        ),
                    ],
                    sm=12,
                )
            ],
            className="my-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(id='output-grafico-historico'),
                    ],
                    sm=12,
                ),
            ],
            className="my-4",
        )
    ],
    fluid=True,
)


# Callback para atualizar o gráfico com os dados históricos

# Callback para atualizar o gráfico com os dados históricos
@historico_producao.callback(
    Output('output-grafico-historico', 'children'),
    [Input('filtrar-button', 'n_clicks')]
)
def update_chart(n_clicks):
    # Lógica para atualizar o gráfico com os dados históricos
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2, 3, 4, 5], y=[10, 15, 13, 17, 12], mode='lines', name='Usina A'))
    fig.update_layout(title='Histórico de Produção de Energia',
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      paper_bgcolor='rgba(0, 0, 0, 0)',
                      font_color='white')
    return dcc.Graph(figure=fig, config={'displayModeBar': False})
