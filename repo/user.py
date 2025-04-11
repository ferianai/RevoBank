from models.user import User
from instance.database import db
from werkzeug.security import generate_password_hash
from shared import crono


def create_user(username, email, password):
    """Create a new user instance."""
    new_user = User(
        username=username,
        email=email,
        password=password,  # Password is already hashed by route
        is_active=True,
        is_admin=False,
        created_at=crono.now(),
        updated_at=crono.now(),
        last_login=crono.now(),
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user

    """    ACCOUNTS {
        INT id PK "Unique identifier"
        INT user_id FK "User associated with the account"
        VARCHAR account_type "Type of account"
        VARCHAR account_number "Unique account number"
        DECIMAL balance "Current balance of the account"
        TEXT image_uri "Profile picture URI"
        VARCHAR name "Account holder's name"
        DATE birth_date "Account holder's date of birth"
        VARCHAR address "Account holder's address"
        VARCHAR gender "Account holder's gender"
        VARCHAR phone "Account holder's phone number"
        DATETIME created_at "Timestamp of account creation"
        DATETIME updated_at "Timestamp of account information update"
    }
    """
