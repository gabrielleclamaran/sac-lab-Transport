# Application de Transport Pédiatrique — CHU Sainte‑Justine

Application destinée à l’équipe de transport pédiatrique pour :
- créer/mettre à jour des dossiers de transport ;
- saisir les diagnostics, co‑morbidités et **signes vitaux** (à l’arrivée & au départ) ;
- téléverser des **CSV Zoll** ;
- générer un **PDF lisible pour les cliniciens** (tableaux plutôt que courbes temporelles).

> ⚠️ Aucune donnée réelle de patient ne doit être stockée dans ce dépôt. Voir **Confidentialité & Sécurité**.

---

## Sommaire
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Démarrage rapide](#démarrage-rapide)
  - [Avec Docker](#avec-docker)
- [Configuration](#configuration)
- [API](#api)
- [Génération du PDF](#génération-du-pdf)
- [Tests & Couverture](#tests--couverture)
- [CI/CD](#cicd)
- [Arborescence](#arborescence)
- [Conventions](#conventions)
- [Feuille de route](#feuille-de-route)
- [Confidentialité & Sécurité](#confidentialité--sécurité)
- [Licence](#licence)

---

## Architecture
```
React (Vite) :3001  ──▶  Flask API :5050  ──▶  PostgreSQL
          ▲                 │
          └──── PDF (téléchargement)  +  Téléversement CSV (Zoll)
```

---

## Technologies
- **Backend :** Python 3.10, Flask, Flask‑CORS, SQLAlchemy, ReportLab  
- **Base de données :** PostgreSQL (Docker)  
- **Frontend :** React (Vite)  
- **Outillage :** Pytest (+ couverture), Ruff, Black, Docker, GitHub Actions

---

## Démarrage rapide

### Avec Docker
Prérequis : Docker & Docker Compose.

```bash
# Lancer les services
docker compose up -d

# Accès
# API backend :  http://localhost:5050
# Frontend     :  http://localhost:3001

# Logs / Arrêt
docker compose logs -f
docker compose down
# (effacer le volume DB) docker compose down -v
```
---

## Configuration
Les variables utiles (Docker Compose fournit des valeurs par défaut cohérentes) :

```
# Backend
BACKEND_PORT=5000               # port du conteneur, publié en 5050 sur l'hôte
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/transport
CORS_ORIGINS=http://localhost:3001
UPLOAD_FOLDER=/app/zoll_uploads

# Frontend
VITE_API_URL=http://localhost:5050
```
---

## API
Base locale : **http://localhost:5050**

- `GET /patients` — lister les patients  
- `POST /patients` — créer  
- `PUT /patients/<id>` — modifier  
- `DELETE /patients/<id>` — supprimer  
- `GET /patients/<id>` — récupérer un patient (recommandé)  
- `POST /patients/<id>/upload` — téléverser un **CSV Zoll**  
- `GET /patients/<id>/pdf` — télécharger le **PDF** du patient

Exemple de payload `POST /patients` :
```json
{
  "name": "Doe, Jane",
  "age": 5,
  "sex": "F",
  "transfer_reason": "Détresse respiratoire",
  "transport_team_diagnosis": "Bronchiolite",
  "secondary_diagnosis": null,
  "comorbidities": "Prématurité",
  "heart_rate": 120,
  "respiratory_rate": 32,
  "saturation": 95,
  "fio2": 0.3,
  "blood_pressure": "95/60",
  "temperature": 37.5,
  "glasgow_score": 15,
  "departure_heart_rate": 118,
  "departure_respiratory_rate": 30,
  "departure_saturation": 96,
  "departure_fio2": 0.3,
  "departure_blood_pressure": "92/58",
  "departure_temperature": 37.2,
  "departure_glasgow_score": 15
}
```

---

## Génération du PDF
- Endpoint : **`GET /patients/<id>/pdf`**  
- Généré avec **ReportLab**.  
- Présentation optimisée :  
  - **Tableaux** des constantes à l’**arrivée** et au **départ** ;  
  - Sections diagnostic (principal/secondaire + évaluation équipe transport) ;  
  - Intégration optionnelle d’un **résumé du CSV Zoll** téléversé.

---

## Tests & Couverture
Exécuter tous les tests :
```bash
pytest -q --cov=app --cov-report=term-missing:skip-covered --cov-report=html
# ouvrir htmlcov/index.html
```

- Le workflow CI applique un **seuil de couverture** (par défaut 70 %). Modifiable via `--cov-fail-under=NN` dans `.github/workflows/ci.yml`.  
- Les rapports HTML/XML sont publiés en **artifacts** sur GitHub Actions.

---

## CI/CD
Workflow : `.github/workflows/ci.yml`
- **python-tests** : installation des dépendances, tests Pytest + couverture, artifacts.  
- **frontend-build** : construction du frontend si un `package.json` est détecté.  
- **docker-build** : build des images backend/frontend si `Dockerfile.*` existent.  
- **Codecov (optionnel)** : définir le secret `CODECOV_TOKEN` pour activer l’upload.

Rendre la CI obligatoire sur les PR : *Settings → Branches → Require status checks to pass*.

---

## Arborescence
```
.
├─ backend/
│  └─ app/
│     ├─ __init__.py
│     ├─ models.py
│     ├─ pdf_utils.py
│     └─ routes.py
├─ frontend/
│  └─ src/...
├─ zoll_uploads/
├─ docker-compose.yml
├─ Dockerfile.backend
├─ Dockerfile.frontend
└─ .github/workflows/ci.yml
```

---

## Conventions
- **API** : JSON, `snake_case`, codes d’erreurs explicites.  
- **Git** : branches de fonctionnalité (`feature/...`), commits conventionnels (`feat:`, `fix:`).

---

## Feuille de route
- Documentation OpenAPI/Swagger (flasgger / apispec).  
- Validation des entrées (pydantic / marshmallow).  
- Authentification & rôles (JWT ou session).  
- Migrations DB (Alembic).  
- Pagination/filtrage sur `/patients`.  
- Parsing CSV avancé (Zoll) + intégration **Hamilton T1**.  
- Tests E2E (Playwright/Cypress).  
- Journalisation structurée & suivi d’erreurs (Sentry).  
- Stratégie de sauvegarde pour le volume Postgres.

---

## Confidentialité & Sécurité
- Ne jamais committer de **PHI** (données identifiantes).  
- Restreindre l’accès aux déploiements ; utiliser **HTTPS** en prod.  
- Gérer les secrets via variables d’environnement (CI/CD et prod).  
- Tracer les modifications (audit) sur les dossiers patients.

---

