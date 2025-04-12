from flask import Blueprint, jsonify

index_router = Blueprint("index", __name__)


@index_router.route("/", methods=["GET"])
def index():
    """Index route."""
    return jsonify({"message": "Welcome to RevoBank!"}), 200


@index_router.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for deployment monitoring."""
    return jsonify({"status": "healthy"}), 200
