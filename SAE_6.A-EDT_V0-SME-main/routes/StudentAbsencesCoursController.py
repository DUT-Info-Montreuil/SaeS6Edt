from flask import Blueprint, jsonify, request
from services.StudentAbsencesCoursService import StudentAbsencesCoursService
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity)

# Création d'un nouveau Blueprint. C'est une façon d'organiser les routes dans Flask.
studentAbsences_bp = Blueprint('studentAbsencesCours', __name__)

# Définition d'une route pour ajouter une absence d'un student à un cours
# Cette fonction sera appelée lorsqu'une requête POST est faite à '/studentAbsenceCours'. 
@studentAbsences_bp.route('/studentAbsenceCours', methods=['POST'])
@jwt_required()
def add_student_absence_to_cours():

    idStudent = request.json["id_student"]
    idCours = request.json["id_cours"]
    
    try:
        # Ajouter une absence d'un student à un cours
        studentsAbsenceToCours = StudentAbsencesCoursService.add_absence_to_cours(idStudent,idCours)
        # Retourner l'absence d'un student à un cours
        return jsonify(studentAbsences_bp.to_dict()),200
    except Exception as e:
        # En cas d'erreur, annulez la transaction et renvoyez un message d'erreur
        # db.session.rollback()
        return jsonify({'error': str(e)}),403

# Définition d'une route pour récuperer toutes les absences d'un student à un cours
# Cette fonction sera appelée lorsqu'une requête GET est faite à '/studentAbsenceCours/getStudentByCours/<idCours>/<idStudent>'.
@studentAbsences_bp.route('/studentAbsenceCours/getStudentByCours/<idCours>/<idStudent>', methods=['GET'])
@jwt_required()
def get_student_absences_by_cours(idCours,idStudent):
    
    try:
        # Récuperer les absences d'un student à un cours
        studentsAbsenceToCours = StudentAbsencesCoursService.get_student_absences_by_cours(idCours,idStudent)
        # Retournez les absences d'un student à un cours
        return jsonify(studentsAbsenceToCours.to_dict()),200
    except Exception as e:
        # En cas d'erreur, annulez la transaction et renvoyez un message d'erreur
        # db.session.rollback()
        return jsonify({'error': str(e)}),403


# Définition d'une route pour récuperer tous les cours d'un student
# Cette fonction sera appelée lorsqu'une requête GET est faite à '/studentAbsenceCours/getCoursByStudent/<idStudent>/<idCours>'.
@studentAbsences_bp.route('/studentAbsenceCours/getCoursByStudent/<idStudent>/<idCours>', methods=['GET'])
@jwt_required()
def get_cours_by_student_absences(idCours,idStudent):
    
    try:
        # Récuperer et retournez les cours d'un student
        studentsAbsenceToCours = StudentAbsencesCoursService.get_cours_by_student_absences(idCours,idStudent)

        return jsonify(studentsAbsenceToCours.to_dict()),200
    except Exception as e:
        # En cas d'erreur, annulez la transaction et renvoyez un message d'erreur
        # db.session.rollback()
        return jsonify({'error': str(e)}),403

# Définition d'une route pour supprimer l'absence d'un student pour un cours spécifique
# Cette fonction sera appelée lorsqu'une requête DELETE est faite à "/studentAbsenceCours/delete/<idStudent>/<idCours>
@studentAbsences_bp.route('/studentAbsenceCours/delete/<idStudent>/<idCours>', methods=['DELETE'])
@jwt_required()
def delete_absences_cours(idStudent,idCours):
    
    try:
        # Supprimer l'absence d'un student pour un cours spécifique
        studentsAbsenceToCours = StudentAbsencesCoursService.delete_absences_cours(idStudent,idCours)
        # Si l'absence n'existe pas, renvoyez une erreur 403
        if not studentsAbsenceToCours:
            return jsonify({'error': 'Student and Cours not found'}),403
        # Retournez l'absence d'un student pour un cours spécifique
        return jsonify(studentsAbsenceToCours.to_dict()),200
    except Exception as e:
        # En cas d'erreur, annulez la transaction et renvoyez un message d'erreur
        # db.session.rollback()
        return jsonify({'error': str(e)}),403

