import pytest
from api.seed import seed
from api.api import create_app, db


@pytest.fixture
def client():
    """Create a test client with a PostgreSQL test database."""
    app = create_app(test=True)

    with app.app_context():
        db.create_all() # FIXME: this creates tables from Models, not migrations
        seed()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture
def app_context():
    """Provide a Flask app context for tests."""
    app = create_app(test=True)
    with app.app_context():
        db.create_all() # FIXME: this creates tables from Models, not migrations
        # TODO: Apply all migrations to the fresh test DB
        # from flask_migrate import upgrade
        # upgrade()
        seed()
        yield app
        db.session.remove()
        db.drop_all()