from instance.database import db
from datetime import datetime
from shared import crono
from enum import Enum


class TransactionType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    TRANSFER = "TRANSFER"


#     # Add other transaction types as needed


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    from_account_id = db.Column(
        db.Integer, db.ForeignKey("accounts.id"), nullable=False
    )
    to_account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.Enum(TransactionType))
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=crono.now)

    from_account = db.relationship(
        "Account", foreign_keys=[from_account_id], back_populates="transactions"
    )
    to_account = db.relationship(
        "Account", foreign_keys=[to_account_id], back_populates="to_transactions"
    )
    transaction_history = db.relationship(
        "TransactionHistory", backref="transaction", lazy=True
    )

    def __repr__(self):
        return f"<Transaction {self.id} - {self.type} - {self.amount}>"
