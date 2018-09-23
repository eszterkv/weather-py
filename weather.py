from flask import Flask, render_template, url_for, request, redirect
from flask_restful import Resource, Api, abort
import json
import requests
import time
import datetime
from config import *
from geopy.geocoders import GeoNames

app = Flask(__name__)
app.config.update(prod_env)
api = Api(app)

API_KEY = app.config['DARKSKY_API_KEY']
GEONAMES_USERNAME = app.config['GEONAMES_USERNAME']
geo = GeoNames(username=GEONAMES_USERNAME)

DEFAULT_LOCATION = 'London'

class CurrentWeather(Resource):
    def get(self):
        location = LocationService.get_user_location_or_default()
        coords = LocationService.get_coords_for_location(location) or None
        if coords != None:
            weather, forecast = WeatherService(DarkskyGateway()).get_weather(coords)
            location, country = LocationService.get_location_name(coords)
            return {'current': weather, 'forecast': forecast}
        else:
            abort(404, message="User location or default not found: {}".format(location))

class CurrentWeatherAtLocation(Resource):
    def get(self, location):
        coords = LocationService.get_coords_for_location(location) or None
        if coords != None:
            weather, forecast = WeatherService(DarkskyGateway()).get_weather(coords)
            location, country = LocationService.get_location_name(coords)
            return {'current': weather, 'forecast': forecast}
        else:
            abort(404, message="Location not found: {}".format(location))


api.add_resource(CurrentWeather, '/')
api.add_resource(CurrentWeatherAtLocation, '/<location>')


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

    def get_forecast(self, coords, date):
        return self.gateway.get_forecast(coords, date)


class DarkskyGateway(object):
    def __init__(self):
        self.api_url = 'https://api.darksky.net/forecast/{}/{},{}?units=auto'
        self.forecast_api_url = 'https://api.darksky.net/forecast/{}/{},{},{}?units=auto'

    def get_weather(self, coords):
        latitude, longitude = coords
        weather_data = requests.get(self.api_url.format(API_KEY, latitude, longitude))
        return self._format_weather(weather_data.json(), make_forecast=True)

    def get_forecast(self, coords, date):
        latitude, longitude = coords
        date = datetime.datetime(date).strftime('%s')
        weather_data = requests.get(self.forecast_api_url.format(API_KEY, latitude, longitude, date))
        return self._format_weather(weather_data.json())

    def _format_weather(self, weather_data, make_forecast=False):
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
            } for day in range(1, len(forecast_data))
        ]

        return (weather_now, forecast_data or None)


if __name__ == '__main__':
	with app.app_context():
		app.run()
