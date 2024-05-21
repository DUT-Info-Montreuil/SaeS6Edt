from xml.dom import NotFoundErr
from flask import Blueprint, jsonify, send_from_directory, request
from services.GroupeService import GroupeService
from services.StudentService import StudentService
from functools import wraps
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity)
from flask import abort

from services.UserGroupeService import UserGroupeService

# Création d'un nouveau Blueprint. C'est une façon d'organiser les routes dans Flask.
student_bp = Blueprint('student', __name__)

# Définition d'une route pour obtenir tous les étudiants. 
# Cette fonction sera appelée lorsqu'une requête GET est faite à '/students'.
@student_bp.route('/students', methods=['GET'])
@jwt_required()
def get_all_students():
    try:
        # Récupération de tous les étudiants.
        students = StudentService.get_all_students()
        students_dict = [student.to_dict() for student in students]
        return jsonify(students_dict),200
    except Exception as e:
        # En cas d'erreur, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

# Définition d'une route pour obtenir un étudiant spécifique par son ID. 
# Cette fonction sera appelée lorsqu'une requête GET est faite à '/student/<id>'.
@student_bp.route('/student/<id>', methods=['GET'])
@jwt_required()
def get_by_student(id):
    try:
        # Récupération de l'étudiant par son ID.
        student = StudentService.get_by_id(id)
        if not student:
            return jsonify({'error': 'Student not found'}),403
        return jsonify(student.to_dict()),200
    except Exception as e:
        # En cas d'erreur, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

# Définition d'une route pour créer un nouvel étudiant. 
# Cette fonction sera appelée lorsqu'une requête POST est faite à '/student'.
@student_bp.route('/student', methods=['POST'])
@jwt_required()
def create_student():
    # Récupération des données de la requête.
    data = request.json
    try:
        # Création de l'étudiant avec les données fournies.
        student = StudentService.create_student(data)
        return jsonify(student.to_dict()), 200
    except Exception as e:
        # En cas d'erreur, retourne un message d'erreur.
        abort(500, {'error': str(e)})

# Définition d'une route pour supprimer un étudiant spécifique par son ID. 
# Cette fonction sera appelée lorsqu'une requête DELETE est faite à '/student/<id>'.
@student_bp.route('/student/<id>', methods=['DELETE'])
@jwt_required()
def delete_student(id):
    try:
        # Suppression de l'étudiant par son ID.
        student = StudentService.delete_student(id)
        if not student:
            return jsonify({'error': 'Student not found'}),403
        return jsonify(student.to_dict()),200
    except Exception as e:
        # En cas d'erreur, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

# Définition d'une route pour mettre à jour un étudiant spécifique par son ID. 
# Cette fonction sera appelée lorsqu'une requête PUT est faite à '/student/<id>'.
@student_bp.route('/student/<id>', methods=['PUT'])
@jwt_required()
def update_student(id):
    # Récupération des données de la requête.
    data = request.json
    if 'id' in data:
        del data['id']
    try:
        # Mise à jour de l'étudiant avec les données fournies.
        student = StudentService.update_student(id=id, **data)
        if not student:
            return jsonify({'error': 'Student not found'}),403
        return jsonify(student.to_dict()),200
    except Exception as e:
        # En cas d'erreur, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

# Définition d'une route pour obtenir tous les étudiants d'un groupe spécifique par son ID. 
# Cette fonction sera appelée lorsqu'une requête GET est faite à '/students/groupe/<idGroupe>'.
@student_bp.route('/students/groupe/<idGroupe>', methods=['GET'])
@jwt_required()
def get_all_students_by_group(idGroupe):
    try:
        # Récupération de tous les groupes par leur ID.
        groups = GroupeService.get_tree(idGroupe)
        if not groups:
            return jsonify({'error': 'Students not found'}),403
        students = []
        for group in groups:
            # Récupération de tous les étudiants pour chaque groupe.
            students_of_group = UserGroupeService.get_etudiants_for_groupe(group)
            if students_of_group:
                students.append(students_of_group)
        return jsonify(students),200
    except Exception as e:
        # En cas d'erreur, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403