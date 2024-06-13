from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from services.FlopEdtService import FlopEdtService

flopEdt_bp = Blueprint('flopEdt', __name__)

@flopEdt_bp.route('/flopEdt', methods=['POST'])
@jwt_required()
def get_FlopEdt_courses():
    # Récupérer les paramètres du corps de la requête
    data = request.get_json()
    dept = data.get('dept')
    week = data.get('week')
    year = data.get('year')
    work_copy = data.get('work_copy')
    
    # Appel au service pour obtenir les données
    response_data = FlopEdtService.get_FlopEdt_courses(dept, week, year, work_copy)
    
    if response_data is None:
        return jsonify({"error": "An error occurred while fetching the data"}), 500
    
    return jsonify(response_data), 200