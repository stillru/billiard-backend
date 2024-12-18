import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import TestConfig
from app import create_app
from extensions import db


@pytest.fixture(scope="session")
def app():
    """Create a Flask application instance for testing."""
    app = create_app(TestConfig)
    with app.app_context():
        # Create the database tables
        db.create_all()
        yield app
        # Cleanup after tests
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """A test client for the app."""
    return app.test_client()
