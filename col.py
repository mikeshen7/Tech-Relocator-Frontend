from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from data import df_job_data, df_col_data, df_col_city_data


# ********************************* DASH COMPONENTS *********************************
state_table = dbc.Table(
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
        html.Tbody(id="state-table-body"),
    ],
    bordered=True,
    hover=True,
    responsive=True,
)

city_table = dbc.Table(
    [
        # Table header
        html.Thead([
            html.Tr([
                html.Th("City", className="cell"),
                html.Th("State", className="cell"),
                html.Th("Index", className="cell"),
            ])
        ]),
        # Table body
        html.Tbody(id="city-table-body"),
    ],
    bordered=True,
    hover=True,
    responsive=True,
)


col_table = dbc.Row(
    [
        dbc.Button(
            "Cost of Living",
            id="toggle-table",
            className="mb-3",
        ),
        dbc.Collapse(
            html.Div(
                [
                    html.Div(
                        [
                            html.H2('State Cost of Living',
                                    className="text-center"),
                            html.Div(
                                state_table,
                                className="table-container",
                            ),
                        ],
                        className="d-inline-block align-top",
                        style={"width": "50%", "paddingRight": "10px"},
                    ),
                    html.Div(
                        [
                            html.H2('City Cost of Living',
                                    className="text-center"),
                            html.Div(
                                city_table,
                                className="table-container",
                            ),
                        ],
                        className="d-inline-block align-top",
                        style={"width": "50%", "paddingLeft": "10px"},
                    ),
                ],
                className="mb-4",
            ),
            id="table-collapse",
            is_open=False,
        ),
    ]
)



# ********************************* CALLBACKS *********************************
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
    Output("state-table-body", "children"),
    Input("state-input", "value")
)
def update_state_table(state):
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


@callback(  # Filters Cost of Living Table based on city
    Output("city-table-body", "children"),
    Input("state-input", "value"),
    Input("city-input", "value")
)
def update_city_table(state_input, city_input):
    filtered_data = df_col_city_data

    if city_input:
        # Split the input by spaces
        cities = city_input.split()

        # Create a regex pattern to match partial city names
        pattern = "|".join(cities)

        # Filter the data based on the pattern
        filtered_data = filtered_data[filtered_data["city"].str.contains(
            pattern, case=False, regex=True)]

    if state_input:
        # Split the input by spaces
        states = state_input.split()

        # Create a regex pattern to match partial city names
        pattern = "|".join(states)

        # Filter the data based on the pattern
        filtered_data = filtered_data[filtered_data["state"].str.contains(
            pattern, case=False, regex=True)]

    table_rows = [
        html.Tr(
            [
                html.Td(row["city"], className="cell"),
                html.Td(row["state"], className="cell"),
                html.Td(row["index"], className="cell"),
            ]
        )
        for _, row in filtered_data.iterrows()
    ]

    return table_rows
