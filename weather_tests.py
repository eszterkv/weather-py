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

    def test_get_coords_for_location(self):
        good_location = 'Budapest'
        bad_location = 'NotReallyBudapest'
        assert weather.get_coords_for_location(good_location) == (47.48974156155466, 19.054009282892107)
        assert weather.get_coords_for_location(bad_location) != (47.48974156155466, 19.054009282892107)

    def test_get_current_weather(self):
        coords = (47.489, 19.054)
        expected_keys = set(['summary', 'temperature', 'feels_like'])
        assert set(weather.get_current_weather(coords).keys()) == expected_keys

    def test_get_weather_data(self):
        coords = (47.489, 19.054)
        expected_keys = [u'hourly', u'currently', u'longitude', u'flags', u'daily', u'offset', u'latitude', u'timezone']
        assert weather.get_weather_data(coords).keys() == expected_keys

    def test_get_units_in_celsius_when_in_hungary(self):
        coords = (47.489, 19.054)
        assert weather.get_weather_data(coords)['flags']['units'] == 'si'


if __name__ == '__main__':
    unittest.main()
