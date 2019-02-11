""" Development Configurations """
from datetime import timedelta

# SQL
SQLALCHEMY_DATABASE_URI = "mysql://:@:3306/"
SQLALCHEMY_TRACK_MODIFICATIONS = False
PREFERRED_URL_SCHEME = "https"

# Log
APP_LOG_FILE = 'log/app.log'
APP_LOG_LEVEL = 'DEBUG'

# JWT
JWT_SECRET_KEY = ''
JWT_TOKEN_LOCATION = 'cookies'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
JWT_COOKIE_SECURE = True
