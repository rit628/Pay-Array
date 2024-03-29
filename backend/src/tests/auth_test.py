import os
from ..auth import decode_token
AUTH_TYPE = os.environ.get("AUTH_TYPE")
API_VERSION = os.environ.get("API_VERSION")
API_ROOT_PATH = f"/api/{API_VERSION}"

def test_user_creation_success(client):
    response = client.post(f"{API_ROOT_PATH}/users/", json={
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
    response = client.post(f"{API_ROOT_PATH}/users/", json={
        "username" : "testUser999",
        "first_name" : "Test",
        "last_name" : "User",
        "email" : "testuser@domain.com",
        "phone" : "1234567890",
    })

    assert response.status_code == 400
    assert response.get_json() == "No Password Provided."

def test_user_creation_invalid_email(client):
    response = client.post(f"{API_ROOT_PATH}/users/", json={
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
    response = client.post(f"{API_ROOT_PATH}/users/", json={
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
    response = client.post(f"{API_ROOT_PATH}/users/", json={
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
    response = client.post(f"{API_ROOT_PATH}/users/", json={
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
    client.post(f"{API_ROOT_PATH}/users/", json={
        "username" : "testUser999",
        "first_name" : "Test",
        "last_name" : "User",
        "email" : "testuser@domain.com",
        "phone" : "1234567890",
        "password" : "terrible_password"
    })

    # attempts to create new user with same username
    response = client.post(f"{API_ROOT_PATH}/users/", json={
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
    response = client.post(f"{API_ROOT_PATH}/users/", json={
        "username" : "testUser999",
        "first_name" : "Test",
        "last_name" : "User",
        "email" : "testuser@domain.com",
        "phone" : "1234567890",
        "password" : "terrible_password"
    })

    response = client.post(f"{API_ROOT_PATH}/login/", json={
        "username" : "testUser999",
        "password" : "terrible_password"
    })


    assert response.status_code == 201

    auth_type, token = response.get_json().split()
    assert auth_type == AUTH_TYPE
    assert decode_token(token)["user_id"] == 1

def test_user_login_incorrect_password(client):
    # creates user
    client.post(f"{API_ROOT_PATH}/users/", json={
        "username" : "testUser999",
        "first_name" : "Test",
        "last_name" : "User",
        "email" : "testuser@domain.com",
        "phone" : "1234567890",
        "password" : "terrible_password"
    })

    # Login to created user
    response = client.post(f"{API_ROOT_PATH}/login/", json={
        "username" : "testUser999",
        "password" : "wrong_password"
    })

    assert response.status_code == 401
    assert response.get_json() == "Incorrect Password."

def test_user_login_invalid_username(client):
    response = client.post(f"{API_ROOT_PATH}/login/", json={
        "username" : "nonexistentUser",
        "password" : "terrible_password"
    })

    assert response.status_code == 404
    assert response.get_json() == "No Account with Username: nonexistentUser."

def test_user_logout(client):
    response = client.post(f"{API_ROOT_PATH}/users/", json={
        "username" : "testUser999",
        "first_name" : "Test",
        "last_name" : "User",
        "email" : "testuser@domain.com",
        "phone" : "1234567890",
        "password" : "terrible_password"
    })

    response = client.post(f"{API_ROOT_PATH}/login/", json={
        "username" : "testUser999",
        "password" : "terrible_password"
    })

    auth_header = response.get_json()

    response = client.delete(f"{API_ROOT_PATH}/logout/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 200
    assert response.get_json() == "Logout Successful."

    response = client.get(f"{API_ROOT_PATH}/users/me/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 401
    assert response.get_json() == "Invalid Token."
