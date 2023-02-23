import os
from decouple import config

# basedir = os.path.abspath(os.path.dirname(__file__))

# Load configuration parameters from .env file
DB_HOST = config('DB_HOST', default='localhost:5432')
DB_USER = config('DB_USER', default='')
DB_PASSWORD = config('DB_PASSWORD', default='')
DB_NAME = config('DB_NAME')
TEST_DB_NAME = config('TEST_DB_NAME')

db_uri = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
test_db_uri = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{TEST_DB_NAME}'


class DevelopmentConfig:
    SECRET_KEY = os.urandom(32)
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(DevelopmentConfig):
    DEVELOPMENT = False
    DEBUG = False


class UnittestConfig(DevelopmentConfig):
    SQLALCHEMY_DATABASE_URI = test_db_uri
