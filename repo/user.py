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
