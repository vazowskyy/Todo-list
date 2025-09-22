from website.models import User, Task
from werkzeug.security import generate_password_hash

def test_new_user_logic():
    """
    GIVEN a User model 
    WHEN a new User is created
    THEN check the email, name and password are defined correctly
    """
    user = User(email="test@gmail.com", name="test", password=generate_password_hash("Test1234!"))
    assert user.email == "test@gmail.com"
    assert user.name == "test"
    assert user.check_password("Test1234!") == True

def test_new_task():
    """
    Given a Task model
    WHEN as new Task is created 
    THEN check name, text, date, user, completed and category are defined correctly
    """
    task = Task(
        name="My Task",
        text="Some description",
        user=1,
        category="Work"
    )
    assert task.name == "My Task"
    assert task.text == "Some description"
    assert task.user == 1
    assert task.category == "Work"

def test_users_exists(init_database):
    """
    GIVEN all Users in database
    WHEN db is queried
    THEN check if users in database exists 
    """
    users = User.query.all()
    assert len(users) == 2 
    assert users[0].email == "patkennedy79@gmail.com"
    assert users[1].email == "patrick@yahoo.com"

def test_task_exist(init_database):
    """
    GIVEN all Tasks in database
    WHEN db is queried
    THEN check if tasks in database exists 
    """
    tasks = Task.query.all()
    assert len(tasks) == 2
    task_names = [task.name for task in tasks]
    assert "Malibu Rising" in task_names
    assert "Flask" in task_names