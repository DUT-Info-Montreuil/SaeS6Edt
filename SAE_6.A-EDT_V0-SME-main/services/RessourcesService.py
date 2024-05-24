from database.config import db
from models.Ressources import Ressources

class RessourcesService:

    # Crée une nouvelle ressource avec les données fournies
    @staticmethod
    def create_resource(data):
        from services.AffRessourcePromoService import AffRessourcePromoService
        try:
            ressource = Ressources(**data)
            db.session.add(ressource)
            db.session.commit()
        except Exception as e:
            return None
        AffRessourcePromoService.affiliate_ressource_to_promo(data.get('initial'), data.get('id_promo'))
        return ressource
    
    # Récupère une ressource par son identifiant initial
    def get_resource_by_initial(initial):
        return Ressources.query.filter_by(initial=initial).first()
    
    # Récupère toutes les ressources de la base de données
    @staticmethod
    def get_all_ressources():
        ressources = Ressources.query.all()
        return ressources
    
    # Supprime une ressource de la base de données par son identifiant initial
    @staticmethod
    def delete_ressource(initial):
        resource = Ressources.query.filter_by(initial=initial).first()
        db.session.delete(resource)
        db.session.commit()
        return resource
    
    # Met à jour les informations d'une ressource avec les valeurs fournies
    @staticmethod
    def update_ressource(initial, name, id_promo):
        ressource = Ressources.query.filter_by(initial=initial).first()
        ressource.name = name
        ressource.id_promo = id_promo
        db.session.commit()
        return ressource
