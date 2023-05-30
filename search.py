from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from data import df_job_data, df_col_data, user_lat, user_lon, user_location_string


search = dbc.Row(
    [
        dbc.Button(
            "Search",
            id="toggle-search",
            className="mb-3",
        ),
        dbc.Collapse(
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
            id="search-collapse",
            is_open=True,
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
