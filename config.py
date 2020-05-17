import os


class Config(object):
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
    SECRET_KEY = '8CG>d223f[|3Zm6^JW!%dATcS<(dcvXf'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'wisma'
    MYSQL_PASSWORD = '12345678'
    MYSQL_DB = 'wisma'
    SQLALCHEMY_DATABASE_URI = 'mysql://' + MYSQL_USER + ':' + MYSQL_PASSWORD + '@'+ MYSQL_HOST + '/' + MYSQL_DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BUILD_ENV = ['development', 'production']
    FLASK_ENV = BUILD_ENV[0]
    if FLASK_ENV == BUILD_ENV[0]:
        DEBUG = True
    else:
        DEBUG = False
