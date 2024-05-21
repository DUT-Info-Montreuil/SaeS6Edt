import pytest
from flask import Flask
from database.config import db
from models.Groupe import Groupe
import warnings

# Suppression de l'avertissement sur l'API obsolète de SQLAlchemy
warnings.filterwarnings("ignore", category=DeprecationWarning, module="sqlalchemy.orm.query.*")

# Fonction pour créer une application Flask pour les tests
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

# Fonction de test pour créer un groupe
def test_create_groupe(app):
    with app.app_context():
        # Create a test groupe
        groupe_data = {'name': 'Test Groupe', 'id_group_parent': None}
        groupe = Groupe(**groupe_data)

        # Commit the groupe to the database
        db.session.add(groupe)
        db.session.commit()

        # Check si le groupe était créé
        assert groupe.id is not None
        assert groupe.name == 'Test Groupe'
        assert groupe.id_group_parent is None

# Fonction de test pour créer un groupe avec un parent
def test_create_groupe_with_parent(app):
    with app.app_context():
        # Create a parent groupe
        parent_data = {'name': 'Parent Groupe', 'id_group_parent': None}
        parent = Groupe(**parent_data)

        # Commit the parent to the database
        db.session.add(parent)
        db.session.commit()

        # Create a child groupe with the parent
        child_data = {'name': 'Child Groupe', 'id_group_parent': parent.id}
        child = Groupe(**child_data)

        # Commit the child to the database
        db.session.add(child)
        db.session.commit()

        # Check si les deux groupe ont été créé
        assert parent.id is not None
        assert child.id is not None
        assert child.id_group_parent == parent.id

# Fonction de test pour créer un groupe avec un parent inexistant
def test_create_groupe_with_nonexistent_parent(app):
    with app.app_context():
        # Attempt to create a groupe with a nonexistent parent
        groupe_data = {'name': 'Test Groupe', 'id_group_parent': 999}
        with pytest.raises(Exception, match="Groupe parent does not exist"):
            groupe = Groupe(**groupe_data)
            db.session.add(groupe)
            db.session.commit()

# Fonction de test pour vérifier la méthode to_dict
def test_to_dict_method(app):
    with app.app_context():
        # Create a test groupe
        groupe_data = {'name': 'Test Groupe', 'id_group_parent': None}
        groupe = Groupe(**groupe_data)

        # Commit the groupe to the database
        db.session.add(groupe)
        db.session.commit()

        # Convert the groupe to a dictionary
        groupe_dict = groupe.to_dict()

        # Check if the dictionary has the expected keys and values
        assert groupe_dict['id'] == groupe.id
        assert groupe_dict['name'] == groupe.name
        assert groupe_dict['id_group_parent'] == groupe.id_group_parent

