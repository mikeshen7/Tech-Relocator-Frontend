from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from data import data
from map import job_map
from col import col_table
from search import search
from chart import chart
from footer import footer


# ********************************* DASH APP *********************************
app = Dash(__name__, external_stylesheets=[
           dbc.themes.MORPH, "/assets/styles.css"])
app.title = "Tech Relocator"
server = app.server


# ********************************* DASH LAYOUT *********************************
app.layout = html.Div(
    [
        # Loading and Title
        html.Div(
            [
                dcc.Loading(
                    id="ls-loading-2",
                    children=[html.Div([html.Div(id="ls-loading-output-1")])],
                    type="circle",
                    className='loading-indicator',
                ),
                html.H1(
                    "Tech Relocators",
                    className="align-bottom w-100 p-2 text-center",
                ),
            ],
            className='d-flex',
        ),
        # Alert for users
        html.Div(
            className="alert alert-dismissible alert-info",
            children=[
                html.Button(type="button", className="btn-close", **{"data-bs-dismiss": "alert"}),
                html.Strong("We only use your location for visual purposes!"),
                " Otherwise ",
                html.A("you will default to Seattle, WA", href="#", className="alert-link"),
                ", if you block this feature. Enjoy."
            ]
        ),
        # Introduction
        html.Div(
            children=[
                html.Strong("Welcome to Tech Relocators", className="header-title"),
                html.P(
                    "At Tech Relocator, we aim to simplify your job search in the tech industry and provide you with valuable insights into the cost of living across different cities in the USA. Our platform is designed to help tech professionals like you make informed decisions when relocating for new job opportunities. Using data analyst with interactive 3d models.",
                    className="header-text"
                )
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    (
                        data,
                        search,
                        job_map,
                        col_table,
                        chart,
                        footer,
                    ),
                    style={"min-width": "200px"},
                ),
            ]
        ),
    ],
)

if __name__ == '__main__':
    app.run_server(debug=True)
