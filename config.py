import os

# default config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = '\x97\x0c\x9e\xaa\xea\x99\xeeN_\xeaK\xdeV\xf8\x1b!?\x08\xa1\xe0\xca`%\xe2'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
