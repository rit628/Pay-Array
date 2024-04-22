import os
from ..auth import decode_token
AUTH_TYPE = os.environ.get("AUTH_TYPE")
API_VERSION = os.environ.get("API_VERSION")
API_ROOT_PATH = f"/api/{API_VERSION}"

def test_household_creation(client):
    response = client.post(f"{API_ROOT_PATH}/users/household/create/")
    assert response.status_code == 201
    assert response.get_json() == 1

    response = client.post(f"{API_ROOT_PATH}/users/household/create/")
    assert response.status_code == 201
    assert response.get_json() == 2