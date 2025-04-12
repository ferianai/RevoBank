import logging
from config.config_loader import get_config
from config.settings import create_app
from instance.database import db  # noqa: F401

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app(get_config())

# Verify database connection
try:
    with app.app_context():
        db.engine.connect()
    logger.info("Database connection successful")
except Exception as e:
    logger.error(f"Database connection failed: {str(e)}")
    raise

logger.info("Application started successfully.")
