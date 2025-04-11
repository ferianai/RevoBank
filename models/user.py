from instance.database import db
from datetime import datetime
from shared import crono


class User(db.Model):
    """User model for storing user information."""

    __tablename__ = "users"

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    password: str = db.Column(
        db.String(256), nullable=False
    )  # Increased for hashed passwords
    created_at: datetime = db.Column(db.DateTime, default=crono.now)
    updated_at: datetime = db.Column(db.DateTime, default=crono.now, onupdate=crono.now)
    last_login: datetime = db.Column(db.DateTime, default=crono.now)
    is_active: bool = db.Column(db.Boolean)
    is_admin: bool = db.Column(db.Boolean)

    # Relationship with Account model
    accounts = db.relationship("Account", backref="user", lazy=True)

    def __repr__(self):
        return f">>> User: {self.username} - email: {self.email}"
