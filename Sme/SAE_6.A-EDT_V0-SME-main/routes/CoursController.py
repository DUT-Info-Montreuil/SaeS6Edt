# Importation des modules nécessaires de flask et flask_jwt_extended
from flask import Blueprint, jsonify, send_from_directory, request
from services.UserService import UserService
from models.User import User
from models.Cours import Cours
from functools import wraps
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity)
from services.CoursService import CoursService

# Création d'un nouveau Blueprint. C'est une façon d'organiser les routes dans Flask.
cours_bp = Blueprint('cours', __name__)

# Définition d'une route pour obtenir tous les cours. 
# Cette fonction sera appelée lorsqu'une requête GET est faite à '/courses'.
@cours_bp.route('/courses', methods=['GET'])
@jwt_required()
def get_all_courses():
    try:
        # Récupération de l'utilisateur actuel.
        current_user = get_jwt_identity()
        user : User = UserService.get_by_id(current_user)

        # Récupération de tous les cours pour cet utilisateur.
        courses = CoursService.get_all_courses(request.args, user=user)   
        print(request.args)

        # Conversion des cours en dictionnaires pour la réponse JSON.
        ressources_dict = [course.to_dict() for course in courses]
        return jsonify(ressources_dict),200
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

# Définition d'une route pour obtenir un cours spécifique par son ID. 
# Cette fonction sera appelée lorsqu'une requête GET est faite à '/course/<id>'.
@cours_bp.route('/course/<id>', methods=['GET'])
@jwt_required()
def get_course(id):
    try:
        # Récupération du cours par son ID.
        course = CoursService.get_course_by_id(id) 

        # Si le cours n'a pas été trouvé, retourne un message d'erreur.
        if not course:
            return jsonify({'error': 'Cours not found'}),404

        # Si le cours a été trouvé, le retourne.
        return jsonify(course.to_dict()),200
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

    
# Définition d'une route pour créer un cours. 
# Cette fonction sera appelée lorsqu'une requête POST est faite à '/course'.
@cours_bp.route('/course', methods=['POST'])
@jwt_required()
def create_course():
    data = request.json

    try:
        #Tentative de création du cours.
        resp, code = CoursService.create_course(data)
        #Si le code est supérieur à égal à 400, retourne un message d'erreur contenu dans resp et le code d'erreur.
        if code >= 400:
            return jsonify(resp),code
        
        #Si le code est supérieur à 200, retourne un warning contenu dans resp et le code du warning.
        #Le cours est quand même créé.
        warning_with_result = resp
        if code > 200:
            return jsonify(warning_with_result),code
        
        #Sinon, retourne le cours créé et le code 200.
        course = resp
        return jsonify(course.to_dict()),code
    except Exception as e:
         # Si une autre erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403
    
# Définition d'une route pour supprimer un cours. 
# Cette fonction sera appelée lorsqu'une requête DELETE est faite à '/course/<id>', où <id> est l'id du cours à supprimé.
@cours_bp.route('/course/<id>', methods=['DELETE'])
@jwt_required()
def delete_course(id):
    try: 
        #Tentative de suppression du cours et assignation du cours et assignation du cours à course.
        course = CoursService.delete_course(id)

        #Retourne le cours supprimé et le code 200.
        return jsonify(course.to_dict()),200
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403
    

# Définition d'une route pour mettre à jour un cours.
# Cette fonction sera appelée lorsqu'une requête PUT est faite à '/course/<id>', où <id> est l'id du cours à mettre à jour.
@cours_bp.route('/course/<id>', methods=['PUT'])
@jwt_required()
def update_course(id):
    #Récupération des données de la requête.
    data = request.json
    isInDraft = data['isInDraft']
    #Suppression de l'id dans les données.
    if 'id' in data:
        del data['id']
    try:
        #Tentative de mise à jour du cours.
        resp, code = CoursService.update_course(id, **data)
        #Si le code est supérieur ou égal à 400, retourne un message d'erreur contenu dans resp et le code d'erreur.
        if code >= 400:
            return jsonify(resp),code
        #Si le code est supérieur à 200, retourne un warning contenu dans resp et le code du warning.
        #Le cours est quand même mis à jour.
        warning_with_result = resp
        if code > 200:
            return jsonify(warning_with_result),code
        #Sinon, retourne le cours mis à jour et le code 200.
        course = resp
        return jsonify(course.to_dict()),200
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403
    
# Définition d'une route pour mettre à jour un cours.
# Cette fonction sera appelée lorsqu'une requête PUT est faite à '/courses/publish'.
@cours_bp.route('/courses/publish', methods=['PUT'])
@jwt_required()
def publish_all():

    try:
        #Publication des cours.
        courses = CoursService.publish()
        courses_dict = [course.to_dict() for course in courses]
        return jsonify(courses_dict),200
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

# Définition d'une route pour annuler les cours non publiés.
# Cette fonction sera appelée lorsqu'une requête DELETE est faite à '/courses/cancel'.
@cours_bp.route('/courses/cancel', methods=['DELETE'])
@jwt_required()
def cancel_all():

    try:
        #Annulation des cours.
        courses = CoursService.cancel()
        courses_dict = [course.to_dict() for course in courses]
        return jsonify(courses_dict),200
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403   


# Définition d'une route pour coller des cours copiés contenus dans data.
# Cette fonction sera appelée lorsqu'une requête POST est faite à '/courses/paste'.
@cours_bp.route('/courses/paste', methods=['POST']) 
@jwt_required()
def paste_all():
    data = request.json

    try:
        #Collage des cours.
        courses = CoursService.paste(**data)
        if isinstance(courses[0], Cours):
            courses_dict = [course.to_dict() for course in courses]
            return jsonify(courses_dict),200
        else:
            return jsonify(courses[0]),409
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

# Définition d'une route pour dupliquer un cour contenu dans data afin de l'assigner à d'autres groupe.
# Cette fonction sera appelée lorsqu'une requête POST est faite à '/courses/duplicate'.
@cours_bp.route('/courses/duplicate', methods=['POST'])
@jwt_required() 
def duplicate_all():
    data = request.json

    try:
        #Duplication du cour.
        courses = CoursService.duplicate(**data)
        courses_dict = [course.to_dict() for course in courses]
        return jsonify(courses_dict),200
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403


# Définition d'une route pour obtenir les statistiques d'un enseignant.
# Cette fonction sera appelée lorsqu'une requête GET est faite à '/courses/stats/<id_teacher>', où <id_teacher> est l'id de l'enseignant.
@cours_bp.route('/courses/stats/<id_teacher>', methods=['GET'])
@jwt_required()
def get_stats_teacher(id_teacher):
    try:
        #Récupération des cours de l'enseignant.
        courses = CoursService.get_courses_by_teacher(id_teacher)
        
        #Récupération des noms des ressources.
        name_courses = {course.initial_ressource for course in courses}
        stats = []
        total_minutes = 0
        
        #Calcul du nombre d'heures et de minutes pour chaque ressource.
        for nc in name_courses:
            duration_nc_minutes = 0
            
            for course in courses:
                if nc == course.initial_ressource:
                    duration = course.end_time - course.start_time
                    minutes = duration.total_seconds() / 60
                    
                    duration_nc_minutes += minutes
                    total_minutes += minutes
                    
            hours, minutes = divmod(duration_nc_minutes, 60)
            stats.append({'name': nc, 'hours': hours, 'minutes': minutes})
        
        #Calcul du total d'heures et de minutes de cours du professeur.
        total_hours, total_minutes = divmod(total_minutes, 60)
        stats.append({'name': 'total', 'hours': total_hours, 'minutes': total_minutes})
        
        #Retourne les statistiques et le code 200.
        return jsonify(stats),200
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403
