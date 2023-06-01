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
           dbc.themes.VAPOR, "/assets/styles.css"])
app.title = "Tech Relocator"
server = app.server


# ********************************* DASH LAYOUT *********************************
app.layout = html.Div(
    [
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
