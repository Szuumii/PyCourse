from fastapi.testclient import TestClient
from main import app
import pytest
import sqlite3

client = TestClient(app)


def test_hello_world():
    response = client.get('/')
    assert response.status_code == 200

def test_get_tracks():
    '''
    with sqlite3.connect('chinook.db') as connection:
        cursor = connection.cursor()
        tracks = cursor.execute("SELECT * FROM tracks ORDER BY TrackId LIMIT 5 OFFSET 10").fetchall()
        '''
        response = client.get("/tracks/5/10")
        assert response.status_code == 200
        assert response.json() == tracks

def test_get_composers():
    response = client.get("/tracks/composers")
    assert response.status_code == 200
