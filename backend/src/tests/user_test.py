import os
from ..auth import decode_token
AUTH_TYPE = os.environ.get("AUTH_TYPE")
API_VERSION = os.environ.get("API_VERSION")
API_ROOT_PATH = f"/api/{API_VERSION}"

def test_get_account_details(client):
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

    response = client.get(f"{API_ROOT_PATH}/users/me/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 200
    assert response.get_json() == {
        "username" : "testUser999",
        "first_name" : "Test",
        "last_name" : "User",
        "email" : "testuser@domain.com",
        "phone" : "1234567890",
        "household_id" : None,
        "balance" : None
    }

def test_get_account_resource(client):
    response = client.post(f"{API_ROOT_PATH}/users/", json={
        "username" : "testUser999",
        "email" : "testuser@domain.com",
        "password" : "terrible_password"
    })

    response = client.post(f"{API_ROOT_PATH}/login/", json={
        "username" : "testUser999",
        "password" : "terrible_password"
    })

    auth_header = response.get_json()

    response = client.get(f"{API_ROOT_PATH}/users/me/email/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 200
    assert response.get_json() == "testuser@domain.com"

def test_access_protected_resource(client):
    response = client.post(f"{API_ROOT_PATH}/users/", json={
        "username" : "testUser999",
        "email" : "testuser@domain.com",
        "password" : "terrible_password"
    })

    response = client.post(f"{API_ROOT_PATH}/login/", json={
        "username" : "testUser999",
        "password" : "terrible_password"
    })

    auth_header = response.get_json()

    response = client.get(f"{API_ROOT_PATH}/users/me/id/", headers={
        "Authorization": auth_header
    })

    assert response.status_code == 404
    assert response.get_json() == "Requested resource does not exist. user has no attribute id."

    response = client.get(f"{API_ROOT_PATH}/users/me/password/", headers={
        "Authorization": auth_header
    })

    assert response.status_code == 404
    assert response.get_json() == "Requested resource does not exist. user has no attribute password."

    response = client.get(f"{API_ROOT_PATH}/users/me/password_hash/", headers={
        "Authorization": auth_header
    })

    assert response.status_code == 404
    assert response.get_json() == "Requested resource does not exist. user has no attribute password_hash."

    response = client.get(f"{API_ROOT_PATH}/users/me/salt/", headers={
        "Authorization": auth_header
    })

    assert response.status_code == 404
    assert response.get_json() == "Requested resource does not exist. user has no attribute salt."

def test_delete_account(client):
    response = client.post(f"{API_ROOT_PATH}/users/", json={
        "username" : "testUser999",
        "email" : "testuser@domain.com",
        "password" : "terrible_password"
    })

    response = client.post(f"{API_ROOT_PATH}/login/", json={
        "username" : "testUser999",
        "password" : "terrible_password"
    })

    auth_header = response.get_json()

    response = client.delete(f"{API_ROOT_PATH}/users/me/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 200
    assert response.get_json() == "User Deleted Successfully."

def test_delete_account_resource(client):
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

    response = client.delete(f"{API_ROOT_PATH}/users/me/phone/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 200
    assert response.get_json() == "User's phone Deleted Successfully."

    response = client.get(f"{API_ROOT_PATH}/users/me/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 200
    assert response.get_json() == {
        "username" : "testUser999",
        "first_name" : "Test",
        "last_name" : "User",
        "email" : "testuser@domain.com",
        "phone" : None,
        "household_id" : None,
        "balance" : None
    }

def test_delete_protected_account_resource(client):
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

    response = client.delete(f"{API_ROOT_PATH}/users/me/email/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 400
    assert response.get_json() == "User's email cannot be deleted."


def test_edit_account(client):
    response = client.post(f"{API_ROOT_PATH}/users/", json={
        "username" : "testUser999",
        "email" : "testuser@domain.com",
        "password" : "terrible_password",
        "first_name" : "Tester"
    })

    response = client.post(f"{API_ROOT_PATH}/login/", json={
        "username" : "testUser999",
        "password" : "terrible_password"
    })

    auth_header = response.get_json()

    response = client.post(f"{API_ROOT_PATH}/users/me/", headers={
        "Authorization" : auth_header
    }, json={
        "email" : "newemail@newdomain.net",
        "first_name" : "NewName"
    })

    assert response.status_code == 200
    assert response.get_json() == "User Updated Successfully."

    response = client.get(f"{API_ROOT_PATH}/users/me/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 200
    email = response.get_json()["email"]
    first_name = response.get_json()["first_name"]
    assert email == "newemail@newdomain.net"
    assert first_name == "NewName"

def test_edit_account_resource(client):
    response = client.post(f"{API_ROOT_PATH}/users/", json={
        "username" : "testUser999",
        "email" : "testuser@domain.com",
        "password" : "terrible_password",
        "first_name" : "Tester"
    })

    response = client.post(f"{API_ROOT_PATH}/login/", json={
        "username" : "testUser999",
        "password" : "terrible_password"
    })

    auth_header = response.get_json()

    response = client.post(f"{API_ROOT_PATH}/users/me/email/", headers={
        "Authorization" : auth_header
    }, json="newemail@newdomain.net")

    assert response.status_code == 200
    assert response.get_json() == "User's email Updated Successfully."

    response = client.get(f"{API_ROOT_PATH}/users/me/email/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 200
    assert response.get_json() == "newemail@newdomain.net"

def test_edit_account_password(client):
    response = client.post(f"{API_ROOT_PATH}/users/", json={
        "username" : "testUser999",
        "email" : "testuser@domain.com",
        "password" : "terrible_password",
        "first_name" : "Tester"
    })

    response = client.post(f"{API_ROOT_PATH}/login/", json={
        "username" : "testUser999",
        "password" : "terrible_password"
    })

    auth_header = response.get_json()

    response = client.post(f"{API_ROOT_PATH}/users/me/password/", headers={
        "Authorization" : auth_header
    }, json="even_worse_password")

    assert response.status_code == 200
    assert response.get_json() == "User's password Updated Successfully."

    response = client.post(f"{API_ROOT_PATH}/login/", json={
        "username" : "testUser999",
        "password" : "terrible_password"
    })

    assert response.status_code == 401
    assert response.get_json() == "Incorrect Password."

    response = client.post(f"{API_ROOT_PATH}/login/", json={
        "username" : "testUser999",
        "password" : "even_worse_password"
    })

    assert response.status_code == 201
    _, token = response.get_json().split()
    assert decode_token(token)["user_id"] == 1

def test_username_update_duplicate(client):
    response = client.post(f"{API_ROOT_PATH}/users/", json={
        "username" : "testUser999",
        "email" : "testuser@domain.com",
        "password" : "terrible_password"
    })

    response = client.post(f"{API_ROOT_PATH}/users/", json={
        "username" : "testUser1000",
        "email" : "testuser@domain.com",
        "password" : "terrible_password"
    })

    response = client.post(f"{API_ROOT_PATH}/login/", json={
        "username" : "testUser999",
        "password" : "terrible_password"
    })

    auth_header = response.get_json()

    response = client.post(f"{API_ROOT_PATH}/users/me/", headers={
        "Authorization": auth_header
    }, json={
        "username": "testuser1000"
    })

    assert response.status_code == 400
    assert response.get_json() == "testuser1000 is already taken."