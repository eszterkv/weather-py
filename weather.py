from flask import Flask, render_template, url_for, request
import json
import requests
from config import *

app = Flask(__name__)
app.config.update(dev_env)

API_KEY = app.config['DARKSKY_API_KEY']

weather = {'summary': 'windy', 'temperature': 29}

@app.route('/')
def get_weather(location='Budapest'): # FIXME get user's location
    coords = get_coords_for_location(location)
    weather = get_current_weather(coords)
    return render_template('current_weather.html', location=location, weather=weather)

def get_coords_for_location(location): # FIXME i'm totally wrong
    if location == 'Budapest':
        return (47.48974156155466, 19.054009282892107)
    return None

def get_weather_data(coords):
    latitude, longitude = coords
    api_url = 'https://api.darksky.net/forecast/{}/{},{}?units=auto'.format(API_KEY, latitude, longitude)
    res = requests.get(api_url)
    return res.json()

def get_current_weather(coords):
    return get_weather_data(coords)['currently']
