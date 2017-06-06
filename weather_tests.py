import os
import weather
import unittest

class WeatherTestCase(unittest.TestCase):

    def setUp(self):
        self.app = weather.app.test_client()

    def tearDown(self):
        pass

    def test_weather_gets_location(self):
        location = 'Budapest'
        rv = self.app.get('/')
        assert b'Budapest' in rv.data

    def test_weather_gets_weather_data(self):
        weather = {'summary': 'windy', 'temperature': 29}
        rv = self.app.get('/')
        assert b'sunny' not in rv.data
        assert b'windy' in rv.data
        assert b'29' in rv.data

if __name__ == '__main__':
    unittest.main()
