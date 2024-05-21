from database.config import db
from models.Salle import Salle

class SalleService:

    # Crée une nouvelle salle avec les données fournies
    @staticmethod
    def create_salle(data):
        salle = Salle(**data)

        db.session.add(salle)
        db.session.commit()

        return salle
    
    
    # Vérifie si une salle avec le nom spécifié existe déjà
    @staticmethod
    def isExist(nom):
        return Salle.query.filter_by(nom=nom).first() is not None
    
    # Récupère toutes les salles de la base de données
    @staticmethod
    def get_all_salles():
        return Salle.query.all()
    
    # Récupère une salle par son nom
    @staticmethod
    def get_salle_by_name(nom):
        return Salle.query.filter_by(nom=nom).first()
    
    # Supprime une salle de la base de données par son nom
    @staticmethod
    def delete_salle(nom):
        salle = SalleService.get_salle_by_name(nom)
        db.session.delete(salle)
        db.session.commit()
        return salle
    
    # Met à jour les informations d'une salle avec les valeurs fournies
    @staticmethod
    def update_salle(name, ordi, tableauNumerique, videoProjecteur):
        salle = SalleService.get_salle_by_name(name)
        salle.ordi = ordi
        salle.tableauNumerique = tableauNumerique
        salle.videoProjecteur = videoProjecteur
        db.session.commit()
        return salle
