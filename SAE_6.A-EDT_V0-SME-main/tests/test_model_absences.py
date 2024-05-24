# Importation de nos modules et des classes nécessaires
from models.Absence import Absence
from models.Cours import Cours
from models.User import User
import pytest
from database.config import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Fonction pour créer une application Flask pour les tests
def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  db.init_app(app)

  return app

# Fixture Pytest pour configurer et détruire le contexte de l'application pour les tests
@pytest.fixture(name="app")
def app():
    app = create_app()

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

# Fonction de test pour vérifier l'initialisation de la classe Absence
def test_absence_initialization(app):
    # Test de l'initialisation de la classe Absence
    # Création d'instances de test pour les modèles associés
    user = User(username="jonas_obrun",password="jonas1234",role="ROLE_STUDENT",name="Jonas",lastname="Obrun")
    cours = Cours(start_time="2023-12-02 23:55:00",end_time="2023-12-03 01:00:00",initial_ressource="R5A05",id_group= 2)

    # Ajout des instances à la base de données de test
    with app.app_context():
        db.session.add(user)
        db.session.add(cours)
        db.session.commit()

    # Création d'une instance de test d'Absence
    absence = Absence(idEtudiant="jonas_obrun", idCour=1)

    # Ajout de l'instance Absence à la base de données de test
    with app.app_context():
        db.session.add(absence)
        db.session.commit()

    # Récupération de l'instance Absence depuis la base de données
    with app.app_context():
        retrieved_absence = Absence.query.filter_by(idEtudiant="jonas_obrun", idCour=1).first()

    # Assertions pour vérifier si l'instance Absence a été ajoutée et récupérée correctement
    assert retrieved_absence is not None
    assert retrieved_absence.idEtudiant == "jonas_obrun"
    assert retrieved_absence.idCour == 1
    assert retrieved_absence.justifiée is False

    with app.app_context():
        db.session.delete(retrieved_absence)
        db.session.delete(user)
        db.session.delete(cours)
        db.session.commit()