from flask import Flask, render_template, url_for, request
import json
import requests
import time
from config import *
from geopy.geocoders import GeoNames

app = Flask(__name__)
app.config.update(prod_env)
geo = GeoNames(username=app.config['GEONAMES_USERNAME'])

API_KEY = app.config['DARKSKY_API_KEY']

# NOTE: for styling purposes, to avoid API calls
# @app.route('/mock')
# def mock():
#     return render_template('mock.html')

@app.route('/')
def get_weather(location='Budapest'): # FIXME get user's location
    coords = get_coords_for_location(location)
    return render_template('current_weather.html', location=location, weather=get_weather(coords))

def get_coords_for_location(location_name):
    location = geo.geocode(location_name)
    return (location.latitude, location.longitude) if location else None

def get_weather_data_from_api(coords):
    latitude, longitude = coords
    api_url = 'https://api.darksky.net/forecast/{}/{},{}?units=auto'.format(API_KEY, latitude, longitude)
    res = requests.get(api_url)
    return res.json()

def get_weather(coords):
    weather_data = get_weather_data_from_api(coords)
    weather_now = weather_data.get('currently')
    daily_data = weather_data.get('daily')
    forecast_data = daily_data.get('data')
    weather_today = forecast_data[0]
    alerts = weather_data.get('alerts')

    weather = {
        'summary': weather_now.get('summary'),
        'temperature': int(round(weather_now.get('temperature'))),
        'feels_like': int(round(weather_now.get('apparentTemperature'))),
        'icon': weather_now.get('icon'),
        'daily_forecast': weather_today.get('summary'),
        'daily_min_temp': int(round(weather_today.get('temperatureMin'))),
        'daily_max_temp': int(round(weather_today.get('temperatureMax'))),
        'alerts': [alert.get('title') for alert in alerts] if alerts else None,
    }

    forecast = [
        {
            'day': time.strftime('%a %d %b', time.gmtime(forecast_data[day].get('time'))),
            'icon': forecast_data[day].get('icon'),
            'min_temp': int(round(forecast_data[day].get('temperatureMin'))),
            'max_temp': int(round(forecast_data[day].get('temperatureMax'))),
        } for day in range(1, len(forecast_data))
    ]

    return (weather, forecast)


if __name__ == '__main__':
	with app.app_context():
		app.run()
