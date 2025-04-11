from flask import Flask

import models  # noqa: F401
from instance.database import init_db
from route.index import index_router
from route.account_routes import account_bp
from route.user_routes import user_bp


def create_app(config_module="config.local"):
    app = Flask(__name__)

    # Load configuration from environment variables or a config file
    app.config.from_object(config_module)
    init_db(app)
    app.register_blueprint(index_router)
    app.register_blueprint(account_bp)
    app.register_blueprint(user_bp)

    return app
