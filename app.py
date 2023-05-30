from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.graph_objects as go
import environ
import dash_bootstrap_components as dbc
from data import df_job_data, df_col_data, user_lat, user_lon, user_location_string
from map import job_map, toggle_map, update_map
from col import col_table, toggle_table, update_table
from search import search, toggle_search
from chart import chart, toggle_chart

# ********************************* ENV SETUP *********************************
env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env()


# ********************************* DASH APP *********************************
app = Dash(__name__, external_stylesheets=[
           dbc.themes.VAPOR, "/assets/styles.css"])
server = app.server


# ********************************* DASH LAYOUT *********************************
app.layout = html.Div(
    [
        html.Div(
            [
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
                        search,
                        job_map,
                        col_table,
                        chart,
                    ),
                    style={"min-width": "200px"},
                ),
            ]
        ),
    ],
)

if __name__ == '__main__':
    app.run_server(debug=True)
