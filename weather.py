from flask import Flask, render_template, url_for, request
import json
import requests
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
    return render_template('current_weather.html', location=location, weather=get_current_weather(coords))

def get_coords_for_location(location_name):
    location = geo.geocode(location_name)
    return (location.latitude, location.longitude) if location else None

def get_weather_data(coords):
    latitude, longitude = coords
    api_url = 'https://api.darksky.net/forecast/{}/{},{}?units=auto'.format(API_KEY, latitude, longitude)
    res = requests.get(api_url)
    return res.json()

def get_current_weather(coords):
    current_data = get_weather_data(coords).get('currently')
    daily_data = get_weather_data(coords).get('daily')
    daily_forecast = daily_data.get('data')[0]
    alerts = get_weather_data(coords).get('alerts')
    current_weather = {
        'summary': current_data.get('summary'),
        'temperature': int(round(current_data.get('temperature'))),
        'feels_like': int(round(current_data.get('apparentTemperature'))),
        'icon': current_data.get('icon'),
        'daily_forecast': daily_forecast.get('summary'),
        'daily_min_temp': int(round(daily_forecast.get('temperatureMin'))),
        'daily_max_temp': int(round(daily_forecast.get('temperatureMax'))),
        'alerts': [alert.get('title') for alert in alerts] if alerts else None,
    }
    return current_weather

if __name__ == '__main__':
	with app.app_context():
		app.run()
