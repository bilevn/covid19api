import os

LOGGER_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ['COVID19API_DB_URI']
