from models.user import User
from shared.crono import now
from config.settings import create_app
from instance.database import db

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
user_fixtures = [
    {
        "username": "john_doe",
        "email": "john@mail.com",
        "password": "johnpassword123",
        "is_active": True,
        "is_admin": False,
        "last_login": now(),
    },
    {
        "username": "jane_smith",
        "email": "jane@mail.com",
        "password": "janepassword123",
        "is_active": True,
        "is_admin": True,
        "last_login": now(),
    },
    {
        "username": "bob_johnson",
        "email": "bob@mail.com",
        "password": "bobpassword123",
        "is_active": True,
        "is_admin": False,
        "last_login": now(),
    },
    {
        "username": "alice_wonder",
        "email": "alice@mail.com",
        "password": "alicepassword123",
        "is_active": False,
        "is_admin": False,
        "last_login": now(),
    },
    {
        "username": "admin_user",
        "email": "admin@example.com",
        "password": "adminpassword123",
        "is_active": True,
        "is_admin": True,
        "last_login": now(),
    },
]

# Inisialisasi aplikasi dan faker
app = create_app("config.local")


def create_dummy_users():
    with app.app_context():
        """Create user fixtures in the database."""
        for user_data in user_fixtures:
            user = User(**user_data)
            db.session.add(user)
        db.session.commit()
        print("INSERTED DUMMY USERS")
