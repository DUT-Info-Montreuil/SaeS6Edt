# Importation des modules nécessaires
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity)
from services.UserGroupeService import UserGroupeService

# Création d'un blueprint pour les routes liées aux groupes d'utilisateurs
usergroupe_bp = Blueprint('usergroupe', __name__)

# Route pour ajouter un utilisateur à un groupe
@usergroupe_bp.route('/usergroupe/addGroupeEtudiant', methods=['POST'])
@jwt_required()
def add_user_to_group():
    # Récupération des données du corps de la requête
    idStudent = request.json["idStudent"]
    idGroupe = request.json["idGroupe"]
    
    try:
        # Appel du service pour ajouter l'utilisateur au groupe
        UserGroupeService.add_user_to_group(idStudent, idGroupe)
        # Si tout se passe bien, on renvoie un message de succès
        return jsonify({"message": "Utilisateur ajouté au groupe avec succès"}), 200
    except Exception as e:
        # En cas d'erreur, on renvoie le message d'erreur
        return jsonify({'error': str(e)}), 403

# Route pour récupérer un groupe d'un étudiant
@usergroupe_bp.route('/usergroupe/groupeEtudiant/<idGroupe>/<idStudent>', methods=['GET'])
@jwt_required()
def get_groupe_etudiant(idStudent,idGroupe):
    try:
        # Appel du service pour récupérer le groupe de l'étudiant
        groupe_etudiant = UserGroupeService.get_groupe_etudiant(idStudent,idGroupe)
        if not groupe_etudiant:
            # Si le groupe n'est pas trouvé, on renvoie un message d'erreur
            return jsonify({'error': 'Groupe not found'}),403

        # Si tout se passe bien, on renvoie le groupe
        return jsonify(groupe_etudiant.to_dict()),200
    except Exception as e:
        # En cas d'erreur, on renvoie le message d'erreur
        return jsonify({'error': str(e)}),403

# Route pour récupérer un étudiant par groupe
@usergroupe_bp.route('/usergroupe/etudiantGroupe/<idGroupe>/<idStudent>', methods=['GET'])
@jwt_required()
def get_etudiant_by_groupe(idStudent,idGroupe):
    try:
        # Appel du service pour récupérer l'étudiant du groupe
        groupe_etudiant = UserGroupeService.get_etudiant_by_groupe(idStudent,idGroupe)
        if not groupe_etudiant:
            # Si l'étudiant n'est pas trouvé, on renvoie un message d'erreur
            return jsonify({'error': 'Etudiant not found'}),403

        # Si tout se passe bien, on renvoie l'étudiant
        return jsonify(groupe_etudiant.to_dict()),200
    except Exception as e:
        # En cas d'erreur, on renvoie le message d'erreur
        return jsonify({'error': str(e)}),403

# Route pour supprimer un utilisateur d'un groupe
@usergroupe_bp.route('/usergroupe/delete/<idStudent>', methods=['DELETE'])
@jwt_required()
def delete_user_groupe(idStudent):
    try:
        # Appel du service pour supprimer l'utilisateur du groupe
        UserGroupeService.delete_user_groupe(idStudent)
        # Si tout se passe bien, on renvoie un message de succès
        return jsonify({"message": "Utilisateur supprimé du groupe avec succès"}), 200
    except Exception as e:
        # En cas d'erreur, on renvoie le message d'erreur
        return jsonify({'error': str(e)}), 403

# Route pour récupérer les étudiants pour un groupe
@usergroupe_bp.route('/usergroupe/groupe/<idGroupe>', methods=['GET'])
@jwt_required()
def get_etudiants_for_groupe(idGroupe):
    try:
        # Appel du service pour récupérer les étudiants du groupe
        etudiants = UserGroupeService.get_etudiants_for_groupe(idGroupe)
        if not etudiants:
            # Si aucun étudiant n'est trouvé, on renvoie un message d'erreur
            return jsonify({'error': 'Etudiants not found'}),201

        # Si tout se passe bien, on renvoie la liste des étudiants
        return jsonify(etudiants),200
    except Exception as e:
        # En cas d'erreur, on renvoie le message d'erreur
        return jsonify({'error': str(e)}),403

# Route pour récupérer les groupes pour un étudiant
@usergroupe_bp.route('/usergroupe/groupForStudent/<idEtudiant>', methods=['GET'])
@jwt_required()
def get_groupes_for_student(idEtudiant):
    try:
        # Appel du service pour récupérer les groupes de l'étudiant
        groupes = UserGroupeService.get_groupes_for_student(idEtudiant)
        if not groupes:
            # Si aucun groupe n'est trouvé, on renvoie un message d'erreur
            return jsonify({'error': 'Groupe not found'}),201

        # Si tout se passe bien, on renvoie la liste des groupes
        return jsonify(groupes),200
    except Exception as e:
        # En cas d'erreur, on renvoie le message d'erreur
        return jsonify({'error': str(e)}),403

# Route pour mettre à jour le groupe d'un étudiant
@usergroupe_bp.route('/usergroupe/modify/<idStudent>/<newIdGroupe>/<idGroupe>', methods=['PUT'])
@jwt_required()
def update_student_group(idStudent, newIdGroupe, idGroupe):
    try:
        # Appel du service pour mettre à jour le groupe de l'étudiant
        result = UserGroupeService.update_student_group(idStudent, newIdGroupe, idGroupe)

        if "error" in result:
            # Si une erreur est renvoyée par le service, on la renvoie
            return jsonify({'error': result["error"]}), 403

        # Si tout se passe bien, on renvoie un message de succès
        return jsonify({'message': result["message"]}), 200
    except Exception as e:
        # En cas d'erreur, on renvoie le message d'erreur
        return jsonify({'error': str(e)}), 403

# Route pour migrer une promotion
@usergroupe_bp.route('/usergroupe/migrate', methods=['POST'])
@jwt_required()
def migrate_promo() :
    try:
        # Récupération des données du corps de la requête
        data = request.json
        
        # Appel du service pour mettre à jour la promotion des étudiants
        result = UserGroupeService.update_promo_etudiants(**data)
        
        if "error" in result:
            # Si une erreur est renvoyée par le service, on la renvoie
            return jsonify({'error': result}), 403

        # Si tout se passe bien, on renvoie un message de succès
        return jsonify({'message': result}), 200
    
    except Exception as e:
        # En cas d'erreur, on renvoie le message d'erreur
        return jsonify({'error': str(e)}), 403

