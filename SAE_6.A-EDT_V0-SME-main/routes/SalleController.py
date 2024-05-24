from xml.dom import NotFoundErr
from flask import Blueprint, jsonify, request
from services.SalleService import SalleService
from flask import abort
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity)

# Création d'un nouveau Blueprint. C'est une façon d'organiser les routes dans Flask.
salle_bp = Blueprint('salle', __name__)

# Définition d'une route pour obtenir toutes les salles. 
# Cette fonction sera appelée lorsqu'une requête GET est faite à '/salles'.
@salle_bp.route('/salles', methods=['GET'])
@jwt_required()
def get_all_rooms():
    try:
        # Récupération de toutes les salles.
        salles = SalleService.get_all_salles()   

        # Conversion des salles en dictionnaires pour la réponse JSON.
        salles_dict = [salle.to_dict() for salle in salles]
        return jsonify(salles_dict),200
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

# Définition d'une route pour obtenir une salle spécifique par son nom. 
# Cette fonction sera appelée lorsqu'une requête GET est faite à '/salle/<name>'.
@salle_bp.route('/salle/<name>', methods=['GET'])
@jwt_required()
def get_room(name):
    try:
        # Récupération de la salle par son nom.
        salle = SalleService.get_salle_by_name(name) 

        # Si la salle n'a pas été trouvée, retourne un message d'erreur.
        if not salle:
            return jsonify({'error': 'Salle not found'}),403  

        # Si la salle a été trouvée, la retourne.
        return jsonify(salle.to_dict()),200
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

# Définition d'une route pour créer une nouvelle salle. 
# Cette fonction sera appelée lorsqu'une requête POST est faite à '/salle'.
@salle_bp.route('/salle', methods=['POST'])
@jwt_required()
def create_room():
    # Récupération des données de la requête.
    data = request.json

    try:
        # Création de la salle avec les données fournies.
        salle = SalleService.create_salle(data)

        # Si la salle a été créée avec succès, retourne un message de succès.
        return jsonify(salle.to_dict()), 200
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        abort(500, {'error': str(e)})
        
# Définition d'une route pour créer un ensemble de salles à partir d'un fichier CSV.
# Cette fonction sera appelée lorsqu'une requête POST est faite à '/salles/csv'.
@salle_bp.route('/salles/csv', methods=['POST'])
@jwt_required()
def create_room_from_csv():
    # Récupération du fichier CSV de la requête.
    data = request.json
    successfully_created = 0
    for i in range (len(data)):
        nombrepc = 0
        if len(data[i]) == 2:
            name = data[i][0]
            if data[i][1] != "":
                if "pc" in data[i][1].strip():
                    nombrepc = int(data[i][1].strip().split("pc")[0])    
                else:
                    name = name + " " + data[i][1]
            
            
            existing_salle = SalleService.get_salle_by_name(name)
            if existing_salle is not None:
                print(f"La salle {name} existe déjà")
                continue
    
            salle_data = {
                'name': name,
                'ordi': nombrepc,
                'tableauNumerique': 0,
                'videoProjecteur': 0
            }
            
            SalleService.create_salle(salle_data)
            
            successfully_created += 1
    
    if successfully_created > 0:
        return jsonify({'message': f'{successfully_created} salles créées avec succès'}), 200
    else:
        return jsonify({'message': 'Aucune salle créée'}), 200

# Définition d'une route pour supprimer une salle spécifique par son nom. 
# Cette fonction sera appelée lorsqu'une requête DELETE est faite à '/salle/<name>'.
@salle_bp.route('/salle/<name>', methods=['DELETE'])
@jwt_required()
def delete_room(name):
    try: 
        # Suppression de la salle par son nom.
        salle = SalleService.delete_salle(name)

        # Si la salle a été supprimée avec succès, retourne un message de succès.
        return jsonify(salle.to_dict()),200
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

# Définition d'une route pour mettre à jour une salle spécifique par son nom. 
# Cette fonction sera appelée lorsqu'une requête PUT est faite à '/salle/<name>'.
@salle_bp.route('/salle/<name>', methods=['PUT'])
@jwt_required()
def update_room(name):
    # Récupération des données de la requête.
    data = request.json

    try:
        # Mise à jour de la salle avec les données fournies.
        salle = SalleService.update_salle(name=name, **data)

        # Si la salle a été mise à jour avec succès, retourne un message de succès.
        return jsonify(salle.to_dict()),200
    except Exception as e:
        # Si une erreur s'est produite, retourne un message d'erreur.
        return jsonify({'error': str(e)}),403

    


    
    