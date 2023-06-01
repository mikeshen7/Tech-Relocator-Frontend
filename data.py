import pandas as pd
import environ
import requests
import geocoder
from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc


# ********************************* ENV SETUP *********************************
env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env()


# ********************************* FUNCTIONS *********************************


def get_job_data():
    url = env('BACKEND_BASE_URL') + 'api/v1/job_data/'
    response = requests.get(url)
    api_data = response.json()

    df = pd.DataFrame(api_data)
    df = df.set_index('id')
    df = df.dropna(subset=['salary_high'])
    df = df.dropna(subset=['months_experience'])
    df['salary_high'] = df['salary_high'].astype(float)
    df['salary_low'] = df['salary_low'].astype(float)
    df['months_experience'] = df['months_experience'].astype(int)
    df['salary_avg'] = (df['salary_high'] + df['salary_low']) / 2

    return df


def get_col_data():
    url = env('BACKEND_BASE_URL') + 'api/v1/col/'
    response = requests.get(url)
    api_data = response.json()

    df = pd.DataFrame(api_data)
    df = df.set_index('rank')
    df = df.drop('id', axis=1)
    df['index'] = df['index'].astype(float)
    df['grocery'] = df['grocery'].astype(float)
    df['housing'] = df['housing'].astype(float)
    df['utilities'] = df['utilities'].astype(float)
    df['transportation'] = df['transportation'].astype(float)
    df['health'] = df['health'].astype(float)
    df['misc'] = df['misc'].astype(float)

    return df


def get_col_city_data():
    url = env('BACKEND_BASE_URL') + 'api/v1/col_city/'
    response = requests.get(url)
    api_data = response.json()

    df = pd.DataFrame(api_data)
    df = df.set_index('id')
    df['index'] = df['index'].astype(float)

    return df


# ********************************* VARIABLES *********************************

df_job_data = get_job_data()
df_col_data = get_col_data()
df_col_city_data = get_col_city_data()
location_string = "nothing yet"
num_jobs = len(df_job_data)
filtered_job_data = df_job_data.copy()


# ********************************* VARIABLES *********************************
data = html.Div(
    [
        dcc.Store(id='filtered_job_data'),
        dcc.Geolocation(id="geolocation"),
        dcc.Store(id='user_lat_lon'),
    ]
)


@callback(  # Filters based on job title or skills
    Output("filtered_job_data", "data"),
    Output('col-toggle-output', 'children'),
    Input("state-input", "value"),
    Input("city-input", "value"),
    Input("title-input", "value"),
    Input("skills-input", "value"),
    Input('col-toggle', 'value'),
)
def filter_data(state, city, title, skills, col_value):
    global filtered_job_data
    global num_jobs

    # Initialize to full list of jobs
    filtered_job_data = df_job_data.copy()

    if state:
        filtered_job_data = filtered_job_data[filtered_job_data['state'].str.contains(
            state, case=False, na=False)]

    if city:
        filtered_job_data = filtered_job_data[filtered_job_data['city'].str.contains(
            city, case=False, na=False)]

    if title:
        filtered_job_data = filtered_job_data[filtered_job_data['title'].str.contains(
            title, case=False, na=False)]

    if skills:
        filtered_job_data = filtered_job_data[filtered_job_data['skills'].str.contains(
            skills, case=False, na=False)]

    if col_value:
        for index, row in filtered_job_data.iterrows():
            city = row['city']
            state = row['state']

            if city in df_col_city_data['city'].values:
                col_index = df_col_city_data.loc[df_col_city_data['city']
                                                 == city, 'index'].iloc[0]
            elif state in df_col_data['state'].values:
                col_index = df_col_data.loc[df_col_data['state']
                                            == state, 'index'].iloc[0]

            filtered_job_data.at[index, 'salary_avg'] = round(
                (row['salary_avg'] * 100 / col_index))

            filtered_job_data.at[index, 'salary_high'] = round(
                (row['salary_high'] * 100 / col_index))

            filtered_job_data.at[index, 'salary_low'] = round(
                (row['salary_low'] * 100 / col_index))

    job_data_json = filtered_job_data.to_json(
        date_format='iso', orient='split')

    num_jobs = len(filtered_job_data)

    if col_value:
        col_text = 'Adjusted for Cost of Living'
    else:
        col_text = 'Not Adjusted for Cost of Living'

    return job_data_json, col_text



@callback( # Geolocation callback
    Output("location_string", "children"),
    Output("user_lat_lon", "data"),
    Input("geolocation", "local_date"),
    Input("geolocation", "position"),
)
def get_geolocation(date, pos):
    if pos is None:
        pos = {'lat': 47.6034, 'lon': -122.3414, 'accuracy': 1, 'alt': None, 'alt_accuracy': None, 'speed': None,
         'heading': None}
        location_string = "Using generic location of Seattle, WA"
    else:
        location_string = f"As of {date} your location was: lat {pos['lat']}, lon {pos['lon']}, accuracy {pos['accuracy']} meters"

    location_json = {
        "user_lat": pos['lat'],
        "user_lon": pos['lon']
    }

    return location_string, location_json
