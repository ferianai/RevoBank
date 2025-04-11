def test_index(client):
    """Test the index route."""
    response = client.get("/")
    assert response.status_code == 200


def test_get_accounts(client):
    """Test the get accounts route."""
    response = client.get("/accounts")
    assert response.status_code == 200


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
