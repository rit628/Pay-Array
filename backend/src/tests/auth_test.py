from ..auth import decode_token

def test_user_creation_success(client):
    response = client.post("/api/v1/users", json={
        "username" : "testUser999",
        "first_name" : "Test",
        "last_name" : "User",
        "email" : "testuser@domain.com",
        "phone" : "1234567890",
        "password" : "terrible_password"
    })

    assert response.status_code == 201
    assert response.get_json() == "User Created Successfully."

def test_user_creation_no_password(client):
    response = client.post("/api/v1/users", json={
        "username" : "testUser999",
        "first_name" : "Test",
        "last_name" : "User",
        "email" : "testuser@domain.com",
        "phone" : "1234567890",
    })

    assert response.status_code == 400
    assert response.get_json() == "No Password Provided."

def test_user_creation_invalid_email(client):
    response = client.post("/api/v1/users", json={
        "username" : "testUser999",
        "first_name" : "Test",
        "last_name" : "User",
        "email" : "testuser@domain",
        "phone" : "1234567890",
        "password" : "terrible_password"
    })

    assert response.status_code == 400
    assert response.get_json() == "Invalid email."

def test_user_creation_invalid_name(client):
    response = client.post("/api/v1/users", json={
        "username" : "testUser999",
        "first_name" : "Test1",
        "last_name" : "User",
        "email" : "testuser@domain.com",
        "phone" : "1234567890",
        "password" : "terrible_password"
    })

    assert response.status_code == 400
    assert response.get_json() == "Invalid first_name."

def test_user_creation_invalid_username(client):
    response = client.post("/api/v1/users", json={
        "username" : "testUser 999",
        "first_name" : "Test",
        "last_name" : "User",
        "email" : "testuser@domain.com",
        "phone" : "1234567890",
        "password" : "terrible_password"
    })

    assert response.status_code == 400
    assert response.get_json() == "Invalid username."

def test_user_creation_invalid_phone_number(client):
    response = client.post("/api/v1/users", json={
        "username" : "testUser999",
        "first_name" : "Test",
        "last_name" : "User",
        "email" : "testuser@domain.com",
        "phone" : "12345678909",
        "password" : "terrible_password"
    })

    assert response.status_code == 400
    assert response.get_json() == "Invalid phone."

def test_user_creation_duplicate(client):
    # creates user initially
    client.post("/api/v1/users", json={
        "username" : "testUser999",
        "first_name" : "Test",
        "last_name" : "User",
        "email" : "testuser@domain.com",
        "phone" : "1234567890",
        "password" : "terrible_password"
    })

    # attempts to create new user with same username
    response = client.post("/api/v1/users", json={
        "username" : "testUser999",
        "first_name" : "Test",
        "last_name" : "User",
        "email" : "testuser@domain.com",
        "phone" : "1234567890",
        "password" : "terrible_password"
    })

    assert response.status_code == 400
    assert response.get_json() == "testUser999 is already taken."

def test_user_login_success(client):
    response = client.post("/api/v1/users", json={
        "username" : "testUser999",
        "first_name" : "Test",
        "last_name" : "User",
        "email" : "testuser@domain.com",
        "phone" : "1234567890",
        "password" : "terrible_password"
    })

    response = client.post("/api/v1/login", json={
        "username" : "testUser999",
        "password" : "terrible_password"
    })

    assert response.status_code == 201
    assert decode_token(response.get_json())["user_id"] == 1

def test_user_login_incorrect_password(client):
    # creates user
    client.post("/api/v1/users", json={
        "username" : "testUser999",
        "first_name" : "Test",
        "last_name" : "User",
        "email" : "testuser@domain.com",
        "phone" : "1234567890",
        "password" : "terrible_password"
    })

    # Login to created user
    response = client.post("/api/v1/login", json={
        "username" : "testUser999",
        "password" : "wrong_password"
    })

    assert response.status_code == 401
    assert response.get_json() == "Incorrect Password."

def test_user_login_invalid_username(client):
    response = client.post("/api/v1/login", json={
        "username" : "nonexistentUser",
        "password" : "terrible_password"
    })

    assert response.status_code == 404
    assert response.get_json() == "No Account with Username: nonexistentUser."