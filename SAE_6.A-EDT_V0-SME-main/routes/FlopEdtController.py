from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from services.flop_edt_service import FlopEdtServices

flopEdt_bp = Blueprint('flopEdt', __name__)

@flopEdt_bp.route('/flopEdt/<dept>/<week>/<year>/<work_copy>', methods=['GET'])
@jwt_required()
def get_FlopEdt_courses(dept, week, year, work_copy):
    data = FlopEdtService.get_FlopEdt(dept, week, year, work_copy)
    
    if data is None:
        return jsonify({"error": "An error occurred while fetching the data"}), 500
    
    return jsonify(data), 200