import environ
from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from data import df_job_data


# ********************************* ENV SETUP *********************************
env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env()


# ********************************* ENV SETUP *********************************
user_lat = 0
user_lon = 0

# ********************************* FUNCTIONS *********************************


def create_figure(dataset):
    figure = go.Figure(
        data=[
            go.Scattermapbox(
                lat=dataset['lat'],
                lon=dataset['lon'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=10,
                    color=dataset['salary_avg'],
                    colorscale='portland',
                    colorbar=dict(title='Salary'),
                ),
                text=dataset['title'],
                hovertemplate=(
                    "<b>Title: %{customdata[0]} </b> <br>"
                    "<b>Average Salary:</b>%{customdata[7]}<br>"
                    "<b>Salary Range:</b> %{customdata[4]} - %{customdata[5]}<br>"
                    "<b>Employment Type:</b> %{customdata[1]}<br>"
                    "<b>Industry:</b> %{customdata[2]}<br>"
                    "<b>Education:</b> %{customdata[3]}<br>"
                    "<b>Skills:</b> %{customdata[6]}"
                    "<extra></extra>"
                ),
                customdata=list(zip(
                    dataset['title'],
                    dataset['employment_type'],
                    dataset['industry'],
                    dataset['education'],
                    dataset['salary_low'],
                    dataset['salary_high'],
                    dataset['skills'],
                    dataset['salary_avg'],
                )),
            )
        ],
        layout=go.Layout(
            mapbox=dict(
                style='mapbox://styles/mapbox/dark-v10',
                accesstoken=env('MAPBOX'),
                center=dict(lat=user_lat, lon=user_lon),
                zoom=5,
                uirevision=True,
            ),
            autosize=True
        )
    ).update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0,
        )
    )

    return figure


# ********************************* DASH COMPONENT *********************************
fig = create_figure(df_job_data)

job_map = dbc.Row(
    [
        dbc.Button(
            "Job Map",
            id="toggle-map",
            color="primary",
            className="mb-3 w-100",
            style={"width": "100%"}
        ),

        dbc.Collapse(
            [
                dcc.Graph(
                    id='map-graph',
                    figure=fig,
                    className="w-100 mb-4"
                ),
                html.Div(id="location_string"),
                html.P(f'Number of jobs: 0', id="num_jobs_display"),
            ],
            id='map-collapse',
            is_open=False,
        ),
    ]
)


# ********************************* CALLBACKS *********************************
@callback(  # Show/Hide Map
    Output("map-collapse", "is_open"),
    [Input("toggle-map", "n_clicks")],
    [State("map-collapse", "is_open")],
)
def toggle_map(n_clicks, is_open):
    if n_clicks is None:
        return is_open
    return not is_open


@callback(  # Update map with filtered data
    Output("num_jobs_display", "children"),
    Output("map-graph", "figure"),
    Input("filtered_job_data", "data"),
    Input("user_lat_lon", "data"),
)
def update_map(json_job_data, json_lat_lon):
    filtered_data = pd.read_json(json_job_data, orient='split')
    global user_lat, user_lon
    user_lat = json_lat_lon['user_lat']
    user_lon = json_lat_lon['user_lon']

    fig = create_figure(filtered_data)

    return f'Number of jobs: {len(filtered_data)}', fig
