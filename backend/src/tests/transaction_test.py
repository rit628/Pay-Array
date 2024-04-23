import os
from ..auth import decode_token
AUTH_TYPE = os.environ.get("AUTH_TYPE")
API_VERSION = os.environ.get("API_VERSION")
API_ROOT_PATH = f"/api/{API_VERSION}"

def test_make_transaction(client):
    response = client.post(f"{API_ROOT_PATH}/users/", json={
        "username" : "testUser999",
        "email" : "testuser@domain.com",
        "password" : "terrible_password",
        "first_name" : "Tester"
    })

    response = client.post(f"{API_ROOT_PATH}/users/", json={
        "username" : "testUser1000",
        "email" : "testuser1@domain.com",
        "password" : "terrible_password",
        "first_name" : "TesterOne"
    })

    assert response.status_code == 201
    assert response.get_json() == "User Created Successfully."

    response = client.post(f"{API_ROOT_PATH}/login/", json={
        "username" : "testUser999",
        "password" : "terrible_password"
    })

    auth_header = response.get_json()

    response = client.get(f"{API_ROOT_PATH}/users/me/transactions/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 200
    assert response.get_json() == []

    response = client.post(f"{API_ROOT_PATH}/users/me/transactions/", headers={
        "Authorization" : auth_header
    }, json={
        "amount": 10.10,
        "message": "apples",
        "users": ["testUser1000"]
    })

    assert response.status_code == 200
    assert response.get_json() == f"Transaction complete."

    response = client.get(f"{API_ROOT_PATH}/users/me/transactions/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 200
    assert response.get_json() == [
        {   
            "id" : 1,
            "amount" : '10.10',
            "completed" : False,
            "message" : "apples",
            "item_id" : 1,
            "purchaser" : "testUser999"
        }
    ]

    response = client.get(f"{API_ROOT_PATH}/users/me/transactions/due/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 200
    assert response.get_json() == []

    response = client.post(f"{API_ROOT_PATH}/login/", json={
        "username" : "testUser1000",
        "password" : "terrible_password"
    })

    auth_header = response.get_json()

    response = client.get(f"{API_ROOT_PATH}/users/me/transactions/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 200
    assert response.get_json() == [
        {   
            "id" : 1,
            "amount" : '10.10',
            "completed" : False,
            "message" : "apples",
            "item_id" : 1,
            "purchaser" : "testUser999"
        }
    ]

    response = client.get(f"{API_ROOT_PATH}/users/me/transactions/due/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 200
    assert response.get_json() == [
        {   
            "id" : 1,
            "amount" : '10.10',
            "completed" : False,
            "message" : "apples",
            "item_id" : 1,
            "purchaser" : "testUser999"
        }
    ]

def test_pay_transaction(client):
    response = client.post(f"{API_ROOT_PATH}/users/", json={
        "username" : "testUser999",
        "email" : "testuser@domain.com",
        "password" : "terrible_password",
        "first_name" : "Tester"
    })

    response = client.post(f"{API_ROOT_PATH}/users/", json={
        "username" : "testUser1000",
        "email" : "testuser1@domain.com",
        "password" : "terrible_password",
        "first_name" : "TesterOne",
        "balance": 100
    })

    assert response.status_code == 201
    assert response.get_json() == "User Created Successfully."

    response = client.post(f"{API_ROOT_PATH}/login/", json={
        "username" : "testUser999",
        "password" : "terrible_password"
    })

    auth_header = response.get_json()

    response = client.get(f"{API_ROOT_PATH}/users/me/transactions/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 200
    assert response.get_json() == []

    response = client.post(f"{API_ROOT_PATH}/users/me/transactions/", headers={
        "Authorization" : auth_header
    }, json={
        "amount": 10.10,
        "message": "apples",
        "users": ["testUser1000"]
    })

    assert response.status_code == 200
    assert response.get_json() == f"Transaction complete."

    response = client.get(f"{API_ROOT_PATH}/users/me/transactions/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 200
    assert response.get_json() == [
        {   
            "id" : 1,
            "amount" : '10.10',
            "completed" : False,
            "message" : "apples",
            "item_id" : 1,
            "purchaser" : "testUser999"
        }
    ]

    response = client.post(f"{API_ROOT_PATH}/login/", json={
        "username" : "testUser1000",
        "password" : "terrible_password"
    })

    auth_header = response.get_json()

    response = client.get(f"{API_ROOT_PATH}/users/me/transactions/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 200
    assert response.get_json() == [
        {   
            "id" : 1,
            "amount" : '10.10',
            "completed" : False,
            "message" : "apples",
            "item_id" : 1,
            "purchaser" : "testUser999"
        }
    ]

    response = client.post(f"{API_ROOT_PATH}/users/me/transactions/1/pay/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 200
    assert response.get_json() == "Transaction paid successfully."


    response = client.get(f"{API_ROOT_PATH}/users/me/balance/", headers={
        "Authorization" : auth_header
    })

    assert response.status_code == 200
    assert response.get_json() == '94.95'

