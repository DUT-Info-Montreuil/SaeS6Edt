# tests/test_PromotionService.py
import pytest
from database.config import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from services.PromotionService import PromotionService

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

# Tests unitaires pour créer unee promo
def test_create_promo(app):
    # Test the creation of a promotion
    with app.app_context():
        promo_data = {
            'name': 'Class of 2023',
            'niveau': 'Bachelor',
            'id_resp': 1,
        }
        promo = PromotionService.create_promo(promo_data)

        assert promo is not None
        assert promo.name == 'Class of 2023'
        assert promo.niveau == 'Bachelor'
        assert promo.id_resp == 1

        PromotionService.delete_promo(promo.id_promo)

# Tests unitaires pour récupérer toutes les promos
def test_get_all_promos(app):
    with app.app_context():
        promos = PromotionService.get_all_promos()

        assert isinstance(promos, list)
        assert len(promos) >= 0  

# Tests unitaires pour récupérer une promo avec un id
def test_get_promo_by_id(app):
    # Test retrieving a promotion by ID
    with app.app_context():
        # Create a test promotion
        promo_data = {
            'name': 'Class of 2024',
            'niveau': 'Master',
            'id_resp': 2,
        }
        promo = PromotionService.create_promo(promo_data)

        # Get the promotion by ID
        retrieved_promo = PromotionService.get_promo_by_id(promo.id_promo)

        assert retrieved_promo is not None
        assert retrieved_promo.name == 'Class of 2024'
        assert retrieved_promo.niveau == 'Master'
        assert retrieved_promo.id_resp == 2

        PromotionService.delete_promo(promo.id_promo)

# Tests unitaires pour mettre à jour une promo
def test_update_promo(app):
    # Test updating a promotion
    with app.app_context():
        # Create a test promotion
        promo_data = {
            'name': 'Class of 2025',
            'niveau': 'Ph.D.',
            'id_resp': 3,
        }
        promo = PromotionService.create_promo(promo_data)

        # Update the promotion
        updated_promo = PromotionService.update_promo(promo.id_promo, 'Class of 2026', 'Postdoc', 4)

        assert updated_promo is not None
        assert updated_promo.name == 'Class of 2026'
        assert updated_promo.niveau == 'Postdoc'
        assert updated_promo.id_resp == 4

        PromotionService.delete_promo(updated_promo.id_promo)

# Tests unitaires pour supprimer une promo
def test_delete_promo(app):
    # Test deleting a promotion
    with app.app_context():
        # Create a test promotion
        promo_data = {
            'name': 'Class of 2027',
            'niveau': 'Undergraduate',
            'id_resp': 5,
        }
        promo = PromotionService.create_promo(promo_data)

        # Delete the promotion
        deleted_promo = PromotionService.delete_promo(promo.id_promo)

        assert deleted_promo is not None
        assert deleted_promo.id_promo == promo.id_promo

        retrieved_promo = PromotionService.get_promo_by_id(promo.id_promo)
        assert retrieved_promo is None
