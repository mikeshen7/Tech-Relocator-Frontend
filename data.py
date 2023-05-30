import pandas as pd
import environ
import requests
import geocoder


# ********************************* ENV SETUP *********************************
env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env()


# ********************************* FUNCTIONS *********************************


def get_job_data():
    l_url = env('BACKEND_BASE_URL') + 'api/v1/job_data/'
    l_response = requests.get(l_url)
    l_api_data = l_response.json()

    df = pd.DataFrame(l_api_data)
    df = df.set_index('id')
    df = df.dropna(subset=['salary_high'])
    df = df.dropna(subset=['months_experience'])
    df['salary_high'] = df['salary_high'].astype(float)
    df['salary_low'] = df['salary_low'].astype(float)
    df['months_experience'] = df['months_experience'].astype(int)
    df['salary_avg'] = (df['salary_high'] + df['salary_low']) / 2

    return df


def get_col_data():
    l_url = env('BACKEND_BASE_URL') + 'api/v1/col/'
    l_response = requests.get(l_url)
    l_api_data = l_response.json()

    df = pd.DataFrame(l_api_data)
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


def get_geolocation():  # Get the user's geolocation using IP address
    g = geocoder.ip('me')
    if g.ok:
        user_lat = g.latlng[0]
        user_lon = g.latlng[1]
        user_location_string = f'Lat: {user_lat}.  Lon: {user_lon}.'
    else:
        user_lat = 39.828175
        user_lon = -98.5795
        user_location_string = f'Location not found'
    return user_lat, user_lon, user_location_string


# ********************************* VARIABLES *********************************

df_job_data = get_job_data()
df_col_data = get_col_data()
user_lat, user_lon, user_location_string = get_geolocation()
