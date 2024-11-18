import logging


class Config(object):
    """
    Base configuration class
    """

    LOGGER_NAME = "default_logger"
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False
    PORT = 5000
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = "[BACKEND] %(asctime)s - %(name)s - %(levelname)s - %(message)s"
    SECRET_KEY = "just_play"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///production.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_TITLE = "Billjard backend API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    @classmethod
    def configure_logging(cls):
        logging.getLogger(cls.LOGGER_NAME)
        logging.basicConfig(level=cls.LOG_LEVEL, format=cls.LOG_FORMAT)


class TestConfig(Config):
    """
    Test configuration
    """

    LOGGER_NAME = "test_logger"
    TESTING = True
    LOG_LEVEL = logging.DEBUG
    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    LOG_FORMAT = "[BACKEND - Test] %(asctime)s - %(name)s - %(levelname)s - %(message)s"


class ProductionConfig(Config):
    """
    Production configuration
    """

    LOGGER_NAME = "prod_logger"
    FLASK_ENV = "production"
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "[BACKEND - Prod] %(asctime)s - %(name)s - %(levelname)s - %(message)s"
    SQLALCHEMY_DATABASE_URI = "sqlite:///production.db"


class DevelopmentConfig(Config):
    """
    Development configuration
    """

    DEBUG = True
