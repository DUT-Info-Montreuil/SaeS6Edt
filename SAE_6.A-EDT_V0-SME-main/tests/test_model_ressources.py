
import pytest
from database.config import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.Ressources import Ressources



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

# Fonction de test pour l'initialisation de la classe Ressources
def test_ressources_initialization(app):
    # Test the initialization of the Ressources class

    # Create a test instance
    ressource = Ressources(
        name="Qualité dev",
        initial="R5A05",
        id_promo=1
    )

    # Add the instance to the test database
    with app.app_context():
        db.session.add(ressource)
        db.session.commit()

    # Retrieve the instance from the database
    with app.app_context():
        retrieved_ressource = Ressources.query.filter_by(initial="R5A05").first()

    # Perform assertions to check if the instance was added and retrieved correctly
    assert retrieved_ressource is not None
    assert retrieved_ressource.name == "Qualité dev"
    assert retrieved_ressource.id_promo == 1

    # Clean up the database (optional)
    with app.app_context():
        db.session.delete(retrieved_ressource)
        db.session.commit()