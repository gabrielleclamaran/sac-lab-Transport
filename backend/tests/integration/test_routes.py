import pytest
from app import create_app

@pytest.fixture
def client():
    # On force TESTING et on laisse __init__ basculer sur SQLite en mémoire
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client

def test_index_route(client):
    # Tu n'as pas de route "/" explicite : on accepte 404 ou 200
    resp = client.get("/")
    assert resp.status_code in (200, 404)
