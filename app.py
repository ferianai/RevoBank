from config.config_loader import get_config
from config.settings import create_app
from instance.database import db  # noqa: F401

app = create_app(get_config())
