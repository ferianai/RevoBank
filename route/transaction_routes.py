from flask import Blueprint, request, jsonify
from utils.auth import token_required
from repo.transaction import create_transaction
from models.transaction import TransactionType
from models.account import Account
from instance.database import db
import traceback

transaction_bp = Blueprint("transaction_routes", __name__)


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

    if transaction_type.upper() == "TRANSFER":
        if not from_account_id or not to_account_id:
            return jsonify({"error": "Missing required fields for transfer"}), 400
    elif transaction_type.upper() == "DEPOSIT":
        if not to_account_id:
            return jsonify({"error": "Missing required fields for deposit"}), 400
    elif transaction_type.upper() == "WITHDRAWAL":
        if not from_account_id:
            return jsonify({"error": "Missing required fields for withdrawal"}), 400
    else:
        return jsonify({"error": "Invalid transaction type"}), 400

    try:
        transaction_type = TransactionType(transaction_type.upper())
    except ValueError:
        return jsonify({"error": "Invalid transaction type"}), 400

    # Verify accounts exist
    from_account = (
        Account.query.filter_by(id=from_account_id).first() if from_account_id else None
    )
    to_account = (
        Account.query.filter_by(id=to_account_id).first() if to_account_id else None
    )

    # Validate source account for withdrawals/transfers
    if from_account_id and not from_account:
        return jsonify({"error": "Source account not found"}), 404
    if from_account and from_account.user_id != current_user.id:
        return jsonify({"error": "Unauthorized access to source account"}), 403

    # Validate destination account for deposits/transfers
    if to_account_id and not to_account:
        return jsonify({"error": "Destination account not found"}), 404

    # Validate sufficient balance
    if from_account and float(from_account.balance) < float(amount):
        return jsonify({"error": "Insufficient funds"}), 400

    try:
        # Update account balances
        if from_account:
            from_account.balance = float(from_account.balance) - float(amount)
        if to_account:
            to_account.balance = float(to_account.balance) + float(amount)

        # Determine which account to use based on transaction type
        account_id = (
            to_account_id if transaction_type.value == "DEPOSIT" else from_account_id
        )

        # Create transaction with repository-compatible parameters
        success, message, transaction = create_transaction(
            account_number=account_id,
            amount=amount,
            transaction_type=transaction_type.value.lower(),
            user_id=current_user.id,
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
                        "account_id": transaction.account_id,
                        "amount": float(transaction.amount),
                        "type": transaction.type,
                        "date": transaction.date.isoformat(),
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
            "input_data": {
                "from_account_id": from_account_id,
                "to_account_id": to_account_id,
                "amount": amount,
                "type": transaction_type,
            },
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
