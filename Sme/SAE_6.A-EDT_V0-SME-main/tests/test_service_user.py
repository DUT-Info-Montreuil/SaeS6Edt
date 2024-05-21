import pytest
from database.config import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.User import User
from services.UserService import UserService
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

# Tests unitaires pour créer un utilisateur
def test_create_user(app):
    # Test the creation of a user
    with app.app_context():
        # Create a test user
        user_data = {
            'username': 'test_user',
            'password': 'password123',
            'name': 'John',
            'lastname': 'Doe',
            'role': 'user'
        }
        user = UserService.create_user(**user_data)

        retrieved_user = UserService.get_by_id(user.id)

        assert retrieved_user is not None
        assert retrieved_user.username == 'test_user'
        assert retrieved_user.name == 'John'
        assert retrieved_user.lastname == 'Doe'
        assert retrieved_user.role == 'user'

        UserService.delete_user(retrieved_user)

# Tests unitaires pour récupérer tous les users
def test_get_all_users(app):
    with app.app_context():
        user1 = UserService.create_user('user1', 'pass1', 'User1', 'Last1', 'user')
        user2 = UserService.create_user('user2', 'pass2', 'User2', 'Last2', 'admin')

        all_users = UserService.get_all_users()

        assert len(all_users) == 2
        assert user1 in all_users
        assert user2 in all_users

        UserService.delete_user(user1)
        UserService.delete_user(user2)

# Tests unitaires pour récupérer un user par son nom d'utilisateur
def test_get_by_username(app):
    with app.app_context():
        user_data = {
            'username': 'test_user',
            'password': 'password123',
            'name': 'John',
            'lastname': 'Doe',
            'role': 'user'
        }
        user = UserService.create_user(**user_data)

        retrieved_user = UserService.get_by_username('test_user')

        assert retrieved_user is not None
        assert retrieved_user.username == 'test_user'
        assert retrieved_user.name == 'John'
        assert retrieved_user.lastname == 'Doe'
        assert retrieved_user.role == 'user'

        UserService.delete_user(retrieved_user)
