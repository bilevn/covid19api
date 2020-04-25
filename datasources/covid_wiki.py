# Coronavirus (COVID-19) data is provided by Wikipedia from the following pages:
# ref: https://en.wikipedia.org/wiki/2019%E2%80%9320_coronavirus_pandemic_by_country_and_territory
# ref: https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Russia
# ref: https://en.wikipedia.org/wiki/Timeline_of_the_2020_coronavirus_pandemic_in_the_United_States


import pandas as pd
from datasources import utils


def check_report(df):
    """
    Each report should contain the following columns:
    - country:   country name
    - state:     state name if reporting regional stats and None otherwise
    - confirmed: number of confirmed cases
    - deaths:    number of deaths
    - recovered: number of recovered patients
    :param df:   pandas DataFrame to check
    """
    for field in ['country', 'state', 'confirmed', 'deaths', 'recovered']:
        if field not in df.columns:
            raise ValueError(f'Required report field "{field}" is not in the report')


def get_report_countries():
    """
    Get data from Wikipedia page with
    COVID-19 statistics for each country

    :return: Pandas DataFrame
    """
    url = 'https://en.wikipedia.org/wiki/2019%E2%80%9320_coronavirus_pandemic_by_country_and_territory'
    df = utils.get_wiki_table_df(url, 'Countries and territories')
    df = pd.DataFrame(df.values[:, 1:5], columns=['country', 'confirmed', 'deaths', 'recovered'])
    df = df[~df['country'].isna()]
    df['country'] = df['country'].apply(lambda x: utils.clean_territory_name(x))
    df.drop(df[df['country'].str.len() > 40].index, inplace=True)
    df = utils.wiki_table_df_numeric_column_clean(df, ['confirmed', 'deaths', 'recovered'])
    df['state'] = None
    check_report(df)
    return df


def get_report_us():
    """
    Get COVID-19 data from Wikipedia page with
    COVID-19 statistics for each state of USA

    :return: Pandas DataFrame
    """
    url = 'https://en.wikipedia.org/wiki/Timeline_of_the_2020_coronavirus_pandemic_in_the_United_States'
    df = utils.get_wiki_table_df(url, 'coronavirus pandemic in the United States by state and territory')
    df = pd.DataFrame(df.values[:, 1:5], columns=['state', 'confirmed', 'deaths', 'recovered'])
    df.drop(df[df['state'].str.len() > 40].index, inplace=True)
    df['state'] = df['state'].apply(lambda x: utils.clean_territory_name(x))
    df = utils.wiki_table_df_numeric_column_clean(df, ['confirmed', 'deaths', 'recovered'])
    df['country'] = 'United States'
    check_report(df)
    return df


def get_report_ru():
    """
    Get data from Wikipedia page with
    COVID-19 statistics for each state of Russia

    :return: Pandas DataFrame
    """
    url = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Russia'
    df = utils.get_wiki_table_df(url, 'coronavirus pandemic in Russia by federal subjects')
    df = pd.DataFrame(df.values[:, 1:5], columns=['state', 'confirmed', 'recovered', 'deaths'])
    df.drop(df[df['state'].str.len() > 40].index, inplace=True)
    df['state'] = df['state'].apply(lambda x: utils.clean_territory_name(x))
    df = utils.wiki_table_df_numeric_column_clean(df, ['confirmed', 'deaths', 'recovered'])
    df['country'] = 'Russia'
    check_report(df)
    return df
