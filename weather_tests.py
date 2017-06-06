import os
import weather
import unittest

class WeatherTestCase(unittest.TestCase):

    def setUp(self):
        self.app = weather.app.test_client()
        self.API_KEY = weather.app.config['DARKSKY_API_KEY']

    def tearDown(self):
        pass

    def test_weather_gets_location(self):
        latitude = 47.48974156155466
        longitude = 19.054009282892107
        rv = self.app.get('/')
        assert b'Budapest' in rv.data

    def test_weather_gets_weather_data(self):
        weather = {'summary': 'windy', 'temperature': 29}
        rv = self.app.get('/')
        assert b'sunny' not in rv.data
        assert b'windy' in rv.data
        assert b'29' in rv.data

    def test_get_coords_for_location(self):
        good_location = 'Budapest'
        bad_location = 'NotReallyBudapest'
        assert weather.get_coords_for_location(good_location) == (47.48974156155466, 19.054009282892107)
        assert weather.get_coords_for_location(bad_location) != (47.48974156155466, 19.054009282892107)

    def test_get_current_weather_calls_correct_API_endpoint(self):
        latitude = 47.489
        longitude = 19.054
        assert weather.get_current_weather(latitude, longitude) == 'https://api.darksky.net/forecast/' + self.API_KEY + '/47.489,19.054'

if __name__ == '__main__':
    unittest.main()
