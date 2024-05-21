import pytest
from flask import Flask
from models.Salle import Salle
from flask_sqlalchemy import SQLAlchemy
from services.SalleService import SalleService
from database.config import db

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

# Tests unitaires pour créer une salle
def test_create_salle(app):
    with app.app_context():
        # Create a test instance
        salle_data = {
            'name': 'A2-05',
            'ordi': 25,
            'tableauNumerique': 1,
            'videoProj': 1
        }

        salle = SalleService.create_salle(**salle_data)

        # Retrieve the instance from the database
        retrieved_salle = SalleService.get_salle_by_name('A2-05')

        # Perform assertions to check if the instance was added and retrieved correctly
        assert retrieved_salle is not None
        assert retrieved_salle.ordi == 25
        assert retrieved_salle.tableauNumerique == 1
        assert retrieved_salle.videoProjecteur == 1

        # Clean up the database
        db.session.delete(retrieved_salle)
        db.session.commit()

# Tests unitaires pour savoir si une salle étant créée existe bien
def test_isExist(app):
    with app.app_context():
        salle_data = {'name': 'A2-05', 'ordi': 25, 'tableauNumerique': 1, 'videoProj': 1}
        SalleService.create_salle(**salle_data)

        #Check if the salle exists
        salle_exists = SalleService.isExist('A2-05')

        assert salle_exists is True

        salle = SalleService.get_salle_by_name('A2-05')
        db.session.delete(salle)
        db.session.commit()

# Tests unitaires pour supprimer une salle
def test_delete_salle(app):
    with app.app_context():
        salle_data = {'name': 'A2-05', 'ordi': 25, 'tableauNumerique': 1, 'videoProj': 1}
        SalleService.create_salle(**salle_data)

        deleted_salle = SalleService.delete_salle('A2-05')

        assert deleted_salle is not None
        assert deleted_salle.nom == 'A2-05'

        salle_exists = SalleService.isExist('A2-05')
        assert salle_exists is False

# Tests unitaires pour récupérer une salle par son nom
def test_get_salle_by_name(app):
    with app.app_context():
        salle_data = {'name': 'A2-05', 'ordi': 25, 'tableauNumerique': 1, 'videoProj': 1}
        SalleService.create_salle(**salle_data)

        retrieved_salle = SalleService.get_salle_by_name('A2-05')

        assert retrieved_salle is not None
        assert retrieved_salle.nom == 'A2-05'

        db.session.delete(retrieved_salle)
        db.session.commit()
