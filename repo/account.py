from models.account import Account
from models.user import User
from werkzeug.security import generate_password_hash
from instance.database import db
from shared import crono
from datetime import datetime


def create_user_account(
    user_id,
    account_type,
    account_number,
    name,
    birth_date,
    address,
    gender,
    phone,
    balance=0.00,
    image_uri=None,
):
    """Create a new account instance."""
    new_account = Account(
        user_id=user_id,
        account_type=account_type,
        account_number=account_number,
        balance=float(balance),
        image_uri=image_uri,
        name=name,
        birth_date=birth_date,
        address=address,
        gender=gender,
        phone=str(phone),
        created_at=crono.now(),
        updated_at=crono.now(),
    )
    db.session.add(new_account)
    db.session.commit()
    return new_account
