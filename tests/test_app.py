from models.user import User
from route.account_routes import AccountRegisterSchema


def test_index(client):
    """Test the index route."""
    response = client.get("/")
    assert response.status_code == 200


def test_get_accounts(client):
    """Test the get accounts route."""
    response = client.get("/accounts")
    assert response.status_code == 200


def test_create_account(client, db):
    """Test the create account route."""
    # First create a test user
    user = client.post(
        "/users",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
        },
    )
    user_id = user.json["data"]["id"]

    # Then create account for this user
    payload = AccountRegisterSchema(
        user_id=user_id,
        account_type="savings",
        account_number="123456789",
        balance=1000.00,
        image_uri="http://example.com/image.jpg",
        name="John Doe",
        birth_date="1990-01-01",
        address="123 Main St",
        gender="male",
        phone="123-456-7890",
    )
    response = client.post("/accounts", json=payload.model_dump())
    assert response.status_code == 201


def test_create_user_success(client, db):
    """Test the create user route."""
    response = client.post(
        "/users",
        json={
            "username": "john",
            "email": "john@mail.com",
            "password": "johnpassword123",
        },
    )
    assert response.status_code == 201
    assert response.json["success"]
    assert response.json["data"]["username"] == "john"
    query = db.select(User).filter(User.email == "john@mail.com")
    data = db.session.execute(query).scalar_one()
    assert data.username == "john"
    assert data.email == "john@mail.com"


def test_create_user_failure(client):
    """Test the create user route."""
    response = client.post(
        "/users",
        json={
            "username": "john",
            # "email": "john@mail.com", # Missing email
            "password": "johnpassword123",
        },
    )
    assert response.status_code == 400
    assert not response.json["success"]
    # print(response.json)
