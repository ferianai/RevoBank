from instance.database import db
from datetime import datetime
from shared import crono


class Account(db.Model):
    __tablename__ = "accounts"

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    account_type: str = db.Column(db.String(100), nullable=False)  # Increased length
    account_number: str = db.Column(
        db.String(40), unique=True, nullable=False
    )  # Increased length
    balance: float = db.Column(db.Numeric(10, 2), default=0.00)
    image_uri: str = db.Column(db.Text)
    name: str = db.Column(db.String(100), nullable=False)
    birth_date: datetime = db.Column(db.Date)
    address: str = db.Column(db.String(255))
    gender: str = db.Column(db.String(20))  # Increased length
    phone: str = db.Column(db.String(300))  # Increased length
    created_at: datetime = db.Column(db.DateTime, default=crono.now)
    updated_at: datetime = db.Column(db.DateTime, default=crono.now, onupdate=crono.now)

    transactions = db.relationship(
        "Transaction",
        back_populates="from_account",
        foreign_keys="Transaction.from_account_id",
        lazy=True,
    )
    to_transactions = db.relationship(
        "Transaction",
        foreign_keys="Transaction.to_account_id",
        back_populates="to_account",
        lazy=True,
    )

    def __repr__(self):
        return f"<Account {self.account_number}>"
