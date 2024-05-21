from database.config import db
from models.User import User
# import ast
# import json
# import os

class UserService:
    
    # Récupère tous les utilisateurs de la base de données.
    @staticmethod
    def get_all_users():
        # :return: Liste d'objets User
        return User.query.all()
    
    # Crée un nouvel utilisateur dans la base de données
    @staticmethod
    def create_user(username, password, name, lastname, role):
        user = User(username=username, password=password, role=role, name=name, lastname=lastname)
        db.session.add(user)
        db.session.commit()
        return user
    
    # Vérifie si un utilisateur avec l'ID donné existe
    @staticmethod
    def is_exist(id):
        return User.query.get(id) is not None
    
    # Récupère un utilisateur par son ID
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)
    
    # Récupère un utilisateur par son nom d'utilisateur
    @staticmethod
    def get_by_username(username):

        user = User.query.filter_by(username=username).first()
        return user

    # Supprime un utilisateur de la base de données
    @staticmethod
    def delete_user(user):
        db.session.delete(user)
        db.session.commit()

    # Met à jour les informations de prénom et nom de famille d'un utilisateur
    @staticmethod
    def update_user(id, name, lastname):
        user = User.query.get(id)
        user.name = name
        user.lastname = lastname
        db.session.commit()
        return user
    
    @staticmethod
    def get_user_role_by_id(user_id):
        user = User.query.get(user_id)
        if user:
            return user.role
        return None