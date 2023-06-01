from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import dash_daq as daq


col_toggle_button = html.Div(
    [
        daq.ToggleSwitch(
            id='col-toggle',
            value=False,
        ),
        html.Div(id='col-toggle-output')
    ]
)


search = dbc.Row(
    [
        dbc.Button(
            "Search",
            id="toggle-search",
            className="mb-3",
        ),
        dbc.Collapse(
            [
                html.Div(
                    [
                        dbc.Input(
                            id="state-input",
                            type="text",
                            placeholder="State",
                            className="search-field"
                        ),
                        dbc.Input(
                            id="city-input",
                            type="text",
                            placeholder="City",
                            className="search-field"
                        ),
                        dbc.Input(
                            id="title-input",
                            type="text",
                            placeholder="Title",
                            className="search-field"
                        ),
                        dbc.Input(
                            id="skills-input",
                            type="text",
                            placeholder="Skills",
                            className="search-field"
                        ),
                    ],
                    className="w-100 mx-2 search-field-container mb-4"
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            daq.ToggleSwitch(
                                id='col-toggle',
                                value=False
                            ),
                            width="auto"
                        ),
                        dbc.Col(
                            dbc.Row(
                                [
                                    html.Label("Cost of Living Adjustment:"),
                                    html.Div(id='col-toggle-output')
                                ],
                            )
                        ),
                    ],
                    className="m-3",
                    justify="start",
                    align="center"
                )
            ],
            id="search-collapse",
            is_open=False,
        ),
    ]
)


@callback(  # Show/Hide Search
    Output("search-collapse", "is_open"),
    [Input("toggle-search", "n_clicks")],
    [State("search-collapse", "is_open")],
)
def toggle_search(n_clicks, is_open):
    if n_clicks is None:
        return is_open
    return not is_open
