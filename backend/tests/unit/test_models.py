from app import models

def test_patient_model_structure_minimal():
    # 1) La classe doit exister
    Patient = getattr(models, "Patient", None)
    assert Patient is not None, "Class 'Patient' not found in app.models"

    # 2) Instanciation sans toucher la DB (SQLAlchemy autorise __init__() vide)
    p = Patient()
    assert isinstance(p, Patient)

    # 3) Inspection des colonnes disponibles sans initialiser d’engine
    #    (ne crée pas de tables ni de connexion)
    assert hasattr(Patient, "__table__"), "Patient has no __table__ (not a SQLAlchemy model?)"
    cols = {c.name for c in Patient.__table__.columns}

    # 4) Vérifications minimales mais robustes
    #    - un identifiant
    id_candidates = {"id", "patient_id", "id_patient"}
    assert cols & id_candidates, f"Aucune colonne id trouvée parmi {sorted(id_candidates)} ; colonnes = {sorted(cols)}"

    #    - un âge (ou champ similaire; adapte si tu utilises un autre nom)
    age_candidates = {"age", "age_annees", "age_years"}
    assert cols & age_candidates, f"Aucune colonne âge trouvée parmi {sorted(age_candidates)} ; colonnes = {sorted(cols)}"

    #    - un nom si présent (optionnel) : on ne l’exige pas pour ne pas casser si ton modèle n’en a pas
    name_candidates = {"nom", "name", "full_name", "patient_name"}
    _ = cols & name_candidates  # juste pour info ; pas d'assert ici
