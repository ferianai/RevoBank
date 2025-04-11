from flask import Flask

import models  # noqa: F401
from instance.database import init_db
from flask_jwt_extended import JWTManager
from route.index import index_router

from route.user_routes import user_bp
from route.account_routes import account_bp
from route.transaction_routes import transaction_bp

# Tambahkan global jwt
jwt = JWTManager()  # ✅ Tambahkan ini di luar create_app


def create_app(config_module="config.local"):
    app = Flask(__name__)

    # Load configuration from environment variables or a config file
    app.config.from_object(config_module)

    # Init database
    init_db(app)
    # ✅ Init JWT
    jwt.init_app(app)

    # Register routes
    app.register_blueprint(index_router)
    app.register_blueprint(user_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(transaction_bp)

    return app
