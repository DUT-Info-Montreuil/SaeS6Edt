from flask import Blueprint, jsonify, send_from_directory, request
from services.UserService import UserService
from services.LdapService import LdapService
from models.User import User
from functools import wraps
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity)
from flask import abort

# Création d'un nouveau Blueprint. C'est une façon d'organiser les routes dans Flask.
user_bp = Blueprint('user', __name__)

# Définition d'une route pour créer un nouvel utilisateur. 
# Cette fonction sera appelée lorsqu'une requête POST est faite à '/user'.
@user_bp.route('/user', methods=['POST'])
@jwt_required()
def create_user():
    # Récupération des données de la requête.
    username = request.json.get('username')
    password = request.json.get('password')
    name = request.json.get('name')
    lastname = request.json.get('lastname')
    try:
        # Création de l'utilisateur avec les données fournies.
        user = UserService.create_user(username, password, name, lastname)
        return jsonify(user.to_dict()),200
    except Exception as e:
        # En cas d'erreur, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403 

# Définition d'une route pour obtenir tous les utilisateurs. 
# Cette fonction sera appelée lorsqu'une requête GET est faite à '/users'.
@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_user():
    try:
        # Récupération de tous les utilisateurs.
        users = UserService.get_all_users()
        users_dict = [user.to_dict() for user in users]
        return jsonify([users_dict]),200
    except Exception as e:
        # En cas d'erreur, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

# Définition d'une route pour obtenir un utilisateur spécifique par son ID. 
# Cette fonction sera appelée lorsqu'une requête GET est faite à '/user/<id>'.
@user_bp.route('/user/<id>', methods=['GET'])
@jwt_required()
def get_by_idUser(id):
    try:
        # Récupération de l'utilisateur par son ID.
        user = UserService.get_by_id(id)
        if not user:
            return jsonify({'error': 'User not found'}),403  
        return jsonify(user.to_dict()),200
    except Exception as e:
        # En cas d'erreur, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

# Définition d'une route pour supprimer un utilisateur spécifique par son ID. 
# Cette fonction sera appelée lorsqu'une requête DELETE est faite à '/user/<id>'.
@user_bp.route('/user/<id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    try:
        # Suppression de l'utilisateur par son ID.
        user = UserService.get_by_id(id)
        UserService.delete_user(user)
        if not user:
            return jsonify({'error': 'User not found'}),403  
        return jsonify(user.to_dict()),200
    except Exception as e:
        # En cas d'erreur, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

# Définition d'une route pour mettre à jour un utilisateur spécifique par son ID. 
# Cette fonction sera appelée lorsqu'une requête PUT est faite à '/user/<id>'.
@user_bp.route('/user/<id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    # Récupération des données de la requête.
    data = request.json
    if 'id' in data:
        del data['id']
    try:
        # Mise à jour de l'utilisateur avec les données fournies.
        user = UserService.update_user(id=id, **data)
        if not user:
            return jsonify({'error': 'User not found'}),403  
        return jsonify(user.to_dict()),200
    except Exception as e:
        # En cas d'erreur, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

# Définition d'une route pour identifier l'utilisateur actuel. 
# Cette fonction sera appelée lorsqu'une requête GET est faite à '/identify'.
@user_bp.route('/identify', methods=['GET'])
@jwt_required()
def identify():
    current_user = get_jwt_identity()
    try:
        user = UserService.get_by_id(current_user)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user_roles = LdapService.get_user_role(user.username)
        if not user_roles:
            return jsonify({'error': 'User roles not found'}), 404

        normalized_user_roles = [LdapService.normalize_role(role) for role in user_roles]
        user_role_normalized = LdapService.normalize_role(user.role)

        if user_role_normalized not in normalized_user_roles:
            return jsonify({'error': 'User role not authorized'}), 403

        return jsonify(user.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 403