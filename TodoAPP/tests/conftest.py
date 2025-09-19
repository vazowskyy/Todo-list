import os
import pytest
from datetime import datetime
from werkzeug.security import generate_password_hash

from website import create_app, db
from website.models import User, Task


# --------
# Fixtures
# --------

@pytest.fixture(scope='module')
def new_user():
    user = User(email='patkennedy79@gmail.com', name="FlaskUser",
                password=generate_password_hash('FlaskIsAwesome!'), )
    return user


@pytest.fixture(scope='module')
def test_client():
    # Set the Testing configuration prior to creating the Flask application
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    default_user = User(email='patkennedy79@gmail.com',
                        password=generate_password_hash('FlaskIsAwesome'))
    second_user = User(email='patrick@yahoo.com',
                       password=generate_password_hash('FlaskIsTheBest987'))
    db.session.add(default_user)
    db.session.add(second_user)

    # Commit the changes for the users
    db.session.commit()

    # Insert book data
    task1 = Task(name='Malibu Rising', text='Taylor Jenkins Reid', date=datetime.now(
    ), user=default_user.id, completed=False, category="Music")
    task2 = Task(name='Flask', text='Web APP', date=datetime.now(),
                 user=second_user.id, completed=True, category="IT")

    db.session.add(task1)
    db.session.add(task2)

    # Commit the changes for the books
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()
