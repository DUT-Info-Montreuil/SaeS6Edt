from database.config import db
from models.Teacher import Teacher
from services.UserService import UserService

# import ast
# import json
# import os

class TeacherService:
    
    # Récupère tous les enseignants de la base de données
    @staticmethod
    def get_all_teachers():
        return Teacher.query.all()

    # Crée un nouvel enseignant avec les données fournies
    @staticmethod
    def create_teacher(data):
        teacher = Teacher(**data)
        db.session.add(teacher)
        db.session.commit()

        return teacher
    
    # Récupère un enseignant par son identifiant
    @staticmethod
    def get_by_id(id):
        return Teacher.query.filter_by(id_teacher=id).first()
    
    # Récupère un enseignant par son identifiant utilisateur
    @staticmethod
    def get_by_user_id(id):
        return Teacher.query.filter_by(id_user=id).first()
    
    # Supprime un enseignant par son identifiant
    @staticmethod
    def delete_teacher(id):
        teacher = Teacher.query.filter_by(id_teacher=id).first()
        db.session.delete(teacher)
        db.session.commit()
        return teacher
    
    # Met à jour les informations d'un enseignant avec les valeurs fournies
    @staticmethod
    def update_teacher(id, name: str, lastname: str,activated: bool, **kwargs):
        teacher = Teacher.query.filter_by(id_teacher=id).first()
        teacher.name = name
        teacher.lastname = lastname
        teacher.activated = activated
        # teacher.role = role

        db.session.commit()
        return teacher


