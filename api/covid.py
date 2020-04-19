from appvars import db
from sqlalchemy import func, and_
from datasources import utils
from models import CovidWiki


def get_covid_countries_report():
    """
    Get covid report for all countries
    :return: dict
    """
    data = db.session.query(CovidWiki).filter(CovidWiki.state.is_(None)).all()
    return [v.to_dict() for v in data]


def get_covid_states_report_by_country(country):
    """
    Get covid report for states by country name
    :param country: country name
    :return: dict
    """
    data = db.session.query(CovidWiki).filter(and_(
        CovidWiki.state.isnot(None),
        func.lower(CovidWiki.country) == country.lower(),
    )).all()
    return [v.to_dict() for v in data]


def get_covid_total_stats():
    """
    Get total stats covid report
    :return: dict
    """
    def to_dict(v):
        return {'confirmed': v[0], 'deaths': v[1], 'recovered': v[2]}

    curr = db.session.query(
        func.sum(CovidWiki.confirmed),
        func.sum(CovidWiki.deaths),
        func.sum(CovidWiki.recovered),
        func.max(CovidWiki.update_time)
    ).filter(CovidWiki.state.is_(None)).one()
    return {
        'data': to_dict(curr),
        'last_update_time': utils.datetime2string(curr[3], time=True)
    }
