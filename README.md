# COVID-19 Python Flask API
Real-time coronavirus API based on COVID-19 data from Wikipedia.
The API is written in Python with Flask framework. This is a simplified
version of the API used by [Routitude COVID-19 Monitoring Service](https://www.routitude.com/).

The API provides data with basic statistics such as the number of 
confirmed cases, the number of deaths and the number of recovered patients
for almost each country, with administrative divisions for
United States and Russia.

## Data sources

Data comes from Wikipedia pages describing current status of coronavirus
outbreak in different countries. At this moment the project retrieves 
COVID-19 statistics from the following Wikipedia pages:
- [2019-20 Coronavirus pandemic by country and territory](https://en.wikipedia.org/wiki/2019%E2%80%9320_coronavirus_pandemic_by_country_and_territory)
- [2020 coronavirus pandemic in Russia](https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Russia)
- [Timeline of the 2020 coronavirus pandemic in the United States](https://en.wikipedia.org/wiki/Timeline_of_the_2020_coronavirus_pandemic_in_the_United_States)

## Requirements

- Python
- SQLAlchemy supported database (tested with PostgreSQL)

## Installation

Install requirements:
```bash
pip install -r requiremets
```

Set database URI environment variable:
```bash
export COVID19API_DB_URI=<your database uri>
```

Set up database:
```bash
python manage.py db upgrade
```

## Usage

The following command updates the data in the project database. 
You can run it manually or with the help of automation tools 
whenever you want to update COVID-19 data to provide the most 
recent coronavirus statistics from Wikipedia through the API.
```bash
python manage.py update_covid_data
```

Run Flask development server:
```bash
python app.py
```

## Tests

Test the API:
```bash
nosetests .
```

Test Wikipedia scraping logic:
```bash
nosetests datasources
```

## Contribution:

You are welcome to contribute to this project. Here are some ideas
on possible new features:
- Regional data for more countries
- Historical data
