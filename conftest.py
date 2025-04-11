import pytest
from config.settings import create_app
from models.user import User
from instance.database import db as _db


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app("config.testing")
    # Additional setup can be done here if needed

    with app.app_context():
        _db.create_all()  # Create tables

    yield app  # This is where the testing happens

    with app.app_context():
        _db.session.remove()
        _db.drop_all()
    # Clean up after tests


@pytest.fixture
def db(app):
    """Create a new database session for a test."""
    # Create the database and the database tables if they don't exist yet
    with app.app_context():
        yield _db


@pytest.fixture
def users(app):
    users = [
        {
            "username": "john",
            "email": "john@mail.com",
            "password": "johnpassword1",
            "id": 1,
        },
        {
            "username": "jane",
            "email": "jane@mail.com",
            "password": "janepassword1",
            "id": 2,
        },
        {
            "username": "bob",
            "email": "bob@mail.com",
            "password": "bobpassword1",
            "id": 3,
        },
    ]
    with app.app_context():
        """Create user fixtures in the database."""
        data_users = []
        for user_data in users:
            user = User(**user_data)
            data_users.append(user)  # __db.session.add(user)
        print("POPULATING TEST USERS")
        _db.session.add_all(data_users)
        _db.session.commit()
        print("INSERTED USER TO DB")
        return data_users


"""_summary
    USERS {
        INT id PK "Unique identifier"
        VARCHAR username "Username for login"
        VARCHAR email "User's email address"
        VARCHAR password_hash "Securely hashed user password"
        DATETIME created_at "Timestamp of user creation"
        DATETIME updated_at "Timestamp of user information update"
    }
"""


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()
