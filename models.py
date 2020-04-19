import logging
from config import LOGGER_FORMAT
from appvars import db
from sqlalchemy import Column, Index
from datasources import covid_wiki, utils
import datetime
import numpy as np

logging.basicConfig(format=LOGGER_FORMAT, level=logging.DEBUG)


class CovidWiki(db.Model):
    """
    Coronavirus (COVID-19) Wikipedia statistics
    """

    __tablename__ = 'covid_wiki'

    territory_id = Column(db.VARCHAR(length=256), nullable=False, primary_key=True)
    update_time = Column(db.TIMESTAMP(), nullable=False)
    country = Column(db.VARCHAR(length=128), nullable=False)
    state = Column(db.VARCHAR(length=128), nullable=True)
    confirmed = Column(db.INTEGER(), nullable=True)
    deaths = Column(db.INTEGER(), nullable=True)
    recovered = Column(db.INTEGER(), nullable=True)

    @staticmethod
    def get_id(country, state):
        """
        Create unique territory id based on country name and state name
        :param country: country name
        :param state: state name
        :return: unique territory id string
        """
        state = '-'+state if state is not None else ''
        return (country.lower()+state.lower()).replace(' ', '_')

    @staticmethod
    def get_wiki_last_report():
        """
        Retrieve last data from table
        :return: dict with stats by country
        """
        report_last_data = db.session.query(CovidWiki).all()
        report_last = {}
        for r in report_last_data:
            stats = {}
            for name in utils.STAT_NAMES:
                stats[name] = getattr(r, name)
            report_last[r.territory_id] = stats
        return report_last

    def update_data_by_dataframe(self, df):
        """
        Update data in db by DataFrame with COVID-19 stats
        :param df: pandas DataFrame with COVID-19 stats
        """
        report = df.to_dict(orient='records')
        report_last = self.get_wiki_last_report()
        for value in report:
            territory_id = self.get_id(value['country'], value['state'])
            value['territory_id'] = territory_id
            changed = (
                (len(report_last) == 0) or
                (territory_id not in report_last) or
                (utils.get_covid_values_sum(value) !=
                 utils.get_covid_values_sum(report_last[territory_id]))
            )
            if not changed:
                continue
            logging.info(f"Updating data for territory: {territory_id}")
            data = dict(value)
            for name in utils.STAT_NAMES:
                value = data[name]
                if np.isnan(value):
                    data[name] = None
                    continue
                data[name] = int(value)
            data['update_time'] = datetime.datetime.now()
            report = CovidWiki(**data)
            db.session.merge(report)
            db.session.commit()

    def update_data(self):
        """
        Update data in db with all reports
        """
        logging.info('Updating countries data')
        self.update_data_by_dataframe(covid_wiki.get_report_countries())
        logging.info('Updating Russia states data')
        self.update_data_by_dataframe(covid_wiki.get_report_ru())
        logging.info('Updating USA states data')
        self.update_data_by_dataframe(covid_wiki.get_report_us())

    def to_dict(self):
        """
        Create dict from model object
        :return: dict
        """
        return {
            'report_date': utils.datetime2string(self.update_time, time=True),
            'country':     self.country,
            'state':       self.state,
            'confirmed':   self.confirmed,
            'deaths':      self.deaths,
            'recovered':   self.recovered,
            'active':      utils.get_active(self.confirmed, self.deaths, self.recovered)
        }


Index('ix_covid_wiki_country', CovidWiki.country)
Index('ix_covid_wiki_state', CovidWiki.state)
