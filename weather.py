from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
def get_weather():
    weather = {'summary': 'windy', 'temperature': 29}
    return render_template('current_weather.html', weather=weather)
