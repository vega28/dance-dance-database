import pytest
import os
from api.seed import seed
from api.api import create_app, db as _db

def _test_config():
    db_uri = os.getenv('TEST_DATABASE_URI')
    if not db_uri:
        raise RuntimeError(
            "TEST_DATABASE_URI environment variable is not set. "
            "Please set it to a valid PostgreSQL test database URI before running tests."
        )
    return {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": db_uri,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }

def _migrate_and_seed_db():
    from flask_migrate import upgrade
    upgrade()
    seed()
    return 

@pytest.fixture()
def client(app):
    """Create a test client."""
    with app.app_context():
        yield app.test_client()

@pytest.fixture(autouse=True)
def app():
    """Create a Flask app configured for testing."""

    app = create_app(app_config=_test_config())

    with app.app_context():
        _db.create_all()
        _migrate_and_seed_db()

        yield app

        _db.session.remove()
        _db.drop_all()

@pytest.fixture(scope="session")
def db_session():
    """Provide a SQLAlchemy database session for tests."""
    return _db.session
    
@pytest.fixture(scope="session")
def models():
    """Import model modules so they are registered with SQLAlchemy."""
    from api import models as _models
    return _models