import dash_auth
from dash import Dash, html
import dash_bootstrap_components as dbc

VALID_USERNAME_PASSWORD_PAIRS = {
    'username': 'password'
}

app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
auth = dash_auth.basic_auth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
app.layout = dbc.Container([
    html.P('Hello, World!')
])

app.run_server(debug=True)
