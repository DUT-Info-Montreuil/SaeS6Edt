# Importation des modules nécessaires
from flask import Blueprint, jsonify, request
from services.WeekCommentService import WeekCommentService
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity)

# Création d'un blueprint pour les routes liées aux commentaires de la semaine
week_comment_bp = Blueprint('comment', __name__)

# Route pour récupérer tous les commentaires de la semaine
@week_comment_bp.route('/week/comments', methods=['GET'])
@jwt_required()
def get_all_week_comments():
    try:
        # Récupérer tous les commentaires de la semaine
        comments = WeekCommentService.get_all_comments()   

        # Convertir chaque commentaire en dictionnaire pour le rendre sérialisable
        comments_dict = [comment.to_dict() for comment in comments]
        return jsonify(comments_dict),200
    except Exception as e:
        # En cas d'erreur, renvoyer un message d'erreur
        return jsonify({'error': str(e)}),403
    
# Route pour récupérer un commentaire par son id
@week_comment_bp.route('/week/comment/<id>', methods=['GET'])
@jwt_required()
def get_comment(id):
    try:
        # Récupérer le commentaire par son id
        comment = WeekCommentService.get_comment_by_id(id) 
        if not comment:
            # Si le commentaire n'est pas trouvé, renvoyer un message d'erreur
            return jsonify({'error': 'Commentaire not found'}),403  

        # Si tout se passe bien, renvoyer le commentaire
        return jsonify(comment.to_dict()),200
    except Exception as e:
        # En cas d'erreur, renvoyer un message d'erreur
        return jsonify({'error': str(e)}),403
    
# Route pour créer un commentaire
@week_comment_bp.route('/week/comment', methods=['POST'])
@jwt_required()
def create_comment():
    # Récupérer les données du corps de la requête
    data = request.json

    try:
        # Créer un commentaire
        comment = WeekCommentService.create_comment(data)

        # Si tout se passe bien, renvoyer le commentaire créé
        return jsonify(comment.to_dict()),200
    except Exception as e:
        # En cas d'erreur, renvoyer un message d'erreur
        return jsonify({'error': str(e)}),403
    
# Route pour supprimer un commentaire
@week_comment_bp.route('/week/comment/<id>', methods=['DELETE'])
@jwt_required()
def delete_comment(id):
    try: 
        # Supprimer le commentaire
        comment = WeekCommentService.delete_comment(id)

        # Si tout se passe bien, renvoyer le commentaire supprimé
        return jsonify(comment.to_dict()),200
    except Exception as e:
        # En cas d'erreur, renvoyer un message d'erreur
        return jsonify({'error': str(e)}),403
    
# Route pour mettre à jour un commentaire
@week_comment_bp.route('/week/comment/<id>', methods=['PUT'])
@jwt_required()
def update_comment(id):
    # Récupérer les données du corps de la requête
    data = request.json
    if 'id' in data:
        del data['id']

    try:
        # Mettre à jour le commentaire
        comment = WeekCommentService.update_comment(id=id, **data)

        # Si tout se passe bien, renvoyer le commentaire mis à jour
        return jsonify(comment.to_dict()),200
    except Exception as e:
        # En cas d'erreur, renvoyer un message d'erreur
        return jsonify({'error': str(e)}),403