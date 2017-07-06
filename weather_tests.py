import os
import weather
import unittest
import mock

class WeatherTestCase(unittest.TestCase):

    def setUp(self):
        self.app = weather.app.test_client()
        self.API_KEY = weather.app.config['DARKSKY_API_KEY']
        self.mock_requests = mock.Mock()

    def tearDown(self):
        pass

    def test_weather_gets_location(self):
        latitude = 47.48974156155466
        longitude = 19.054009282892107
        rv = self.app.get('/')
        assert b'Budapest' in rv.data

    def test_get_units_in_celsius_when_in_hungary(self):
        coords = (47.489, 19.054)
        assert weather.get_weather_data(coords)['flags']['units'] == 'si'

    def test_get_coords_for_location(self):
        good_location = 'Budapest'
        bad_location = 'Southampton'
        not_a_location = 'ReallyNoPlaceCalledHere'
        assert weather.get_coords_for_location(good_location) == (47.49801, 19.03991)
        assert weather.get_coords_for_location(bad_location) != (47.49801, 19.03991)
        assert weather.get_coords_for_location(not_a_location) != (47.49801, 19.03991)
        assert weather.get_coords_for_location(not_a_location) == None

    def test_get_weather_data(self):
        coords = (47.489, 19.054)

        expected_weather_data_keys = set([u'hourly', u'currently', u'longitude', u'flags',
                                            u'daily', u'offset', u'latitude', u'timezone'])
        assert set(weather.get_weather_data(coords).keys()) == expected_weather_data_keys

        expected_daily_keys = set([u'summary', u'icon', u'data'])
        assert set(weather.get_weather_data(coords)['daily'].keys()) == expected_daily_keys

        expected_weekly_keys = set([u'time', u'icon', u'temperatureMin', u'temperatureMax'])
        assert len(weather.get_weather_data(coords)['daily']['data']) == 8
        assert expected_weekly_keys <= set(weather.get_weather_data(coords)['daily']['data'][0].keys())

    def test_get_current_weather(self):
        coords = (47.489, 19.054)
        keys = set(weather.get_current_weather(coords).keys())
        expected_keys = set(['summary', 'temperature', 'feels_like', 'icon',
                                'daily_forecast', 'daily_min_temp', 'daily_max_temp', 'alerts'])
        assert keys <= expected_keys


if __name__ == '__main__':
    unittest.main()
