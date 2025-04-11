from instance.database import db
from datetime import datetime
from shared import crono


class TransactionHistory(db.Model):
    __tablename__ = "transactions_history"

    id: int = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(
        db.Integer, db.ForeignKey("transactions.id"), nullable=False
    )
    status: str = db.Column(db.String(50), nullable=False)
    status_timestamp: datetime = db.Column(db.DateTime, default=crono.now)
    notes: str = db.Column(db.Text)

    def __repr__(self):
        return f"<TransactionHistory {self.transaction_id} - {self.status}>"
