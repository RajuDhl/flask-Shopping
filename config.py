import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '8c467f6f48494c0639964a56b9e6fe4c0f7a0966'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://repouser@sda-dev:grandCanyon2021#@sda-dev.postgres.database.azure.com
    # /repolog'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    USER_APP_NAME = 'Same Day Auto'
    USER_ENABLE_EMAIL = False
    USER_ENABLE_USERNAME = False
    USER_REQUIRE_RETYPE_PASSWORD = False
    USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL = True
    # SQLALCHEMY_DATABASE_URI = 'postgresql://repouser:s3cret@localhost/repolog'
    EMAIL_API = os.environ.get("SENDGRID_API_KEY")
    SAME_DAY_DOMAIN = os.environ.get("SAME_DAY_DOMAIN")


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
