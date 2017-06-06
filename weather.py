from flask import Flask, render_template, url_for, request
import json
from config import *

app = Flask(__name__)
app.config.update(dev_env)

API_KEY = app.config['DARKSKY_API_KEY']

weather = {'summary': 'windy', 'temperature': 29}

@app.route('/')
def get_weather(location='Budapest'):
    latitude, longitude = get_coords_for_location(location)
    weather = get_current_weather(latitude, longitude)
    return render_template('current_weather.html', location=location, weather=weather)

def get_coords_for_location(location):
    if location == 'Budapest':
        return (47.48974156155466, 19.054009282892107)
    return None

def get_current_weather(latitude, longitude):
    api_url = 'https://api.darksky.net/forecast/{}/{},{}'.format(API_KEY, latitude, longitude)
    res = json.loads(api_url)
    # return 'https://api.darksky.net/forecast/{}/{},{}'.format(API_KEY, latitude, longitude)
    # return {'summary': 'windy', 'temperature': 29}
    print(res)
    return None
