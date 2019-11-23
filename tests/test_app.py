import pytest

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            pass
        yield client


def test_root_url(client):
    rv = client.get('/')
    assert b'Please select an option from the menu' in rv.data
