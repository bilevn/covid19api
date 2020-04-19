from api import covid as covid_api
from flask import jsonify, abort
from appvars import app


def check_data(data):
    if len(data) == 0:
        abort(404, 'Data is not found')


@app.route('/covid/countries')
def get_covid_countries_report():
    report = covid_api.get_covid_countries_report()
    check_data(report)
    return jsonify(report)


@app.route('/covid/states/<string:country>')
def get_covid_states_report_by_country(country):
    report = covid_api.get_covid_states_report_by_country(country)
    check_data(report)
    return jsonify(report)


@app.route('/covid/total')
def get_covid_total_stats():
    report = covid_api.get_covid_total_stats()
    check_data(report)
    return jsonify(report)


if __name__ == '__main__':
    app.run(port=5000)
