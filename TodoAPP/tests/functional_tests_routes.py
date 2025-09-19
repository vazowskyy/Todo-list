from website import create_app


def test_home_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested via GET 
    THEN check that response is valid 
    """
    response = test_client.get('/')
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "home" in html.lower()
    assert "register" in html.lower()
    assert "login" in html.lower()


def test_login_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested via GET 
    THEN check that response is valid 
    """
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b"Sign in to your account" in response.data
    assert b"Your email" in response.data
    assert b"Password" in response.data


def test_todo_list_not_logged_in(test_client):
    res = test_client.get('/todo_list')
    assert res.status_code == 302


def test_register_user(test_client):
    # register
    response = test_client.post('/register', data={
        'email': 'alice@example.com',
        'name': 'alice',
        'password': 'foo1234!',
        'password2': 'foo1234!',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data  # sprawdzamy, że strona login się wyświetla

    # login
    response = test_client.post('/login', data={
        'email': 'alice@example.com',
        'password': 'foo1234!',
    }, follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'tasks completed' in html.lower()
