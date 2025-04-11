import pytest
from config.settings import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app("config.testing")
    # Additional setup can be done here if needed
    yield app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()
