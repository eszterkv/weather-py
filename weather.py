from flask import Flask, render_template, url_for
app = Flask(__name__)

weather = {'summary': 'windy', 'temperature': 29}

@app.route('/')
def get_weather(location='Budapest'):
    return render_template('current_weather.html', location=location, weather=weather)
