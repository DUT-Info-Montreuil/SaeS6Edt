from xml.dom import NotFoundErr
from flask import Blueprint, jsonify, request
from services.RessourcesService import RessourcesService
from flask import abort
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity)

# Création d'un nouveau Blueprint. C'est une façon d'organiser les routes dans Flask.
ressource_bp = Blueprint('ressource', __name__)

#Définition d'une route pour récuperer toutes les ressources
#Cette fonction sera appelée lorsqu'une requête GET est faite à '/ressources'.
@ressource_bp.route('/ressources', methods=['GET'])
@jwt_required()
def get_all_ressources():

    try:
        # Récupérer toutes les ressources
        ressources = RessourcesService.get_all_ressources()   
        # Retourner les ressources
        ressources_dict = [ressource.to_dict() for ressource in ressources]
        return jsonify(ressources_dict),200
    except Exception as e:
        # En cas d'erreur, renvoyez un message d'erreur
        return jsonify({'error': str(e)}),403

#Définition d'une route pour récuperer une ressource selon ses initiales
#Cette fonction sera appelée lorsqu'une requête GET est faite à '/ressource/<initial>'.
@ressource_bp.route('/ressource/<initial>', methods=['GET'])
@jwt_required()
def get_ressource(initial):
    try:
        # Récupérer la ressource selon ses initiales
        ressource = RessourcesService.get_resource_by_initial(initial) 
        # Si la ressource n'existe pas, renvoyez un message d'erreur
        if not ressource:
            return jsonify({'error': 'Ressource not found'}),403  
        # Sinon, retournez la ressource
        return jsonify(ressource.to_dict()),200
    except Exception as e:
        # En cas d'erreur, renvoyez un message d'erreur
        return jsonify({'error': str(e)}),403

#Définition d'une route pour créer une ressource
#Cette fonction sera appelée lorsqu'une requête POST est faite à '/ressource'.
@ressource_bp.route('/ressource', methods=['POST'])
@jwt_required()
def create_ressource():
    data = request.json

    try:
        ressource = RessourcesService.create_resource(data)
        return jsonify(ressource.to_dict()), 200

    except ValueError as ve:
        abort(400, {'error': str(ve)})

    except PermissionError as pe:
        abort(403, {'error': str(pe)})

    except NotFoundErr as nfe:
        abort(404, {'error': str(nfe)})

    except Exception as e:
        abort(500, {'error': str(e)})


#Définition d'une route pour supprimer une ressource selon ses initiales
#Cette fonction sera appelée lorsqu'une requête DELETE est faite à '/ressource/<initial>'.
@ressource_bp.route('/ressource/<initial>', methods=['DELETE'])
@jwt_required()
def delete_ressource(initial):
    try: 
        # Récupérer la ressource selon ses initiales
        ressource = RessourcesService.delete_ressource(initial)
        # Retournez la ressource
        return jsonify(ressource.to_dict()),200
    except Exception as e:
        # En cas d'erreur, renvoyez un message d'erreur
        return jsonify({'error': str(e)}),403
    
#Définition d'une route pour mettre à jour une ressource selon ses initiales
#Cette fonction sera appelée lorsqu'une requête PUT est faite à '/ressource/<initial>'.
@ressource_bp.route('/ressource/<initial>', methods=['PUT'])
@jwt_required()
def update_ressource(initial):

    data = request.json
    if 'initial' in data:
        del data['initial']

    try:
        # Récupérer la ressource selon ses initiales
        ressource = RessourcesService.update_ressource(initial=initial,**data)
        # Retournez la ressource
        return jsonify(ressource.to_dict()),200
    except Exception as e:
        # En cas d'erreur, renvoyez un message d'erreur
        return jsonify({'error': str(e)}),403
    
    

# @ressource_bp.route('/salle/<name>', methods=['PUT'])
# def update_room(name):
#     ordi = request.json.get('ordi')
#     tableauNumerique = request.json.get('tableauNumerique')
#     videoProj = request.json.get('videoProjecteur')

#     try:
#         salle = SalleService.update_salle(name, ordi, tableauNumerique, videoProj)

#         return jsonify(salle.to_dict()),200
#     except Exception as e:
#         # En cas d'erreur, annulez la transaction et renvoyez un message d'erreur
#         # db.session.rollback()
#         return jsonify({'error': str(e)}),403