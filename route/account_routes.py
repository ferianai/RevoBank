from flask import Blueprint, jsonify

account_bp = Blueprint("account_routes", __name__, url_prefix="/accounts")


@account_bp.route("", methods=["GET"])
def get_accounts():
    """get accounts route."""
    return jsonify({"message": "Welcome to RevoBank!"}), 200
