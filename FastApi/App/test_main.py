from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)


def test_hello_world():
    response = client.get('/')
    assert response.status_code == 200
    response = client.get("/welcome")
    assert response.status_code == 200

@pytest.mark.parametrize("name",["Ala", "Beata","Kamil"])
def test_hello_name(name):
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello {name}"}

def test_method_GET():
    response = client.get("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "GET"}

def test_method_POST():
    response = client.post("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "POST"}

def test_method_PUT():
    response = client.put("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "PUT"}

def test_method_DELETE():
    response = client.delete("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "DELETE"}

def test_recieve_patient():
    response1 = client.post("/patient",json={"name":"NAME0", "surename":"SURNAME0"})
    assert response1.status_code == 200
    response2 = client.post("/patient",json={"name":"NAME1", "surename":"SURNAME1"})
    assert response2.status_code == 200
    assert response1.json() == {"id": 0, "patient": {"name": "NAME0", "surename": "SURNAME0"}}
    assert response2.json() == {"id": 1, "patient": {"name": "NAME1", "surename": "SURNAME1"}}


def test_give_patient_under_id():
    client.post("/patient",json={"name":"NAME0", "surename":"SURNAME0"})
    response = client.get("/patient/0")
    assert response.status_code == 200
    assert response.json() == {"name": "NAME0", "surename": "SURNAME0"}

    client.post("/patient",json={"name":"NAME1", "surename":"SURNAME1"})
    response = client.get("/patient/1")
    assert response.status_code == 200
    assert response.json() == {"name": "NAME1", "surename": "SURNAME1"}

    response = client.get("/patient/4")
    assert response.status_code == 204

def test_reset_list():
    response = client.get("/reset")

    assert response.status_code == 200
    assert response.json() == {"message" : "Paient list cleared"}

    client.post("/patient",json={"name":"Jakub", "surename":"Szumski"})
    response = client.get("/patient/0")
    assert response.status_code == 200
    assert response.json() == {"name": "Jakub", "surename": "Szumski"}

    client.get("/reset")


def test_login():
    response = client.post("/login")

    assert response.status_code == 200
    


