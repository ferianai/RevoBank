from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User
from functools import wraps
from flask import jsonify


def generate_token(user_id):
    """Generate JWT token for authenticated user using flask-jwt-extended"""
    return create_access_token(
        identity=str(user_id)
    )  # pastikan id disimpan sebagai string


def token_required(f):
    """Decorator to verify JWT token and inject current_user"""

    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        try:
            user = User.query.get(int(user_id))
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid user ID in token"}), 400

        if not user:
            return jsonify({"error": "User not found"}), 404

        return f(user, *args, **kwargs)

    return decorated_function


def get_current_user():
    """(Optional) Manually get current authenticated user"""
    user_id = get_jwt_identity()
    return User.query.get(int(user_id))  # convert ke int juga di sini
