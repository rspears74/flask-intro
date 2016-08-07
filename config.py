import os

# default config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = '\x97\x0c\x9e\xaa\xea\x99\xeeN_\xeaK\xdeV\xf8\x1b!?\x08\xa1\xe0\xca`%\xe2'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
