from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc

footer = dbc.Row(
    [
        html.Span(
            [
                html.P("City Cost of Living Data from ",
                       style={"display": "inline"}),
                html.A("AdvisorSmith", href="https://advisorsmith.com/data/coli",
                       target="_blank", style={"display": "inline"})
            ]
        )
    ],
)
