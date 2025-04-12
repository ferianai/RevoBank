import os


def get_config():
    """Return the config module path based on FLASK_ENV env variable."""
    env = os.getenv("FLASK_ENV", "local").lower()

    if env == "local":
        return "config.local"
    elif env == "dev":
        return "config.dev"
    elif env == "testing":
        return "config.testing"
    elif env in ("remote", "production"):
        return "config.remote"
    else:
        return "config.local"
