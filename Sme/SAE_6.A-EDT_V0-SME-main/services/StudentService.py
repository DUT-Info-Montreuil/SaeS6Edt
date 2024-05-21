from database.config import db
from models.Student import Student
from services.UserGroupeService import UserGroupeService
from services.GroupeService import GroupeService
from models.relations import user_groupe
# import ast
# import json
# import os

class StudentService:
    
    def __init__(self):
        self.group_service = GroupeService()
    
    # Récupère tous les étudiants de la base de données
    @staticmethod
    def get_all_students():
        return Student.query.all()

    # Crée un nouvel étudiant avec les données fournies
    @staticmethod
    def create_student(data):
        student = Student(**data)
        db.session.add(student)
        db.session.commit()
        return student

    # Récupère un étudiant par son identifiant
    @staticmethod
    def get_by_id(id):
        return Student.query.filter_by(id_student=id).first()

    # Supprime un étudiant de la base de données par son identifiant
    @staticmethod
    def delete_student(id):
        UserGroupeService.delete_user_groupe(id)
        
        student = Student.query.filter_by(id_student=id).first()
        db.session.delete(student)
        db.session.commit()
        return student

    # Met à jour les informations d'un étudiant avec les valeurs fournies
    @staticmethod
    def update_student(id, name, lastname):
        student = Student.query.filter_by(id_student=id).first()
        student.name = name
        student.lastname = lastname
        db.session.commit()
        return student
    
    # Récupère tous les étudiants associés à un groupe et à ses sous-groupes
    @staticmethod
    def get_students_by_group(idGroupe):
        group_service = GroupeService()
        groups = group_service.get_tree(idGroupe)

        students = []

        for group in groups:
            students_of_group = UserGroupeService.get_etudiants_for_groupe(group.id)
            
            if students_of_group:
                students.append(students_of_group)

        return students


