# RevoBANK [API Documentation](https://gx4h8ezxcv.apidog.io/)

## Database Schema Overview

### Entity Relationship Diagram

```mermaid
erDiagram
    USERS {
        INT id PK "Unique identifier"
        VARCHAR username "Username for login"
        VARCHAR email "User's email address"
        VARCHAR password_hash "Securely hashed user password"
        DATETIME created_at "Timestamp of user creation"
        DATETIME updated_at "Timestamp of user information update"
    }

    ACCOUNTS {
        INT id PK "Unique identifier"
        INT user_id FK "User associated with the account"
        VARCHAR account_type "Type of account"
        VARCHAR account_number "Unique account number"
        DECIMAL balance "Current balance of the account"
        TEXT image_uri "Profile picture URI"
        VARCHAR name "Account holder's name"
        DATE birth_date "Account holder's date of birth"
        VARCHAR address "Account holder's address"
        VARCHAR gender "Account holder's gender"
        VARCHAR phone "Account holder's phone number"
        DATETIME created_at "Timestamp of account creation"
        DATETIME updated_at "Timestamp of account information update"
    }

    TRANSACTIONS {
        INT id PK "Unique identifier"
        INT from_account_id FK "Account initiating the transaction"
        INT to_account_id FK "Account receiving the transaction"
        DECIMAL amount "Transaction amount"
        ENUM type "Type of transaction (deposit, withdrawal, transfer)"
        VARCHAR description "Optional description of the transaction"
        DATETIME created_at "Timestamp of transaction creation"
    }

    TRANSACTIONS_HISTORY {
        INT id PK "Unique identifier for the history entry"
        INT transaction_id FK "Transaction related to this history entry"
        VARCHAR status "Status of the transaction (e.g., completed, failed)"
        DATETIME status_timestamp "Timestamp when the transaction status was recorded"
        TEXT notes "Additional notes regarding the transaction status"
    }

    USERS ||--o{ ACCOUNTS : has
    ACCOUNTS ||--o{ TRANSACTIONS : owns
    TRANSACTIONS ||--o{ TRANSACTIONS_HISTORY : logs
```

### Database Connection Configuration

The application supports multiple database backends:

1. **SQLite (for testing):**

   ```python
   # config/testing.py
   SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
   ```

2. **PostgreSQL (for development/production):**
   ```python
   # config/dev.py or config/prod.py
   SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost:5432/revobank'
   ```

Environment variables should be set in `.env` file:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=revobank
DB_USER=user
DB_PASSWORD=password
```

### Example Database Operations

**1. Creating a User:**

```python
from models.user import User
from instance.database import db

new_user = User(
    username='john_doe',
    email='john@example.com',
    password_hash='hashed_password'
)
db.session.add(new_user)
db.session.commit()
```

**2. Managing Accounts:**

```python
from models.account import Account

# Create account
account = Account(
    user_id=1,
    account_type='savings',
    account_number='1234567890',
    balance=1000.00
)
db.session.add(account)
db.session.commit()

# Update balance
account = Account.query.get(1)
account.balance += 500.00
db.session.commit()
```

**3. Initiating Transactions:**

```python
from models.transaction import Transaction

# Transfer between accounts
transaction = Transaction(
    from_account_id=1,
    to_account_id=2,
    amount=100.00,
    type='transfer',
    description='Monthly savings'
)
db.session.add(transaction)
db.session.commit()
```

### API Documentation

Full API documentation is available at: [RevoBANK API Docs](https://gx4h8ezxcv.apidog.io/)

## Installation

```bash
    # Install the required packages
    uv init
    mv main.py app.py
    uv add flask
    uv add pytest
    uv run pytest -s -v     # run test
```

- for testing : sqlite

```bash
    uv add flask-sqlalchemy flask-migrate psycopg2-binary
    uv add pydantic # for pydantic validation in models
```

- for local, production, development : postgresql
- model manager / table manager / ORM / migration : alembic / [lask-migrate](https://flask-migrate.readthedocs.io/en/latest/#)

create a migration/update repository with the following command:

```bash
    $ uv run flask db init # create the migration repository
    $ uv run flask db migrate -m "Initial migration" # create the first migration
    $ uv run flask db upgrade # apply the migration
    $ uv run flask db downgrade # revert the migration
    $ uv run flask db --help # list available commands
    $ uv run load_fixture.py # load dummy data
    $ rm -rf migrations # remove the migration repository
```

```bash
    docker compose up -d   # run docker
```

### **Run the application:**

```bash
    uv run task fr # update toml : [tool.taskipy.tasks] fr = "flask --app main run --port 5000 --reload --debug"
```

### **API will be available at:**

```
http://127.0.0.1:5000
```

- implement .env variables in a .env file
- konsep rollback and commit
- implement pagination
- Optimize Queries: Avoid N+1 queries, use eager loading in SQLAlchemy.
- catat history perbankan (mutasi rekening)
