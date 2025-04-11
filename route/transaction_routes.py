from flask import Blueprint, request, jsonify
from utils.auth import token_required
from repo.transaction import create_transaction
from models.transaction import Transaction, TransactionType
from models.account import Account
from instance.database import db
import traceback
from datetime import datetime

transaction_bp = Blueprint("transaction_routes", __name__)


@transaction_bp.route("/transactions", methods=["GET"])
@token_required
def get_transactions(current_user):
    """Get all transactions for the current user with optional filters"""
    account_id = request.args.get("account_id")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    try:
        # Base query for user's transactions
        query = Transaction.query.join(
            Account,
            (Transaction.from_account_id == Account.id)
            | (Transaction.to_account_id == Account.id),
        ).filter(Account.user_id == current_user.id)

        # Apply filters
        if account_id:
            query = query.filter(
                (Transaction.from_account_id == account_id)
                | (Transaction.to_account_id == account_id)
            )
        if start_date:
            start = datetime.fromisoformat(start_date)
            query = query.filter(Transaction.created_at >= start)
        if end_date:
            end = datetime.fromisoformat(end_date)
            query = query.filter(Transaction.created_at <= end)

        transactions = query.order_by(Transaction.created_at.desc()).all()

        return (
            jsonify(
                [
                    {
                        "id": t.id,
                        "from_account_id": t.from_account_id,
                        "to_account_id": t.to_account_id,
                        "amount": float(t.amount),
                        "type": t.type.value,
                        "date": t.created_at.isoformat(),
                    }
                    for t in transactions
                ]
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify({"error": "Failed to retrieve transactions", "details": str(e)}),
            500,
        )


@transaction_bp.route("/transactions/<int:transaction_id>", methods=["GET"])
@token_required
def get_transaction(current_user, transaction_id):
    """Get a specific transaction by ID if it belongs to the user"""
    try:
        transaction = (
            Transaction.query.join(
                Account,
                (Transaction.from_account_id == Account.id)
                | (Transaction.to_account_id == Account.id),
            )
            .filter(
                Transaction.id == transaction_id, Account.user_id == current_user.id
            )
            .first()
        )

        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404

        return (
            jsonify(
                {
                    "id": transaction.id,
                    "from_account_id": transaction.from_account_id,
                    "to_account_id": transaction.to_account_id,
                    "amount": float(transaction.amount),
                    "type": transaction.type.value,
                    "date": transaction.created_at.isoformat(),
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify({"error": "Failed to retrieve transaction", "details": str(e)}),
            500,
        )


@transaction_bp.route("/transactions", methods=["POST"])
@token_required
def create_transaction_route(current_user):
    data = request.json
    from_account_id = data.get("from_account_id")
    to_account_id = data.get("to_account_id")
    amount = data.get("amount")
    transaction_type = data.get("type")

    # Validate required fields
    if not all([amount, transaction_type]):
        return jsonify({"error": "Missing required fields"}), 400

    # Properly initialize enum value
    try:
        transaction_type = TransactionType[transaction_type.upper()]
    except KeyError:
        return jsonify({"error": "Invalid transaction type"}), 400

    if transaction_type == TransactionType.TRANSFER:
        if not from_account_id or not to_account_id:
            return jsonify({"error": "Missing required fields for transfer"}), 400
    elif transaction_type == TransactionType.DEPOSIT:
        if not to_account_id:
            return jsonify({"error": "Missing required fields for deposit"}), 400
    elif transaction_type == TransactionType.WITHDRAW:
        if not from_account_id:
            return jsonify({"error": "Missing required fields for withdrawal"}), 400

    # Verify accounts exist
    from_account = (
        Account.query.filter_by(id=from_account_id).first() if from_account_id else None
    )
    to_account = (
        Account.query.filter_by(id=to_account_id).first() if to_account_id else None
    )

    # Validate source account
    if from_account_id and not from_account:
        return jsonify({"error": "Source account not found"}), 404
    if from_account and from_account.user_id != current_user.id:
        return jsonify({"error": "Unauthorized access to source account"}), 403

    # Validate destination account
    if to_account_id and not to_account:
        return jsonify({"error": "Destination account not found"}), 404

    # Validate balance
    if from_account and float(from_account.balance) < float(amount):
        return jsonify({"error": "Insufficient funds"}), 400

    try:
        # Update balances
        if from_account:
            from_account.balance = float(from_account.balance) - float(amount)
        if to_account:
            to_account.balance = float(to_account.balance) + float(amount)

        # Create transaction
        account_id = (
            to_account_id
            if transaction_type == TransactionType.DEPOSIT
            else from_account_id
        )
        success, message, transaction = create_transaction(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            transaction_type=transaction_type.value,
            user_id=current_user.id,
            amount=amount,
        )

        if not success:
            db.session.rollback()
            return jsonify({"error": message}), 400

        db.session.commit()

        return (
            jsonify(
                {
                    "message": message,
                    "transaction": {
                        "id": transaction.id,
                        "from_account_id": transaction.from_account_id,
                        "to_account_id": transaction.to_account_id,
                        "amount": float(transaction.amount),
                        "type": transaction.type.value,
                        "date": transaction.created_at.isoformat(),
                    },
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        error_details = {
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc(),
            "input_data": data,
        }
        print(f"Transaction Error: {error_details}")
        return (
            jsonify(
                {
                    "error": "Transaction processing failed",
                    "details": str(e),
                    "debug_id": "TX_ERROR_1001",
                }
            ),
            500,
        )
