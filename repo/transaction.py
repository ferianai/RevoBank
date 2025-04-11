from models.transaction import Transaction
from models.account import Account
from instance.database import db
from shared import crono
from sqlalchemy import and_

def create_transaction(account_id, amount, transaction_type, user_id):
    """
    Create a new transaction and update account balance
    Returns: (success: bool, message: str, transaction: Transaction)
    """
    account = Account.query.filter_by(id=account_id, user_id=user_id).first()
    if not account:
        return False, "Invalid account", None

    if transaction_type == "withdraw" and account.balance < amount:
        return False, "Insufficient balance", None

    # Update account balance
    if transaction_type == "deposit":
        account.balance += amount
    elif transaction_type == "withdraw":
        account.balance -= amount

    # Create transaction record
    transaction = Transaction(
        account_id=account_id,
        amount=amount,
        type=transaction_type,
        date=crono.now()
    )

    db.session.add(transaction)
    db.session.commit()

    return True, "Transaction successful", transaction

def get_transactions(user_id, account_id=None, start_date=None, end_date=None):
    """
    Get transactions with optional filters
    Returns: List[Transaction]
    """
    query = Transaction.query.join(Account).filter(Account.user_id == user_id)

    if account_id:
        query = query.filter(Transaction.account_id == account_id)
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)

    return query.all()

def get_transaction_by_id(transaction_id, user_id):
    """
    Get a specific transaction by ID if it belongs to the user
    Returns: Transaction or None
    """
    return Transaction.query.join(Account)\
