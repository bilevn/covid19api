from app import app
from unittest import TestCase


class TestIntegrations(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_covid_countries_report(self):
        response = self.app.get('/covid/countries')
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(response.json) > 0, True)

    def test_get_covid_report_on_date(self):
        response = self.app.get('/covid/states/Russia')
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(response.json) > 0, True)

        response = self.app.get('/covid/states/United%20States')
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(response.json) > 0, True)

    def test_get_covid_total_stats(self):
        response = self.app.get('/covid/total')
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.json['data']['confirmed'] > 2000000)
        self.assertTrue(response.json['data']['deaths'] > 150000)
        self.assertTrue(response.json['data']['recovered'] > 500000)
