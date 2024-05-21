import pytest
from database.config import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.Salle import Salle

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


# Fonction de test pour l'initialisation de la classe Salle
def test_salle_initialization(app):
    # Test the initialization of the Salle class
    # Create a test instance
    salle = Salle(
        name="A2-05",
        ordi=25,
        tableauNumerique=1,
        videoProjecteur=1
    )

    # Add the instance to the test database
    with app.app_context():
        db.session.add(salle)
        db.session.commit()

    # Retrieve the instance from the database
    with app.app_context():
        retrieved_salle = Salle.query.filter_by(nom="A2-05").first()

    # Assertions pour vérifier si l'instance a été ajoutée et récupérée correctement
    assert retrieved_salle is not None
    assert retrieved_salle.ordi == 25
    assert retrieved_salle.tableauNumerique == 1
    assert retrieved_salle.videoProjecteur == 1

    with app.app_context():
        db.session.delete(retrieved_salle)
        db.session.commit()