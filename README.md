### ERD RevoBANK

## USER

- `id` - `INT` - `PK` - `Unique identifier`
- `username` - `VARCHAR` - `Username for login`
- `email` - `VARCHAR` - `User's email address`
- `password_hash` - `VARCHAR` - `Securely hashed user password`
- `created_at` - `DATETIME` - `Timestamp of user creation`
- `updated_at` - `DATETIME` - `Timestamp of user information update`

## Schema RevoBANK

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

### Installation

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

- implement .env variables in a .env file
- konsep rollback and commit
- implement pagination
- Optimize Queries: Avoid N+1 queries, use eager loading in SQLAlchemy.
- catat history perbankan (mutasi rekening)
