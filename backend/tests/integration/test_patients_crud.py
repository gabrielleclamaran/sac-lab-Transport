import pytest
import time
from app import create_app


def get_all_patients(client):
    """Récupère tous les patients"""
    r = client.get("/patients")
    assert r.status_code == 200, f"GET /patients failed: {r.status_code}"
    return r.get_json()


def create_patient(client, name=None, age=25, sex="M"):
    """Crée un patient et retourne son ID"""
    if name is None:
        name = f"TestPatient_{int(time.time())}"

    payload = {"name": name, "age": age, "sex": sex}
    r = client.post("/patients", json=payload)
    assert r.status_code == 201, f"POST failed: {r.status_code} - {r.get_data(as_text=True)}"

    # Trouver le patient créé dans la liste
    patients = get_all_patients(client)
    for p in patients:
        if p.get("name") == name and p.get("age") == age:
            return p.get("id")

    assert False, f"Patient '{name}' non trouvé après création"


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_create_and_get_patient(client):
    """Test création et récupération d'un patient"""
    patient_id = create_patient(client, age=7, sex="F")

    # Récupérer le patient par son ID
    r = client.get(f"/patients/{patient_id}")
    assert r.status_code == 200, f"GET /patients/{patient_id} failed: {r.status_code}"

    data = r.get_json()
    assert data.get("age") == 7
    assert data.get("sex") == "F"


def test_list_patients(client):
    """Test récupération de la liste des patients"""
    # Créer quelques patients
    id1 = create_patient(client, age=3, sex="F")
    id2 = create_patient(client, age=5, sex="M")

    patients = get_all_patients(client)
    assert isinstance(patients, list)
    assert len(patients) >= 2

    # Vérifier que nos patients sont présents
    ids = [p.get("id") for p in patients]
    assert id1 in ids
    assert id2 in ids


def test_update_patient(client):
    """Test mise à jour d'un patient"""
    patient_id = create_patient(client, age=9, sex="M")

    # Mise à jour
    update_payload = {"name": "PatientUpdated", "age": 10, "sex": "M"}
    r = client.put(f"/patients/{patient_id}", json=update_payload)
    assert r.status_code == 200, f"PUT failed: {r.status_code} - {r.get_data(as_text=True)}"

    # Vérifier la mise à jour
    r = client.get(f"/patients/{patient_id}")
    assert r.status_code == 200
    data = r.get_json()
    assert data.get("age") == 10


def test_delete_patient(client):
    """Test suppression d'un patient"""
    patient_id = create_patient(client, age=2, sex="F")

    # Supprimer
    r = client.delete(f"/patients/{patient_id}")
    assert r.status_code == 200, f"DELETE failed: {r.status_code} - {r.get_data(as_text=True)}"

    # Vérifier que le patient n'existe plus
    r = client.get(f"/patients/{patient_id}")
    assert r.status_code == 404, "Patient should be deleted"


def test_get_nonexistent_patient(client):
    """Test récupération d'un patient inexistant"""
    r = client.get("/patients/99999")
    assert r.status_code == 404


def test_update_nonexistent_patient(client):
    """Test mise à jour d'un patient inexistant"""
    r = client.put("/patients/99999", json={"name": "Test", "age": 30, "sex": "M"})
    assert r.status_code == 404


def test_delete_nonexistent_patient(client):
    """Test suppression d'un patient inexistant"""
    r = client.delete("/patients/99999")
    assert r.status_code == 404