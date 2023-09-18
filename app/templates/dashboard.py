import dash
from app import app
from dash import Dash, html, dcc, Input, Output
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output #for the callbacks

app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

dashboard = Dash(__name__, server=app, external_stylesheets=[dbc.themes.LUX], url_base_pathname="/dashboard/")

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "black",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.NavbarSimple(
            brand="Bem-vindo a S.D.H.",
            brand_href="#",
            color="primary",
            dark=True,
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(dbc.NavLink("Perfil", href="/page-2")),
                dbc.NavItem(dbc.NavLink("Configurações", href="/page-3")),
            ],
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)
header = html.H4(
    "Side Example.py", className="bg-primary text-white p-2 mb-2 text-center"
)

app.layout = html.Div([dcc.Location(id="url"),sidebar,header,content])


@app.callback(Output("page-content", "children"),[Input("url", "pathname")])
     #Output("line-chart", "figure"),
    

def render_page_content(pathname):
    if pathname == "/":
        return dbc.NavbarSimple(children=[html.H2('Particular info for HOMEPAGE')],color="grey",dark=True,)
    elif pathname == "/page-1":
        return dbc.NavbarSimple(children=[html.H2('Particular info for PAGE1')],color="grey",dark=True,)
    elif pathname == "/page-2":
        return dbc.NavbarSimple(children=[html.H2('Particular info for PAGE2')],color="grey",dark=True,)
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )