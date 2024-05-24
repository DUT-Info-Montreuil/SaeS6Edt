from xml.dom import NotFoundErr
from flask import Blueprint, jsonify, send_from_directory, request
from functools import wraps
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity)
from services.ResponsableEdtService import ResponsableEdtService
from models.User import User
from services.UserService import UserService
from services.PromotionService import PromotionService
from services.AffiliationRespEdtService import AffiliationRespEdtService
from flask import abort

# Création d'un nouveau Blueprint. C'est une façon d'organiser les routes dans Flask.
responsable_edt_bp = Blueprint('responsable_edt', __name__)

#Définition d'une route pour récuperer tous les responsables étudiants
#Cette fonction sera appelée lorsqu'une requête GET est faite à '/responsables'.
@responsable_edt_bp.route('/responsables', methods=['GET'])
@jwt_required()
def get_all_responsable_edt():
    try:
        # Récupérer tous les responsables d'emploi du temps
        responsables_edt = ResponsableEdtService.get_all_responsable_edt()
        responsables_edt_dict = [responsable_edt.to_dict() for responsable_edt in responsables_edt]
        # Récupérer tous les enseignants
        return jsonify(responsables_edt_dict),200
    except Exception as e:
        # En cas d'erreur, annulez la transaction et renvoyez un message d'erreur
        # db.session.rollback()
        return jsonify({'error': str(e)}),403

#Définition d'une route pour récuperer un responsable d'emploi du temps par son ID
#Cette fonction sera appelée lorsqu'une requête GET est faite à '/responsable/<id>'.
@responsable_edt_bp.route('/responsable/<id>', methods=['GET'])
@jwt_required()
def get_by_responsable_edt(id):
    try:
        # Récupérer le responsable d'emploi du temps par son ID
        responsables_edt = ResponsableEdtService.get_by_id(id)
        # Si le responsable d'emploi du temps n'existe pas, renvoyez une erreur 404
        if not responsables_edt:
            return jsonify({'error': 'Responsable Edt not found'}),403
        # Sinon, renvoyez le responsable d'emploi du temps
        return jsonify(responsables_edt.to_dict()),200
    except Exception as e:
        # En cas d'erreur, annulez la transaction et renvoyez un message d'erreur
        # db.session.rollback()
        return jsonify({'error': str(e)}),403

#Définition d'une route pour créer un responsable d'emploi du temps
#Cette fonction sera appelée lorsqu'une requête POST est faite à '/responsable'.
@responsable_edt_bp.route('/responsable', methods=['POST'])
@jwt_required()
def create_responsable():
    data = request.json
    try:
        # Créer un responsable d'emploi du temps
        responsable_edt = ResponsableEdtService.create_responsable_edt(data)
        # Renvoyer le responsable d'emploi du temps
        return jsonify(responsable_edt.to_dict()), 200
    # Si une erreur se produit, renvoyez un message d'erreur
    except ValueError as ve:
        abort(400, {'error': str(ve)})
    except PermissionError as pe:
        abort(403, {'error': str(pe)})
    except NotFoundErr as nfe:
        abort(404, {'error': str(nfe)})
    except Exception as e:
        abort(500, {'error': str(e)})

#Définition d'une route pour supprimer un responsable d'emploi du temps
#Cette fonction sera appelée lorsqu'une requête DELETE est faite à '/responsable/<id>'.
@responsable_edt_bp.route('/responsable/<id>', methods=['DELETE'])
@jwt_required()
def delete_responsable(id):
    try:
        # Supprimer le responsable d'emploi du temps
        responsable_edt = ResponsableEdtService.delete_responsable_edt(id)
        # Si le responsable d'emploi du temps n'existe pas, renvoyez une erreur 404
        if not responsable_edt:
            return jsonify({'error': 'Responsable Edt not found'}),403
        # Sinon, renvoyez un message de succès
        return jsonify(responsable_edt.to_dict()),200
    except Exception as e:
        # En cas d'erreur, renvoyez un message d'erreur
        return jsonify({'error': str(e)}),403

#Définition d'une route pour mettre à jour un responsable d'emploi du temps
#Cette fonction sera appelée lorsqu'une requête PUT est faite à '/responsable/<id>'.
@responsable_edt_bp.route('/responsable/<id>', methods=['PUT'])
@jwt_required()
def update_responsable_edt(id):
    data = request.json
    # Si l'ID est présent dans le dictionnaire, supprimez-le
    if 'id' in data:
        del data['id']
    try:
        # Mettre à jour le responsable d'emploi du temps
        responsable_edt = ResponsableEdtService.update_responsableEdt(id=id, **data)
        # Si le responsable d'emploi du temps n'existe pas, renvoyez une erreur 404
        if not responsable_edt:
            return jsonify({'error': 'Responsable edt not found'}),403
        # Sinon, renvoyez le responsable d'emploi du temps modifié
        return jsonify(responsable_edt.to_dict()),200
    except Exception as e:
        # En cas d'erreur, renvoyez un message d'erreur
        return jsonify({'error': str(e)}),403
    
#Définition d'une route pour récuperer les promos
#Cette fonction sera appelée lorsqu'une requête GET est faite à '/responsable/promos'.
@responsable_edt_bp.route('/responsable/promos', methods=['GET'])
@jwt_required()
def get_promos():
    try:
        # Récupérer tous les responsables d'emploi du temps
        current_user = get_jwt_identity()
        user : User = UserService.get_by_id(current_user)
        respEdt= ResponsableEdtService.get_by_userId(user.id)
        promos = AffiliationRespEdtService.get_promos_for_respedt(respEdt.id_resp)

        # Retourner les promos
        return [promos.to_dict() for promos in promos],200
    except Exception as e:
        # En cas d'erreur, renvoyez un message d'erreur
        return jsonify({'error': str(e)}),403
    # id_groups = [promo.id_group for promo in promos]