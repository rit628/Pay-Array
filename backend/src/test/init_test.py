from .. import server

client = server.app.test_client()

def test_server_runtime():
    response = client.get("/validate-server-runtime")

    assert response.status_code == 200
    assert response.get_json() == "Hello World!"

def test_db_connection():
    response = client.get("/validate-db-connection")

    assert response.status_code == 200
    assert response.get_json() == [["item"], ["user"], ["user_preference"]]