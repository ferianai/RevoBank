# DB_HOST = "localhost"
# DB_PORT = "revobank_db"

# SQLALCHEMY_DATABASE_URI = "sqlite:///local.db"
SQLALCHEMY_DATABASE_URI = (
    "postgresql://RevoBank_user:RevoPass123@localhost:5000/RevoBank_db"
)

# JWT Configuration
JWT_SECRET_KEY = "your-secret-key-here"  # Replace with a strong secret key
JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour in seconds
