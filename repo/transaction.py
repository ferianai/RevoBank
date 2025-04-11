from models.transaction import Transaction, TransactionType
from models.account import Account
from instance.database import db
from shared import crono


def create_transaction(
    from_account_id, to_account_id, amount, transaction_type, user_id
):
    """
    Create a transaction (deposit, withdraw, transfer) and update balances.
    Returns: (success: bool, message: str, transaction: Transaction)
    """
    from_account = None
    to_account = None

    # Validate accounts
    if from_account_id:
        from_account = Account.query.filter_by(
            id=from_account_id, user_id=user_id
        ).first()
        if not from_account:
            return False, "Invalid or unauthorized source account", None

    if to_account_id:
        to_account = Account.query.filter_by(id=to_account_id).first()
        if not to_account:
            return False, "Destination account not found", None

    # Validate balance
    if transaction_type in [
        TransactionType.WITHDRAW.value,
        TransactionType.TRANSFER.value,
    ]:
        if not from_account or from_account.balance < amount:
            return False, "Insufficient balance", None

    # Update balances
    if transaction_type == TransactionType.DEPOSIT.value:
        to_account.balance += amount
    elif transaction_type == TransactionType.WITHDRAW.value:
        from_account.balance -= amount
    elif transaction_type == TransactionType.TRANSFER.value:
        from_account.balance -= amount
        to_account.balance += amount

    # Create transaction
    transaction = Transaction(
        from_account_id=from_account_id,
        to_account_id=to_account_id,
        amount=amount,
        type=transaction_type,
        created_at=crono.now(),
    )

    db.session.add(transaction)
    return True, "Transaction successful", transaction
