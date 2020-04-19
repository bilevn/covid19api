from unittest import TestCase
from datasources import covid_wiki


class TestCovid(TestCase):
    def test_get_wiki_report(self):
        report = covid_wiki.get_report_countries()
        self.assertTrue('Russia' in list(report['country']))
        self.assertTrue(report.shape[0] > 0)

    def test_get_wiki_report_us(self):
        report = covid_wiki.get_report_us()
        self.assertTrue('Alabama' in list(report['state']))
        test_value = report['confirmed'].values[0] / 5
        test_value = report['deaths'].values[0] / 5
        test_value = report['recovered'].values[0] / 5

    def test_get_wiki_report_ru(self):
        report = covid_wiki.get_report_ru()
        self.assertTrue('Moscow Oblast' in list(report['state']))
        test_value = report['confirmed'].values[0] / 5
        test_value = report['deaths'].values[0] / 5
        test_value = report['recovered'].values[0] / 5
