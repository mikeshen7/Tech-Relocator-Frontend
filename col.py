from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from data import df_job_data, df_col_data, user_lat, user_lon, user_location_string

col_table = dbc.Row(
    [
        dbc.Button(
            "Cost of Living",
            id="toggle-table",
            className="mb-3",
        ),
        dbc.Collapse(
            html.Div(
                dbc.Table(
                    [
                        # Table header
                        html.Thead([
                            html.Tr([
                                html.Th("Region", className="cell"),
                                html.Th("Index", className="cell"),
                                html.Th("Grocery", className="cell"),
                                html.Th("Housing", className="cell"),
                                html.Th("Utilities", className="cell"),
                                html.Th("Transportation", className="cell"),
                                html.Th("Health", className="cell"),
                                html.Th("Misc", className="cell"),
                            ])
                        ]),
                        # Table body
                        html.Tbody(id="table-body"),
                    ],
                    bordered=True,
                    hover=True,
                    responsive=True,
                ),
                className="table-container mb-4",
            ),
            id="table-collapse",
            is_open=True,
        ),
    ]
)


@callback(  # Show/Hide Cost of Living Table
    Output("table-collapse", "is_open"),
    [Input("toggle-table", "n_clicks")],
    [State("table-collapse", "is_open")],
)
def toggle_table(n_clicks, is_open):
    if n_clicks is None:
        return is_open
    return not is_open


@callback(  # Filters Cost of Living Table based on state
    Output("table-body", "children"),
    Input("state-input", "value")
)
def update_table(state):
    if state:
        # Split the input by spaces
        states = state.split()

        # Create a regex pattern to match partial state names
        pattern = "|".join(states)

        # Filter the data based on the pattern
        filtered_data = df_col_data[df_col_data["state"].str.contains(
            pattern, case=False, regex=True)]
    else:
        filtered_data = df_col_data

    table_rows = [
        html.Tr(
            [
                html.Td(row["state"], className="cell"),
                html.Td(row["index"], className="cell"),
                html.Td(row["grocery"], className="cell"),
                html.Td(row["housing"], className="cell"),
                html.Td(row["utilities"], className="cell"),
                html.Td(row["transportation"], className="cell"),
                html.Td(row["health"], className="cell"),
                html.Td(row["misc"], className="cell"),
            ]
        )
        for _, row in filtered_data.iterrows()
    ]

    return table_rows
