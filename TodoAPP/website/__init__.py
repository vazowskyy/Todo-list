from flask import Flask
from flask_login import LoginManager, user_logged_in
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from os import environ, path
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
from flask_mailman import Mail

# load enviroment variables
load_dotenv()

DB_NAME = environ.get("DB_NAME")
RESET_PASS_TOKEN_MAX_AGE = int(environ.get(
    "RESET_PASS_TOKEN_MAX_AGE") or (15 * 60))
MAIL_SERVER = environ.get("MAIL_SERVER")
MAIL_PORT = int(environ.get("MAIL_PORT") or 25)
MAIL_USERNAME = environ.get("MAIL_USERNAME")
MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
DOMAIN_NAME = environ.get("DOMAIN_NAME")

db = SQLAlchemy()
csrf = CSRFProtect()
mail = Mail()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = environ.get("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = MAIL_PORT
    app.config['MAIL_USE_SSL'] = True if MAIL_PORT == 465 else False
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
    app.config['MAIL_DEFAULT_SENDER'] = MAIL_USERNAME
    app.config['RESET_PASS_TOKEN_MAX_AGE'] = RESET_PASS_TOKEN_MAX_AGE

    csrf.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
