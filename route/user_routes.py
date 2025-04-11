from flask import Blueprint, jsonify, request
from models.user import User
from instance.database import db
from shared import crono
from werkzeug.security import generate_password_hash
from pydantic import BaseModel, ValidationError
from repo.user import create_user


class UserRegisterSchema(BaseModel):
    username: str
    email: str
    password: str


user_bp = Blueprint("user_routes", __name__, url_prefix="/users")


@user_bp.route("", methods=["POST"])
def register_user():
    """Register a new user."""

    data = request.json
    try:
        user = UserRegisterSchema.model_validate(data)
    except ValidationError as e:
        return (
            jsonify(
                {
                    "success": False,
                    "data": e.errors(include_url=False, include_context=False),
                }
            ),
            400,
        )
    hashed_password = generate_password_hash(user.password)
    created_user = create_user(user.username, user.email, hashed_password)

    return (
        jsonify(
            {
                "data": {
                    "id": created_user.id,
                    "username": created_user.username,
                    "email": created_user.email,
                },
                "success": True,
            }
        ),
        201,
    )


"""
@user_bp.route("", methods=["POST"])
def register_user():
    # Register a new user.
    data = request.get_json()
    if "username" not in data or "password" not in data or "email" not in data:
        return jsonify({"error": "Username, email and password are required!"}), 400

    # Check if user already exists
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    # Create new user
    new_user = User(
        username=data["username"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        is_active=True,
        is_admin=False,
    )
    db.session.add(new_user)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "User registered successfully!",
                "user": {
                    "id": new_user.id,
                    "username": new_user.username,
                    "email": new_user.email,
                },
            }
        ),
        201,
    )


@user_bp.route("/me", methods=["GET"])
def get_current_user():
    # Retrieve the profile of the currently logged-in user.
    # In a real implementation, this would get user from session/token
    # For demo, we'll get the first user
    user = User.query.first()
    if not user:
        return jsonify({"error": "No users found"}), 404

    return (
        jsonify(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at.isoformat(),
                "last_login": user.last_login.isoformat(),
            }
        ),
        200,
    )


@user_bp.route("/me", methods=["PUT"])
def update_current_user():
    # Update the profile information of the currently logged-in user.
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided for update"}), 400

    # In a real implementation, this would get user from session/token
    # For demo, we'll get the first user
    user = User.query.first()
    if not user:
        return jsonify({"error": "No users found"}), 404

    # Update allowed fields
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password = generate_password_hash(data["password"])

    user.updated_at = crono.now()
    db.session.commit()

    return (
        jsonify(
            {
                "message": "User profile updated successfully",
                "user": {"id": user.id, "username": user.username, "email": user.email},
            }
        ),
        200,
    )
"""
