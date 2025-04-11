from flask import Blueprint, jsonify, request
from models.user import User
from instance.database import db
from shared import crono
from werkzeug.security import generate_password_hash, check_password_hash
from pydantic import BaseModel, ValidationError
from repo.user import create_user
from utils.auth import generate_token, token_required
from flask_jwt_extended import create_access_token, create_refresh_token


class UserRegisterSchema(BaseModel):
    username: str
    email: str
    password: str


user_bp = Blueprint("user_routes", __name__, url_prefix="/users")


@user_bp.route("", methods=["POST"])
def register_user():
    """Register a new user using Pydantic and repo."""
    data = request.json

    try:
        user = UserRegisterSchema.model_validate(data)
    except ValidationError as e:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Validation error",
                    "details": e.errors(
                        include_url=False, include_context=False, include_input=False
                    ),
                }
            ),
            400,
        )

    # Check if user already exists
    if User.query.filter_by(username=user.username).first():
        return jsonify({"success": False, "error": "Username already exists"}), 400

    if User.query.filter_by(email=user.email).first():
        return jsonify({"success": False, "error": "Email already exists"}), 400

    # Save the user to the database
    hashed_password = generate_password_hash(user.password)
    created_user = create_user(user.username, user.email, hashed_password)

    return (
        jsonify(
            {
                "success": True,
                "data": {
                    "id": created_user.id,
                    "username": created_user.username,
                    "email": created_user.email,
                },
            }
        ),
        201,
    )


@user_bp.route("/login", methods=["POST"])
def login_user():
    """Authenticate user and return JWT token."""
    data = request.json
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password required"}), 400

    user = User.query.filter_by(username=data["username"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    # ✅ Convert user.id to str
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return (
        jsonify(
            {
                "success": True,
                "data": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
            }
        ),
        200,
    )


@user_bp.route("/me", methods=["GET"])
@token_required
def get_profile(current_user):
    """Get current user profile"""
    user = User.query.get(current_user.id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at.isoformat(),
        }
    )


@user_bp.route("/me", methods=["PUT"])
@token_required
def update_profile(current_user):
    """Update current user profile"""
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    user = User.query.get(current_user.id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password = generate_password_hash(data["password"])

    user.updated_at = crono.now()
    db.session.commit()

    return jsonify(
        {
            "message": "Profile updated successfully",
            "user": {"id": user.id, "username": user.username, "email": user.email},
        }
    )
