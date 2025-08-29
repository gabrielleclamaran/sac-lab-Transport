import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_debug_routes(client):
    """Test pour déboguer les routes disponibles"""

    # 1. Créer un patient d'abord
    payload = {"name": "TestDebug", "age": 25, "sex": "M"}
    create_resp = client.post("/patients", json=payload)
    print(f"POST /patients: {create_resp.status_code} - {create_resp.get_data(as_text=True)}")

    # 2. Lister tous les patients pour récupérer l'ID
    list_resp = client.get("/patients")
    print(f"GET /patients: {list_resp.status_code}")

    if list_resp.status_code == 200:
        patients = list_resp.get_json()
        if isinstance(patients, list) and len(patients) > 0:
            patient_id = patients[-1].get('id')  # Prendre le dernier créé
            print(f"Patient ID trouvé: {patient_id}")

            # 3. Tester GET d'un patient spécifique
            get_resp = client.get(f"/patients/{patient_id}")
            print(f"GET /patients/{patient_id}: {get_resp.status_code}")

            # 4. Tester PUT
            put_resp = client.put(f"/patients/{patient_id}", json={"name": "TestDebugUpdated", "age": 26, "sex": "M"})
            print(f"PUT /patients/{patient_id}: {put_resp.status_code} - {put_resp.get_data(as_text=True)}")

            # 5. Tester DELETE
            delete_resp = client.delete(f"/patients/{patient_id}")
            print(f"DELETE /patients/{patient_id}: {delete_resp.status_code} - {delete_resp.get_data(as_text=True)}")

            # 6. Vérifier que le DELETE a fonctionné
            get_after_delete = client.get(f"/patients/{patient_id}")
            print(f"GET après DELETE: {get_after_delete.status_code}")

    # 7. Lister toutes les routes disponibles
    from flask import current_app
    print("\n=== Routes disponibles ===")
    for rule in current_app.url_map.iter_rules():
        methods = ', '.join(rule.methods - {'HEAD', 'OPTIONS'})
        print(f"{rule.endpoint}: {rule.rule} [{methods}]")


def test_check_app_config(client):
    """Vérifier la configuration de l'app"""
    from flask import current_app
    print(f"Testing: {current_app.config.get('TESTING')}")
    print(f"DB URI: {current_app.config.get('SQLALCHEMY_DATABASE_URI')}")

    # Vérifier que les blueprints sont bien enregistrés
    print("Blueprints enregistrés:")
    for bp_name, bp in current_app.blueprints.items():
        print(f"  - {bp_name}: {bp}")