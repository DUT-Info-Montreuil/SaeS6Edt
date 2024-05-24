from xml.dom import NotFoundErr
from flask import Blueprint, jsonify, request
from services.PromotionService import PromotionService
from flask import abort
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity)

# Création d'un nouveau Blueprint. C'est une façon d'organiser les routes dans Flask.
promotion_bp = Blueprint('promotion', __name__)

#Définition d'une route pour récuperer toutes les promotions
#Cette fonction sera appelée lorsqu'une requête GET est faite à '/promotions'.
@promotion_bp.route('/promotions', methods=['GET'])
@jwt_required()
def get_all_promotions():

    try:
        # Récupérer toutes les promotions existantes
        promotions = PromotionService.get_all_promos()   

        #Retourne un tableau de dictionnaires représentant les promotions
        promotions_dict = [promotion.to_dict() for promotion in promotions]
        return jsonify(promotions_dict),200
    except Exception as e:
        # En cas d'erreur, annulez la transaction et renvoyez un message d'erreur
        # db.session.rollback()
        return jsonify({'error': str(e)}),403

#Définition d'une route pour récuperer une promotion par son id
#Cette fonction sera appelée lorsqu'une requête GET est faite à '/promotion/<id>'.
@promotion_bp.route('/promotion/<id>', methods=['GET'])
@jwt_required()
def get_promotion_by_id(id):

    try:
        # Récupérer la promotion avec l'id spécifié
        promotion = PromotionService.get_promo_by_id(id)   

        #Si la promotion n'existe pas, renvoyer une erreur 404
        if not promotion:
            return jsonify({'error': 'Promotion not found'}),404
        #Sinon, retourner la promotion
        return jsonify(promotion.to_dict()),200
    except Exception as e:
        # En cas d'erreur, annulez la transaction et renvoyez un message d'erreur
        # db.session.rollback()
        return jsonify({'error': str(e)}),403

#Définition d'une route pour récuperer une promotion par son année
#Cette fonction sera appelée lorsqu'une requête GET est faite à '/promotion/<year>'.
@promotion_bp.route('/promotion/<year>', methods=['GET'])
@jwt_required()
def get_promotion_by_year(year):
    
        try:
            # Récupérer les promotions avec l'année spécifiée
            promotion = PromotionService.get_promo_by_year(year)   
    
            #Si la promotion n'existe pas, renvoyer une erreur 404
            if not promotion:
                return jsonify({'error': 'Promotion not found'}),404
            #Sinon, retourner la promotion
            return jsonify(promotion.to_dict()),200
        except Exception as e:
            # En cas d'erreur, annulez la transaction et renvoyez un message d'erreur
            # db.session.rollback()
            return jsonify({'error': str(e)}),403

#Définition d'une route pour récuperer les promotions activées
#Cette fonction sera appelée lorsqu'une requête GET est faite à '/promotion/activated'.
@promotion_bp.route('/promotion/activated', methods=['GET'])
@jwt_required()
def get_promotion_activated():
    try:
        # Récupérer les promotions activées
        promotions = PromotionService.get_promo_activated()
        #Retourne un tableau de dictionnaires représentant les promotions
        promotions_dict = [promotion.to_dict() for promotion in promotions]
        return jsonify(promotions_dict),200
    except Exception as e:
        # En cas d'erreur, annulez la transaction et renvoyez un message d'erreur
        # db.session.rollback()
        return jsonify({'error': str(e)}),403

#Définition d'une route pour récuperer les promotions désactivées
#Cette fonction sera appelée lorsqu'une requête GET est faite à '/promotion/deactivated'.
@promotion_bp.route('/promotion/deactivated', methods=['GET'])
@jwt_required()
def get_promotion_not_activated():
    try:
        # Récupérer les promotions activées
        promotions = PromotionService.get_promo_not_activated()
        #Retourne un tableau de dictionnaires représentant les promotions
        promotions_dict = [promotion.to_dict() for promotion in promotions]
        return jsonify(promotions_dict),200
    except Exception as e:
        # En cas d'erreur, annulez la transaction et renvoyez un message d'erreur
        # db.session.rollback()
        return jsonify({'error': str(e)}),403
    
#Définition d'une route pour créer une promotion
#Cette fonction sera appelée lorsqu'une requête POST est faite à '/promotion'.
@promotion_bp.route('/promotion', methods=['POST'])
@jwt_required()
def create_promotion():
    try:
        # Récupérer les données de la requête
        data = request.json

        print("hnduehd",data)
        # Créer une promotion avec les données récupérées et la retourner
        promotion = PromotionService.create_promo(data)
        return jsonify(promotion.to_dict()), 200
    # Gérer les erreurs
    except ValueError as ve:
        abort(400, {'error': str(ve)})
    except PermissionError as pe:
        abort(403, {'error': str(pe)})
    except NotFoundErr as nfe:
        abort(404, {'error': str(nfe)})
    except Exception as e:
        abort(500, {'error': str(e)})

#Définition d'une route pour supprimer une promotion
#Cette fonction sera appelée lorsqu'une requête DELETE est faite à '/promotion/<id>'.
@promotion_bp.route('/promotion/<id>', methods=['DELETE'])
@jwt_required()
def delete_promotion(id):
    try:
        # Supprimer la promotion avec l'id spécifié
        promotion = PromotionService.delete_promo(id)
        #Si la promotion n'existe pas, renvoyer une erreur 404
        if not promotion:
            return jsonify({'error': 'Promotion not found'}),404
        #Sinon, retourner la promotion
        return jsonify(promotion.to_dict()),200
    except Exception as e:
        # En cas d'erreur, annulez la transaction et renvoyez un message d'erreur
        # db.session.rollback()
        return jsonify({'error': str(e)}),403
    
#Définition d'une route pour mettre à jour une promotion
#Cette fonction sera appelée lorsqu'une requête PUT est faite à '/promotion/<id>'.
@promotion_bp.route('/promotion/<id>', methods=['PUT'])
@jwt_required()
def update_promotion(id):
    try:
        data = request.json
        #Si l'id est présent dans les données, le supprimer
        if 'id' in data:
            del data['id']

        # Mettre à jour la promotion avec l'id spécifié
        promotion = PromotionService.update_promo(id=id, **data)
        #Si la promotion n'existe pas, renvoyer une erreur 404
        if not promotion:
            return jsonify({'error': 'Promotion not found'}),404
        #Sinon, retourner la promotion
        return jsonify(promotion.to_dict()),200
    except Exception as e:
        # En cas d'erreur, renvoyez un message d'erreur
        return jsonify({'error': str(e)}),403
    
@promotion_bp.route('/promotion/deactivate/<id>', methods=['PUT'])
@jwt_required()
def deactivate_promotion(id):
    try:
        # Mettre à jour la promotion avec l'id spécifié
        promotion = PromotionService.deactivate_promo(id)
        #Si la promotion n'existe pas, renvoyer une erreur 404
        if not promotion:
            return jsonify({'error': 'Promotion not found'}),404
        #Sinon, retourner la promotion
        return jsonify(promotion.to_dict()),200
    except Exception as e:
        # En cas d'erreur, renvoyez un message d'erreur
        return jsonify({'error': str(e)}),403