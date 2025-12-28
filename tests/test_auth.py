from fastapi import status

def test_register_user(client):
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "testpass123"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "password" not in data

def test_register_duplicate_username(client):
    user_data = {
        "username": "duplicate",
        "email": "duplicate@example.com",
        "password": "testpass123"
    }
    client.post("/auth/register", json=user_data)
    
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_login_success(client, test_user):
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    login_data = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_login_nonexistent_user(client):
    login_data = {
        "username": "nonexistent",
        "password": "password"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED