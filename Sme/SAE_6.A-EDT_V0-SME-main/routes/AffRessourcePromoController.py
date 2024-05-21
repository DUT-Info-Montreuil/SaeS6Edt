from flask import Blueprint, jsonify, request
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity)

from services.AffRessourcePromoService import AffRessourcePromoService

affiliationressourcepromo_bp = Blueprint('affiliationressourcepromo_bp', __name__)

@affiliationressourcepromo_bp.route('/affiliateRessourcePromo', methods=['POST'])
@jwt_required()
def affiliate_resssource_to_promo():
    # Récupération des identifiants du responsable et de la promotion à partir des données de la requête.
    idRessource = request.json["id_ressource"]
    idPromo = request.json["id_promo"]
    
    try:
        # Appel du service pour associer le responsable à la promotion.
        AffRessourcePromoService.affiliate_ressource_to_promo(idRessource, idPromo)

        # Si l'association a réussi, retourne un message de succès.
        return jsonify({"message": "RespEdtPromo ajouté au groupe avec succès"}),200
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403
    
@affiliationressourcepromo_bp.route('/getRessourcesByPromo/<int:idPromo>', methods=['GET'])
@jwt_required()
def get_ressources_by_promo(idPromo):
    try:
        ressources = AffRessourcePromoService.get_ressources_by_promo(idPromo)
        return jsonify([ressource.to_dict() for ressource in ressources]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 403

@affiliationressourcepromo_bp.route('/getPromoByRessource/<string:idRessource>', methods=['GET'])
@jwt_required()
def get_promo_by_ressource(idRessource):
    try:
        promotions = AffRessourcePromoService.get_promo_by_ressource(idRessource)
        return jsonify([promotion.to_dict() for promotion in promotions]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 403

@affiliationressourcepromo_bp.route('/deleteAffiliation/<int:idPromo>/<string:idRessource>', methods=['DELETE'])
@jwt_required()
def delete_affiliation(idPromo, idRessource):
    try:
        AffRessourcePromoService.delete_affiliation(idRessource, idPromo)
        return jsonify({'message': 'L\'affiliation à bien été supprimé'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 403
    
@affiliationressourcepromo_bp.route('/migrerRessources/<int:oldPromoId>/<int:newPromoId>', methods=['PUT'])
@jwt_required()
def change_promotion_for_all_resources(oldPromoId, newPromoId):
    try:
        AffRessourcePromoService.change_promotion_for_all_resources_in_promo(oldPromoId, newPromoId)
        return jsonify({'message': 'La promotion de toutes les ressources affiliées a été modifiée avec succès'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 403
