import environ
from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df_job_data, df_col_data, user_lat, user_lon, user_location_string

# ********************************* ENV SETUP *********************************
env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env()


# ********************************* DATA *********************************
filtered_data = df_job_data.copy()
filtered_data['lat'] = filtered_data['lat'].astype(float)
filtered_data['lat'] = filtered_data['lat'].round(1)


# ********************************* DASH COMPONENT *********************************
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
        bgcolor='rgb(51,255,255)',
    ),
    autosize=True,
    margin=dict(l=0, r=0, t=0, b=0),
    scene_aspectmode='auto',
    legend=dict(
        x=0,
        y=1,
        traceorder='normal',
        font=dict(
            family='Arial',
            size=12,
            color='black'
        ),
        bgcolor='rgba(255, 255, 255, 0.5)',
        bordercolor='rgba(0, 0, 0, 0.5)',
        borderwidth=1,
    ),
)


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
                    # className='hide-legend',
                ),
                className="w-100 mb-4"
            ),
            id="chart-collapse",
            is_open=False,
        ),
    ]
)


@callback(  # Show/Hide 3D Chart
    Output("chart-collapse", "is_open"),
    [Input("toggle-chart", "n_clicks")],
    [State("chart-collapse", "is_open")],
)
def toggle_chart(n_clicks, is_open):
    if n_clicks is None:
        return is_open
    return not is_open
