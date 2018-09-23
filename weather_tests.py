# This Python file uses the following encoding: utf-8
import os
import weather
import unittest
import mock

class WeatherTestCase(unittest.TestCase):

    def setUp(self):
        self.app = weather.app.test_client()
        self.API_KEY = weather.app.config['DARKSKY_API_KEY']
        self.mock_requests = mock.Mock()
        self.test_coords = (47.489, 19.054)
        self.long_test_coords = (47.49801, 19.03991)
        self.test_date = 0;

    def tearDown(self):
        pass

    def test_get_weather_gets_default_location(self):
        rv = self.app.get('/')
        assert b'London' in rv.data

    def test_get_weather_for_specific_location(self):
        rv = self.app.get('/Stuttgart')
        assert b'Stuttgart, Germany' in rv.data

    def test_404_shows_message(self):
        rv = self.app.get('/404')
        assert b'The location you entered does not exist' in rv.data

    def test_get_weather_returns_error_page_if_location_not_found(self):
        rv = self.app.get('/noSuchLocation!!!!Really')
        assert rv._status_code == 302
        assert '404' in rv.headers.get('Location')

    def test_redirect_in_location_chooser(self):
        rv = self.app.post('/Stuttgart', data={'new_location': 'Budapest'})
        assert b'Budapest' in rv.data
        assert b'Stuttgart' not in rv.data

    def test_locationservice_gets_coords_for_location(self):
        good_location = 'Budapest'
        bad_location = 'Southampton'
        not_a_location = 'ReallyNoPlaceCalledHere'
        assert weather.LocationService.get_coords_for_location(good_location) == self.long_test_coords
        assert weather.LocationService.get_coords_for_location(bad_location) != self.long_test_coords
        assert weather.LocationService.get_coords_for_location(not_a_location) != self.long_test_coords
        assert weather.LocationService.get_coords_for_location(not_a_location) == None

    def test_darksky_gateway_gets_units_in_celsius_when_in_hungary(self):
        assert weather.DarkskyGateway().get_weather(self.test_coords)[0]['units'] == 'si'

    def test_darksky_gateway_gets_weather_data(self):
        gateway = weather.DarkskyGateway()
        weather_now, forecast = gateway.get_weather(self.test_coords)
        weather_now_keys = set(weather_now.keys())
        forecast_keys = set(forecast[0].keys())
        expected_weather_now_keys = set(['summary', 'temperature', 'feels_like', 'icon',
                                'daily_forecast', 'daily_min_temp', 'daily_max_temp', 'alerts', 'units'])
        expected_forecast_keys = set(['day', 'icon', 'summary', 'min_temp', 'max_temp'])
        assert weather_now_keys <= expected_weather_now_keys
        assert forecast_keys <= expected_forecast_keys
        assert len(forecast) == 6

    def test_get_weather(self):
        gateway = weather.DarkskyGateway()
        weather_now, forecast = weather.WeatherService(gateway).get_weather(self.test_coords)
        weather_now_keys = set(weather_now.keys())
        forecast_keys = set(forecast[0].keys())
        expected_weather_now_keys = set(['summary', 'temperature', 'feels_like', 'icon',
                                'daily_forecast', 'daily_min_temp', 'daily_max_temp', 'alerts', 'units'])
        expected_forecast_keys = set(['day', 'icon', 'summary', 'min_temp', 'max_temp'])
        assert weather_now_keys <= expected_weather_now_keys
        assert forecast_keys <= expected_forecast_keys
        assert len(forecast) == 6


if __name__ == '__main__':
    unittest.main()
