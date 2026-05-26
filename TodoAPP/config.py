import os
from os import environ
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler


# Determine the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv()
# print(environ.get('DATABASE_URL'))
# print(os.path.join(BASEDIR, "/website", "/.env"))


class Config(object):
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='BAD_SECRET_KEY')
    if os.getenv('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASEDIR, '../../instance', 'database.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESET_PASS_TOKEN_MAX_AGE = int(os.getenv(
        "RESET_PASS_TOKEN_MAX_AGE") or (15 * 60))
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT") or 25)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    DOMAIN_NAME = os.getenv("DOMAIN_NAME")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "false").lower() in ("true", "1")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() in ("true", "1")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME)


class ProductionConfig(Config):
    FLASK_ENV = 'production'

    @staticmethod
    def init_app(app):
        if app.config.get("LOG_WITH_GUNICORN"):
            gunicorn_logger = logging.getLogger("gunicorn.error")
            app.logger.handlers = gunicorn_logger.handlers
            app.logger.setLevel(gunicorn_logger.level)


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI',
    #                                    default=f"sqlite:///{os.path.join(BASEDIR, '../../instance', 'test.db')}")
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
