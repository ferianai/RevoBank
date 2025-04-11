import re
from flask import Blueprint, jsonify, request
from repo.account import create_user_account
from pydantic import BaseModel, ValidationError
from instance.database import db
from models.account import Account
from models.user import User
from shared import crono
from datetime import datetime
from utils.auth import token_required


class AccountRegisterSchema(BaseModel):
    user_id: int
    account_type: str
    account_number: str
    balance: float = 0.00
    image_uri: str = None
    name: str
    birth_date: str
    address: str
    gender: str
    phone: str


account_bp = Blueprint("account_routes", __name__, url_prefix="/accounts")


@account_bp.route("", methods=["POST"])
def create_account():
    """create account route."""
    try:
        account = AccountRegisterSchema.model_validate(request.json)
    except ValidationError as e:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Validation error",
                    "data": e.errors(
                        include_url=False, include_context=False, include_input=False
                    ),
                }
            ),
            400,
        )

    # Convert birth_date to a date object
    try:
        birth_date = datetime.strptime(account.birth_date, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid birth date format. Use YYYY-MM-DD"}), 400

    user = db.get_or_404(User, account.user_id)

    # ✅ Check if account number already exists
    existing_account = Account.query.filter_by(
        account_number=account.account_number
    ).first()
    if existing_account:
        return jsonify({"error": "Account with this number already exists"}), 400

    # ✅ Optional: Check if user already has same type account
    same_type_account = Account.query.filter_by(
        user_id=account.user_id, account_type=account.account_type
    ).first()
    if same_type_account:
        return (
            jsonify({"error": f"User already has a '{account.account_type}' account"}),
            400,
        )

    # ✅ Create new account
    user_account = create_user_account(
        user_id=account.user_id,
        account_type=account.account_type,
        account_number=account.account_number,
        balance=account.balance,
        name=account.name,
        birth_date=birth_date,
        address=account.address,
        gender=account.gender,
        phone=account.phone,
        image_uri=account.image_uri,
    )
    return jsonify({"message": "Account created successfully!"}), 201


@account_bp.route("", methods=["GET"])
def get_accounts():
    """Get all accounts."""
    accounts = Account.query.all()
    accounts_data = [
        {
            "id": account.id,
            "user_id": account.user_id,
            "account_number": account.account_number,
            "account_type": account.account_type,
            "balance": float(account.balance),
            "name": account.name,
            "created_at": account.created_at.isoformat(),
        }
        for account in accounts
    ]

    return jsonify({"success": True, "data": accounts_data}), 200


@account_bp.route("/<int:account_id>", methods=["PUT"])
@token_required
def update_account(current_user, account_id):
    """Update an existing account with comprehensive validation."""
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"success": False, "error": "Account not found"}), 404

    if account.user_id != current_user.id:
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400

    # Define updatable fields with validation rules
    updatable_fields = {
        "name": {"type": str, "max_length": 100},
        "address": {"type": str, "max_length": 200},
        "phone": {"type": str, "pattern": r"^\+?[\d\s-]{10,15}$"},
        "image_uri": {"type": str, "is_url": True},
    }

    errors = []
    updates = {}

    for field, rules in updatable_fields.items():
        if field in data:
            try:
                # Type validation
                if not isinstance(data[field], rules["type"]):
                    raise ValueError(f"{field} must be {rules['type'].__name__}")

                # Length validation
                if "max_length" in rules and len(data[field]) > rules["max_length"]:
                    raise ValueError(
                        f"{field} exceeds maximum length of {rules['max_length']}"
                    )

                # Pattern validation
                if "pattern" in rules and not re.match(rules["pattern"], data[field]):
                    raise ValueError(f"Invalid {field} format")

                # URL validation
                if "is_url" in rules and not data[field].startswith(
                    ("http://", "https://")
                ):
                    raise ValueError(f"{field} must be a valid URL")

                updates[field] = data[field]
            except ValueError as e:
                errors.append(str(e))

    if errors:
        return (
            jsonify(
                {"success": False, "error": "Validation errors", "details": errors}
            ),
            400,
        )

    # Apply updates
    for field, value in updates.items():
        setattr(account, field, value)

    account.updated_at = crono.utc_now()

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"success": False, "error": "Database error", "details": str(e)}),
            500,
        )

    # Return complete account data
    account_data = {
        "id": account.id,
        "user_id": account.user_id,
        "account_number": account.account_number,
        "account_type": account.account_type,
        "balance": float(account.balance),
        "name": account.name,
        "address": account.address,
        "phone": account.phone,
        "image_uri": account.image_uri,
        "created_at": account.created_at.isoformat(),
        "updated_at": account.updated_at.isoformat(),
    }

    return (
        jsonify(
            {
                "success": True,
                "message": "Account updated successfully",
                "data": account_data,
            }
        ),
        200,
    )


@account_bp.route("/<int:account_id>", methods=["DELETE"])
@token_required
def delete_account(current_user, account_id):
    """Delete an existing account."""
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"success": False, "error": "Account not found"}), 404

    if account.user_id != current_user.id:
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    db.session.delete(account)
    db.session.commit()

    return jsonify({"success": True, "message": "Account deleted successfully!"}), 200
