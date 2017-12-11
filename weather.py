from flask import Flask, render_template, url_for, request, redirect
import json
import requests
import time
from config import *
from geopy.geocoders import GeoNames

app = Flask(__name__)
app.config.update(prod_env)

API_KEY = app.config['DARKSKY_API_KEY']
GEONAMES_USERNAME = app.config['GEONAMES_USERNAME']
geo = GeoNames(username=GEONAMES_USERNAME)

DEFAULT_LOCATION = 'London'

@app.route('/')
def get_weather_for_user_location_or_default():
    location = LocationService.get_user_location_or_default()
    return redirect(url_for('get_weather', location=location))

@app.route('/<location>', methods=['GET', 'POST'])
def get_weather(location):
    if request.method == 'POST':
        return redirect(url_for('get_weather', location=request.form['new_location']))

    coords = LocationService.get_coords_for_location(location) or None
    if coords != None:
        weather, forecast = WeatherService(DarkskyGateway()).get_weather(coords)
        location, country = LocationService.get_location_name(coords)
        return render_template('current_weather.html', location=location, country=country, weather=weather, forecast=forecast)
    else:
        return redirect(url_for('no_such_location'))

@app.route('/widget/<location>')
def get_weather_widget():
    coords = LocationService.get_coords_for_location(location) or None
    if coords != None:
        weather, forecast = WeatherService(DarkskyGateway()).get_weather(coords)
        location, country = LocationService.get_location_name(coords)
        return render_template('widget.html', location=location, country=country, weather=weather)
    else:
        return render_template('widget_not_available.html')

@app.route('/404')
def no_such_location():
    return render_template('404.html')

class LocationService(object):
    @staticmethod
    def get_user_location_or_default():
        return DEFAULT_LOCATION # FIXME

    @staticmethod
    def get_coords_for_location(location_name):
        location = geo.geocode(location_name)
        if location == None:
            return None
        return (location.latitude, location.longitude)

    @staticmethod
    def get_location_name(coords):
        lat, lng = coords
        api_url = 'http://api.geonames.org/findNearbyPlaceNameJSON?lat={}&lng={}&username={}'
        location = requests.get(api_url.format(lat, lng, GEONAMES_USERNAME))
        res_json = location.json().get('geonames')[0]
        loc_name = res_json.get('name')
        country = res_json.get('countryName')
        return (loc_name, country)


class WeatherService(object):
    def __init__(self, gateway):
        self.gateway = gateway

    def get_weather(self, coords):
        return self.gateway.get_weather(coords)


class DarkskyGateway(object):
    def __init__(self):
        self.api_url = 'https://api.darksky.net/forecast/{}/{},{}?units=auto'

    def get_weather(self, coords):
        latitude, longitude = coords
        weather_data = requests.get(self.api_url.format(API_KEY, latitude, longitude))
        return self._format_weather(weather_data.json())

    def _format_weather(self, weather_data):
        weather_now = weather_data.get('currently')
        alerts = weather_data.get('alerts')
        daily_data = weather_data.get('daily')
        forecast_data = daily_data.get('data')
        weather_today = forecast_data[0]

        weather = {
            'summary': weather_now.get('summary'),
            'temperature': int(round(weather_now.get('temperature'))),
            'feels_like': int(round(weather_now.get('apparentTemperature'))),
            'icon': weather_now.get('icon'),
            'daily_forecast': weather_today.get('summary'),
            'daily_min_temp': int(round(weather_today.get('temperatureMin'))),
            'daily_max_temp': int(round(weather_today.get('temperatureMax'))),
            'alerts': [alert.get('title') for alert in alerts] if alerts else None,
            'units': weather_data.get('flags').get('units')
        }

        forecast = [
            {
                'day': time.strftime('%a %d %b', time.gmtime(forecast_data[day].get('time'))),
                'icon': forecast_data[day].get('icon'),
                'summary': forecast_data[day].get('summary'),
                'min_temp': int(round(forecast_data[day].get('temperatureMin'))),
                'max_temp': int(round(forecast_data[day].get('temperatureMax'))),
            } for day in range(2, len(forecast_data))
        ]

        return (weather, forecast)


if __name__ == '__main__':
	with app.app_context():
		app.run()
