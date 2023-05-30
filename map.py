import environ
from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from data import df_job_data, df_col_data, user_lat, user_lon, user_location_string

# ********************************* ENV SETUP *********************************
env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env()


# ********************************* DASH COMPONENT *********************************
fig = go.Figure(
    data=[
        go.Scattermapbox(
            lat=df_job_data['lat'],
            lon=df_job_data['lon'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=10,
                color=df_job_data['salary_avg'],
                colorscale='portland',
                colorbar=dict(title='Salary'),
            ),
            text=df_job_data['title'],
        )
    ],
    layout=go.Layout(
        mapbox=dict(
            style='mapbox://styles/mapbox/dark-v10',
            accesstoken=env('MAPBOX'),
            center=dict(lat=user_lat, lon=user_lon),
            zoom=5,
        ),
        autosize=True
    )
)

fig.update_layout(
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
                html.Div(user_location_string),
                dcc.Graph(
                    id='map-graph',
                    figure=fig,
                    className="w-100 mb-4"
                )
            ],
            id='map-collapse',
            is_open=True,
        ),
    ]
)


@callback(  # Show/Hide Map
    Output("map-collapse", "is_open"),
    [Input("toggle-map", "n_clicks")],
    [State("map-collapse", "is_open")],
)
def toggle_map(n_clicks, is_open):
    if n_clicks is None:
        return is_open
    return not is_open


@callback(  # Filters based on job title or skills
    Output("map-graph", "figure"),
    Input("title-input", "value"),
    Input("skills-input", "value")
)
def update_map(title, skills):
    filtered_data = df_job_data

    if title:
        filtered_data = filtered_data[filtered_data['title'].str.contains(
            title, case=False, na=False)]

    if skills:
        filtered_data = filtered_data[filtered_data['skills'].str.contains(
            skills, case=False, na=False)]

    figure = go.Figure(
        data=[
            go.Scattermapbox(
                lat=filtered_data['lat'],
                lon=filtered_data['lon'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=10,
                    color=filtered_data['salary_avg'],
                    colorscale='portland',
                    colorbar=dict(title='Salary'),
                ),
                text=filtered_data['title'],
                hovertemplate=(
                    "<b>%{customdata[0]} </b> <br>"
                    "<b>Employment Type:</b> %{customdata[1]}<br>"
                    "<b>Industry:</b> %{customdata[2]}<br>"
                    "<b>Education:</b> %{customdata[3]}<br>"
                    "<b>Salary:</b> %{customdata[4]} - %{customdata[5]}<br>"
                    "<b>Skills:</b> %{customdata[6]}"
                    "<extra></extra>"
                ),
                customdata=list(zip(
                    filtered_data['title'],
                    filtered_data['employment_type'],
                    filtered_data['industry'],
                    filtered_data['education'],
                    filtered_data['salary_low'],
                    filtered_data['salary_high'],
                    filtered_data['skills'],
                )),
            )
        ],
        layout=go.Layout(
            mapbox=dict(
                style='mapbox://styles/mapbox/dark-v10',
                accesstoken=env('MAPBOX'),
                center=dict(lat=user_lat, lon=user_lon),
                zoom=5,
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
