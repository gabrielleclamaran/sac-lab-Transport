from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config: dict | None = None):
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Valeurs par défaut (prod/dev)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/medical_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Surcharges éventuelles (tests, etc.)
    if config:
        app.config.update(config)
        # Si tests ⇒ bascule DB sur SQLite en mémoire (sauf si l'appelant a déjà fourni une URI)
        if app.config.get("TESTING") and 'SQLALCHEMY_DATABASE_URI' not in config:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    db.init_app(app)

    from .routes import bp
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app
