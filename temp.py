# -*- coding: utf-8 -*-
from dash import Dash, dcc, html
import time

from dash.dependencies import Input, Output, State

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H3("Edit text input to see loading state"),
        dcc.Input(id="ls-input-1", value='Input triggers local spinner'),
        dcc.Loading(id="ls-loading-1", children=[html.Div(id="ls-loading-output-1")], type="default"),
        html.Div(
            [
                dcc.Input(id="ls-input-2", value='Input triggers nested spinner'),
                dcc.Loading(
                    id="ls-loading-2",
                    children=[html.Div([html.Div(id="ls-loading-output-2")])],
                    type="circle",
                )
            ]
        ),
    ],
)

@app.callback(Output("ls-loading-output-1", "children"), Input("ls-input-1", "value"))
def input_triggers_spinner(value):
    time.sleep(1)
    return value


@app.callback(Output("ls-loading-output-2", "children"), Input("ls-input-2", "value"))
def input_triggers_nested(value):
    time.sleep(1)
    return value


if __name__ == "__main__":
    app.run_server(debug=False)
