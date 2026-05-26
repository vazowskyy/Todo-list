from flask import Flask
from flask_login import LoginManager, user_logged_in
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from os import environ, path
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
from flask_mailman import Mail
from flask_migrate import Migrate
import sqlalchemy as sa
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
import logging


# load enviroment variables
load_dotenv()

db = SQLAlchemy()
csrf = CSRFProtect()
mail = Mail()
migrate = Migrate()
login_manager = LoginManager()

DOMAIN_NAME = environ.get("DOMAIN_NAME")


def create_app():
    app = Flask(__name__)

    if environ.get("FLASK_ENV") == "production":
        config_class = os.getenv(
            'CONFIG_TYPE', default='TodoAPP.config.ProductionConfig')
    else:
        config_class = os.getenv(
            'CONFIG_TYPE', default='TodoAPP.config.DevelopmentConfig')

    app.config.from_object(config_class)
    app.logger.info(f"Currently using {app.config['SQLALCHEMY_DATABASE_URI']}")
    initialize_extensions(app)
    register_blueprint(app)
    # configure_logging(app)

    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)
    if not inspector.has_table("user"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')
    else:
        app.logger.info('Database already contains the user table.')

    return app


def initialize_extensions(app):
    # Since the application instance is created, bind each extension instance to Flask app
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Flask Login
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


def register_blueprint(app):
    # Since flask app instance is created, register blueprints to Flask app
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    from .metrics import metrics_bp
    app.register_blueprint(metrics_bp, url_prefix='/metrics')

    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
