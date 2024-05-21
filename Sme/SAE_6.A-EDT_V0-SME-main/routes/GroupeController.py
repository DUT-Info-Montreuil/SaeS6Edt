from xml.dom import NotFoundErr
from flask import Blueprint, jsonify, send_from_directory, request
from services.GroupeService import GroupeService
from models.Groupe import Groupe
from functools import wraps
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity)
from flask import abort

# Création d'un nouveau Blueprint. C'est une façon d'organiser les routes dans Flask.
groupe_bp = Blueprint('groupe', __name__)

#Définition d'une route pour créer un groupe.
#Cette fonction sera appelée lorsqu'une requête POST est faite à '/groupe'.
@groupe_bp.route('/groupe', methods=['POST'])
@jwt_required()
def create_groupe():
    #Récupération des données du cours à créer.
    data = request.json
    try:
        #Tentative de création du cours.
        groupe = GroupeService.create_groupe(data)
        return jsonify(groupe.to_dict()), 200
    #Si une erreur s'est produite, retourne un message d'erreur et arrêt de la tentative de création de groupe.
    except ValueError as ve:
        abort(400, {'error': str(ve)})
    except PermissionError as pe:
        abort(403, {'error': str(pe)})
    except NotFoundErr as nfe:
        abort(404, {'error': str(nfe)})
    except Exception as e:
        abort(500, {'error': str(e)})

#Définition d'une route pour obtenir tous les groupes.
#Cette fonction sera appelée lorsqu'une requête GET est faite à '/groupes'.
@groupe_bp.route('/groupes', methods=['GET'])
@jwt_required()
def get_all_groupes():
    try:
        #Récupération et retour de tous les groupes.
        groupes = GroupeService.get_all_groupes()
        groupes_dict = [groupe.to_dict() for groupe in groupes]
        return jsonify(groupes_dict),200
    except Exception as e:
        #Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

#Définition d'une route pour obtenir un groupe spécifique par son ID.
#Cette fonction sera appelée lorsqu'une requête GET est faite à '/groupe/<id>'.
@groupe_bp.route('/groupe/<id>', methods=['GET'])
@jwt_required()
def get_by_id(id):
    try:
        #Récupération du groupe par son ID.
        groupe = GroupeService.get_groupe_by_id(id)
        #Si le groupe n'a pas été trouvé, retourne un message d'erreur.
        if not groupe:
            return jsonify({'error': 'Groupe not found'}),403
        #Si le groupe a été trouvé, le retourne.
        return jsonify(groupe.to_dict()),200
    except Exception as e:
        #Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403
    
#Définition d'une route pour supprimer un groupe spécifique par son ID.
@groupe_bp.route('/groupe/<id>', methods=['DELETE'])
@jwt_required()
def delete_groupe(id):
    try:
        #Tentative de suppression du groupe.
        groupe = GroupeService.delete_groupe(id)
        #Si le groupe n'a pas été trouvé, retourne un message d'erreur.
        if not groupe:
            return jsonify({'error': 'Groupe not found'}),403
        #Si le groupe a été trouvé, le retourne.
        return jsonify(groupe.to_dict()),200
    except Exception as e:
        #Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403
    
#Définition d'une route pour mettre à jour un groupe spécifique par son ID.
#Cette fonction sera appelée lorsqu'une requête PUT est faite à '/groupe/<id>'.
@groupe_bp.route('/groupe/<id>', methods=['PUT'])
@jwt_required()
def update_groupe(id):
    #Récupération des données du groupe à mettre à jour.
    data = request.json
    #Si l'ID est présent dans les données, le supprime.
    if 'id' in data:
        del data['id']
    try:
        #Tentative de mise à jour du groupe.
        groupe = GroupeService.update_groupe(id, **data)
        #Si le groupe n'a pas été trouvé, retourne un message d'erreur.
        if not groupe:
            return jsonify({'error': 'Groupe not found'}),403
        #Si le groupe a été trouvé, le retourne.
        return jsonify(groupe.to_dict()),200
    except Exception as e:
        #Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

#Définition d'une route pour obtenir les enfants et les parents d'un groupe spécifique par son ID.
#Cette fonction sera appelée lorsqu'une requête GET est faite à '/groupe/children/<id>'.
@groupe_bp.route('/groupe/tree/<id>', methods=['GET'])
@jwt_required()
def get_tree(id):
    try:
        #Récupération du groupe par son ID.
        groupe = GroupeService.get_groupe_by_id(id)
        #Si le groupe n'a pas été trouvé, retourne un message d'erreur.
        if not groupe:
            return jsonify({'error': 'Groupe not found'}),403
        
        #Récupération des parents et des enfants du groupe.
        groupe_dict = groupe.to_dict()
        groupe_dict["parent"] = GroupeService.get_parents(id)["parent"]
        groupe_dict["children"] = GroupeService.get_children(id)["children"]
        #Retourne le groupe avec ses parents et ses enfants.
        return jsonify(groupe_dict),200
    except Exception as e:
        #Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

#Définition d'une route pour obtenir les enfants d'un groupe spécifique par son ID.
#Cette fonction sera appelée lorsqu'une requête GET est faite à '/groupe/children/<id>'.
@groupe_bp.route('/groupe/childs/<id>', methods=['GET'])
@jwt_required()
def get_childs(id):
    try:
        #Récupération du groupe par son ID.
        groupe = GroupeService.get_groupe_by_id(id)
        #Si le groupe n'a pas été trouvé, retourne un message d'erreur.
        if not groupe:
            return jsonify({'error': 'Groupe not found'}),403
        
        #Récupération des enfants du groupe.
        groupe_dict = groupe.to_dict()
        groupe_dict["children"] = GroupeService.get_children(id)["children"]
                
        return jsonify(groupe_dict),200
    except Exception as e:
        #Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403