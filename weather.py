from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/w')
def get_weather(coords=None):
    if coords == None:
        coords = [0, 0]
    return 'How\'s the weather in {} today?'.format(coords)
