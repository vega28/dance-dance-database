import pytest
import os
from api.api import app, db


@pytest.fixture
def client():
    """Create a test client with a PostgreSQL test database."""
    # Use PostgreSQL test database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URI')
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def app_context():
    """Create an app context for testing."""
    app.config['TESTING'] = True
    with app.app_context():
        yield app
