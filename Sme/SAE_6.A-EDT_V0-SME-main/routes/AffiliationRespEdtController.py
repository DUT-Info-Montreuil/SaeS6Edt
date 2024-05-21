# Importation des modules nécessaires de flask et flask_jwt_extended
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity)

# Importation du service AffiliationRespEdtService
from services.AffiliationRespEdtService import AffiliationRespEdtService

# Création d'un nouveau Blueprint. C'est une façon d'organiser les routes dans Flask.
affiliationrespedt_bp = Blueprint('affiliationrespedt', __name__)

# Définition d'une route pour associer un responsable d'emploi du temps à une promotion. 
# Cette fonction sera appelée lorsqu'une requête POST est faite à '/affiliateRespEdt'.
@affiliationrespedt_bp.route('/affiliateRespEdt', methods=['POST'])
@jwt_required()
def affiliate_respedt_to_promo():
    # Récupération des identifiants du responsable et de la promotion à partir des données de la requête.
    idResp = request.json["id_resp"]
    idPromo = request.json["id_promo"]
    
    try:
        # Appel du service pour associer le responsable à la promotion.
        affiliate_respEdt = AffiliationRespEdtService.affiliate_respedt_to_promo(idResp,idPromo)

        # Si l'association a réussi, retourne un message de succès.
        return jsonify({"message": "RespEdtPromo ajouté au groupe avec succès"}),200
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

# Définition d'une route pour obtenir les promotions associées à un responsable. 
# Cette fonction sera appelée lorsqu'une requête GET est faite à '/affiliateRespEdt/getPromosByResp/<idResp>'.
@affiliationrespedt_bp.route('/affiliateRespEdt/getPromosByResp/<idResp>', methods=['GET'])
@jwt_required()
def get_promos_for_respedt(idResp):
    try:
        # Appel du service pour obtenir les promotions associées au responsable.
        affiliate_respEdt = AffiliationRespEdtService.get_promos_for_respedt(idResp)

        # Si aucune promotion n'a été trouvée, retourne un message d'erreur.
        if not affiliate_respEdt:
            return jsonify({'error': 'Promotions not found'}),201

        # Si des promotions ont été trouvées, les retourne.
        return jsonify(affiliate_respEdt),200
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403
    

# Définition d'une route pour obtenir les responsables associés à une promotion. 
# Cette fonction sera appelée lorsqu'une requête GET est faite à '/affiliateRespEdt/getRespByPromo/<idPromo>'.
@affiliationrespedt_bp.route('/affiliateRespEdt/getRespByPromo/<idPromo>', methods=['GET'])
@jwt_required()
def get_respedt_for_promo(idPromo):
    try:
        # Appel du service pour obtenir les responsables associés à la promotion.
        respedts = AffiliationRespEdtService.get_respedt_by_promo(idPromo)

        # Si des responsables ont été trouvés, les retourne.
        return jsonify([respedt.to_dict() for respedt in respedts]),200
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

# Définition d'une route pour supprimer l'association d'un responsable à une promotion. 
# Cette fonction sera appelée lorsqu'une requête DELETE est faite à '/affiliateRespEdt/delete/<idResp>/'.
@affiliationrespedt_bp.route('/affiliateRespEdt/delete/<idResp>/', methods=['DELETE'])
@jwt_required()
def delete_affiliate_respedt_to_promo(idResp):
    try:
        # Appel du service pour supprimer l'association du responsable à la promotion.
        affiliate_respEdt = AffiliationRespEdtService.delete_respEdt_promo(idResp)

        # Si la suppression a réussi, retourne un message de succès.
        return jsonify({"message": "RespEdtPromo supprimé du groupe avec succès"}), 200
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}), 403

# Définition d'une route pour supprimer l'association d'un responsable et d'une promotion. 
# Cette fonction sera appelée lorsqu'une requête DELETE est faite à '/affiliateRespEdt/delete/<idResp>/<idPromo>'.
@affiliationrespedt_bp.route('/affiliateRespEdt/delete/<idResp>/<idPromo>', methods=['DELETE'])
@jwt_required()
def delete_affiliate_respedt_and_promo(idResp, idPromo):
    try:
        # Appel du service pour supprimer l'association du responsable et de la promotion.
        affiliate_respEdt = AffiliationRespEdtService.delete_respEdt_and_promo(idResp, idPromo)

        # Si la suppression a réussi, retourne un message de succès.
        return jsonify({"message": "RespEdtPromo supprimé du groupe avec succès"}), 200
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}), 403
