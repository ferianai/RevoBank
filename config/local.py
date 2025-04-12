# DB_HOST = "localhost"
# DB_PORT = "revobank_db"

# SQLALCHEMY_DATABASE_URI = "sqlite:///local.db"
# SQLALCHEMY_DATABASE_URI = (
#     "postgresql://RevoBank_user:RevoPass123@localhost:5000/RevoBank_db"
# )

DB_PASSWORD = "HqldfLPnON9ZePpZ"
DB_USERNAME = "postgres.qbtzphhjikelvgeojvne"
DB_HOST = "aws-0-us-east-1.pooler.supabase.com"
DB_PORT = 5432
DB_NAME = "postgres"
# postgresql://postgres.qbtzphhjikelvgeojvne:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:5432/postgres
# SQLALCHEMY_DATABASE_URI = (
#     f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # "postgresql://RevoBank_user:RevoPass123@localhost:5000/RevoBank_db"
# JWT Configuration

JWT_SECRET_KEY = "your-secret-key-here"  # Replace with a strong secret key
JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour in seconds
