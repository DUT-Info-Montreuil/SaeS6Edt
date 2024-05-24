import pytest
from database.config import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.Disponibilite import Disponibilite  
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app

@pytest.fixture(name="app")
def app():
    app = create_app()

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

# Tests unitaires pour l'initialisation d'une disponibilité
def test_disponibilite_initialization(app):

    # Create a test instance
    disponibilite = Disponibilite(
        enseignant="JM",
        disponible=True,
        date_debut_disponibilite= datetime(2023,1,1,8,00,00),
        date_fin_disponibilite= datetime(2023,1,1,17,00,00)
    )

    with app.app_context():
        db.session.add(disponibilite)
        db.session.commit()

    with app.app_context():
        retrieved_disponibilite = Disponibilite.query.filter_by(enseignant="JM").first()

    assert retrieved_disponibilite is not None
    assert retrieved_disponibilite.disponible is True
    assert str(retrieved_disponibilite.date_debut_disponibilite) == "2023-01-01 08:00:00"
    assert str(retrieved_disponibilite.date_fin_disponibilite) == "2023-01-01 17:00:00"

    with app.app_context():
        db.session.delete(retrieved_disponibilite)
        db.session.commit()
