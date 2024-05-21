import pytest
from flask import Flask
from database.config import db
from services.GroupeService import GroupeService
from models.Groupe import Groupe
import warnings

# Suppress SQLAlchemy Legacy API Warning
warnings.filterwarnings("ignore", category=DeprecationWarning, module="sqlalchemy.orm.query.*")

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

# Tests unitaires pour la création de GroupeService
def test_create_groupe(app):
    with app.app_context():
        # Create a test groupe
        groupe_data = {'name': 'Test Groupe', 'id_group_parent': None}
        groupe = GroupeService.create_groupe(groupe_data)

        # Check if the groupe was created
        assert groupe.id is not None
        assert groupe.name == 'Test Groupe'

        # Clean up
        GroupeService.delete_groupe(groupe.id)

# Tests unitaires pour la récupération de tous les groupes
def test_get_all_groupes(app):
    with app.app_context():
        # Create some test groupes
        groupe_data_1 = {'name': 'Groupe 1', 'id_group_parent': None}
        groupe_data_2 = {'name': 'Groupe 2', 'id_group_parent': None}
        GroupeService.create_groupe(groupe_data_1)
        GroupeService.create_groupe(groupe_data_2)

        # Get all groupes
        groupes = GroupeService.get_all_groupes()

        # Check if the correct number of groupes is returned
        assert len(groupes) == 2

        # Clean up
        GroupeService.delete_groupe(groupes[0].id)
        GroupeService.delete_groupe(groupes[1].id)

# Tests unitaires pour récupérer un groupe via un id 
def test_get_groupe_by_id(app):
    with app.app_context():
        # Create a test groupe
        groupe_data = {'name': 'Test Groupe', 'id_group_parent': None}
        groupe = GroupeService.create_groupe(groupe_data)

        # Get the groupe by ID
        retrieved_groupe = GroupeService.get_groupe_by_id(groupe.id)

        # Check if the correct groupe is retrieved
        assert retrieved_groupe.id == groupe.id
        assert retrieved_groupe.name == groupe.name

        # Clean up
        GroupeService.delete_groupe(groupe.id)

# Tests unitaires pour mettre à jour un groupe
def test_update_groupe(app):
    with app.app_context():
        # Create a test groupe
        groupe_data = {'name': 'Test Groupe', 'id_group_parent': None}
        groupe = GroupeService.create_groupe(groupe_data)

        # Update the groupe
        updated_groupe = GroupeService.update_groupe(groupe.id, 'Updated Groupe')

        # Check if the groupe was updated
        assert updated_groupe.name == 'Updated Groupe'

        # Clean up
        GroupeService.delete_groupe(updated_groupe.id)

# Tests unitaires pour supprimer un groupe
def test_delete_groupe(app):
    with app.app_context():
        # Create a test groupe
        groupe_data = {'name': 'Test Groupe', 'id_group_parent': None}
        groupe = GroupeService.create_groupe(groupe_data)

        # Delete the groupe
        deleted_groupe = GroupeService.delete_groupe(groupe.id)

        # Check if the groupe was deleted
        assert deleted_groupe is not None

        # Try to retrieve the deleted groupe (should be None)
        retrieved_groupe = GroupeService.get_groupe_by_id(groupe.id)
        assert retrieved_groupe is None
