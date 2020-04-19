import re
import requests
import datetime
import numpy as np
import pandas as pd


class ParsingFailed(Exception):
    """Parsing Exception"""
    pass


DATE_FORMAT = '%d-%m-%Y'
DATETIME_FORMAT = '%d-%m-%Y %H.%M.%S'
STAT_NAMES = ['confirmed', 'deaths', 'recovered']


def string2datetime(value):
    """Covert string to datetime"""
    return datetime.datetime.strptime(value, DATE_FORMAT)


def datetime2string(date, time=False):
    """Covert datetime to string"""
    return date.strftime(DATETIME_FORMAT if time else DATE_FORMAT)


def get_wiki_table_df(page_url, match_string):
    """
    Get table from Wiki page by page url
    and unique string that must appear in table
    :param page_url: page url
    :param match_string: match string
    :return: pandas DataFrame
    """
    response = requests.get(page_url)
    df = None
    tables = pd.read_html(response.content)
    for table in tables:
        df = table
        if match_string in str(df):
            break
    return df


def wiki_table_df_numeric_column_clean(df, columns, na_values=None):
    """
    Clean numeric columns in dataframe
    :param na_values: list of string values that should be considered as NA value
    :param df: dataframe
    :param columns: columns name to clean
    :return: clean pandas DataFrame
    """
    if na_values is None:
        na_values = ['–']
    df = df.copy()
    for col in columns:
        df.loc[df[col].isin(na_values), col] = np.nan
        df[col] = df[col].apply(lambda x: re.sub("[^0-9]", "", str(x)))
        df[col] = df[col].apply(lambda x: x if np.char.isnumeric(str(x)) else np.nan)
        df[col] = df[col].astype(np.float32)
    return df


def clean_territory_name(value):
    value = re.sub(r'\(.*?\)', '', value)
    value = re.sub(r'\[.*?\]', '', value)
    value = re.sub(r'\s+[^\s]*<!--[^>]*-->', '', value)
    value = re.sub('http[s]?://\S+', '', value)
    value = re.sub('\[', '', value)
    value = re.sub('\]', '', value)
    return value.strip()


def get_covid_values_sum(data):
    """
    Calculate sum of COVID-19 statistics
    :param data: dict with the following fields:
        'confirmed', 'deaths', 'recovered'
    :return: sum of statistics
    """
    values_sum = 0
    for name in STAT_NAMES:
        if name not in data:
            raise ValueError(f'Required "{name}" fields is not provided')
        if (data[name] is not None) and not np.isnan(data[name]):
            values_sum += data[name]
    return values_sum


def na2zero(value):
    """
    Convert None to 0
    :param value: value to convert
    :return: int value
    """
    return value if value else 0


def get_active(confirmed, deaths, recovered):
    """
    Calculate number of active cases
    :param confirmed: number confirmed cases
    :param deaths: number of deaths
    :param recovered: number of recovered patients
    :return:
    """
    return na2zero(confirmed) - na2zero(deaths) - na2zero(recovered)
