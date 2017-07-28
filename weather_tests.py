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

    def test_get_weather_gets_default_location(self):
        rv = self.app.get('/')
        assert b'Budapest' in rv.data

    def test_get_weather_for_specific_location(self):
        rv = self.app.get('/Stuttgart')
        assert b'Stuttgart' in rv.data

    def test_redirect_in_location_chooser(self):
        rv = self.app.post('/Stuttgart', data={'new_location': 'London'})
        assert b'London' in rv.data
        assert b'Stuttgart' not in rv.data

    def test_locationservice_gets_coords_for_location(self):
        good_location = 'Budapest'
        bad_location = 'Southampton'
        not_a_location = 'ReallyNoPlaceCalledHere'
        assert weather.LocationService.get_coords_for_location(good_location) == (47.49801, 19.03991)
        assert weather.LocationService.get_coords_for_location(bad_location) != (47.49801, 19.03991)
        assert weather.LocationService.get_coords_for_location(not_a_location) != (47.49801, 19.03991)
        assert weather.LocationService.get_coords_for_location(not_a_location) == None

    def test_darksky_gateway_gets_units_in_celsius_when_in_hungary(self):
        coords = (47.489, 19.054)
        assert weather.DarkskyGateway().get_weather(coords)[0]['units'] == 'si'

    def test_darksky_gateway_gets_weather_data(self):
        coords = (47.489, 19.054)
        gateway = weather.DarkskyGateway()
        weather_now, forecast = gateway.get_weather(coords)
        weather_now_keys = set(weather_now.keys())
        forecast_keys = set(forecast[0].keys())
        expected_weather_now_keys = set(['summary', 'temperature', 'feels_like', 'icon',
                                'daily_forecast', 'daily_min_temp', 'daily_max_temp', 'alerts', 'units'])
        expected_forecast_keys = set(['day', 'icon', 'summary', 'min_temp', 'max_temp'])
        assert weather_now_keys <= expected_weather_now_keys
        assert forecast_keys <= expected_forecast_keys
        assert len(forecast) == 6

    def test_get_weather(self):
        coords = (47.489, 19.054)
        gateway = weather.DarkskyGateway()
        weather_now, forecast = weather.WeatherService(gateway).get_weather(coords)
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
