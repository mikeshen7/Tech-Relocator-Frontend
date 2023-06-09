import environ
from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from data import df_job_data

# ********************************* ENV SETUP *********************************
env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env()


# ********************************* FUNCTIONS *********************************
def create_figure(dataset):
    filtered_data = dataset.copy()
    filtered_data['lat'] = filtered_data['lat'].astype(float)
    filtered_data['lat'] = filtered_data['lat'].round(1)


    fig = px.scatter_3d(
        filtered_data,
        x='months_experience',
        y='lat', z='salary_avg',
        color='industry',
        symbol='senority'
    )

    fig.update_layout(
        scene=dict(
            xaxis_title='Months Experience',
            yaxis_title='Latitude',
            zaxis_title='Salary',
            bgcolor='rgb(255,204,229)',
        ),
        autosize=True,
        margin=dict(l=0, r=0, t=0, b=0),
        scene_aspectmode='auto',
        showlegend=True,
    )
    return fig


# ********************************* DASH COMPONENT *********************************
fig = create_figure(df_job_data)

chart = dbc.Row(
    [
        dbc.Button(
            "Salary vs Experience vs Location Chart",
            id="toggle-chart",
            className="mb-3",
        ),
        dbc.Collapse(
            html.Div(
                dcc.Graph(
                    id='3d-scatter-plot',
                    figure=fig,
                ),
                className="w-100 mb-4"
            ),
            id="chart-collapse",
            is_open=False,
        ),
    ]
)

# ********************************* CALLBACKS *********************************


@callback(  # Show/Hide 3D Chart
    Output("chart-collapse", "is_open"),
    [Input("toggle-chart", "n_clicks")],
    [State("chart-collapse", "is_open")],
)
def toggle_chart(n_clicks, is_open):
    if n_clicks is None:
        return is_open
    return not is_open


@callback(  # Update chart with filtered data
    Output("3d-scatter-plot", "figure"),
    Input("filtered_job_data", "data"),
)
def update_chart(json_job_data):
    filtered_data = pd.read_json(json_job_data, orient='split')
    fig = create_figure(filtered_data)

    return fig

