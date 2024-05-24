# Fonction de vérification du rôle
from functools import wraps
from flask import jsonify

from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity)

from services.UserService import UserService


def role_required(roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user = UserService.get_by_id(get_jwt_identity())
            if current_user.role in roles:
                return fn(*args, **kwargs)
            else:
                return jsonify(message="Accès refusé. Rôle insuffisant."), 403
        return wrapper
    return decorator
    


# @api_bp.route('/test', methods=['GET'])
# @jwt_required()
# @role_required(roles=['ROLE_ADMIN'])
# def ressource_protégée():
#     current_user = get_jwt_identity()
#     return {'message': 'Ceci est une ressource protégée', 'user': current_user},200
