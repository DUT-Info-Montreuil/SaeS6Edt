from database.config import db
from models.Promotion import Promotion

class PromotionService:

    # Crée une nouvelle promotion avec les données fournies
    @staticmethod
    def create_promo(data):
        promo = Promotion(**data)

        db.session.add(promo)
        db.session.commit()

        return promo
    
    # Récupère toutes les promotions de la base de données
    @staticmethod
    def get_all_promos():
        return Promotion.query.all()
    
    # Récupère une promotion par son identifiant
    @staticmethod
    def get_promo_by_id(id_promo):
        return Promotion.query.filter_by(id_promo=id_promo).first()
    
    # Récupère une promotion par son année scolaire
    @staticmethod
    def get_promo_by_year(year):
        return Promotion.query.filter_by(year=year).all()
    
    @staticmethod
    def get_promo_activated():
        return Promotion.query.filter_by(activated=True).all()
    
    @staticmethod
    def get_promo_not_activated():
        return Promotion.query.filter_by(activated=False).all()
    
    # Supprime une promotion de la base de données par son identifiant
    @staticmethod
    def delete_promo(id_promo):
        promo = Promotion.query.filter_by(id_promo=id_promo).first()
        db.session.delete(promo)
        db.session.commit()
        return promo

    # Met à jour les informations d'une promotion avec les valeurs fournies
    @staticmethod
    def update_promo(id,name, niveau, id_resp, **kwargs):
        promo = Promotion.query.filter_by(id_promo=id).first()
        promo.name = name
        promo.niveau = niveau
        promo.id_resp = id_resp

        db.session.commit()
        return promo
    
    @staticmethod
    def deactivate_promo(id_promo):
        promo = Promotion.query.filter_by(id_promo=id_promo).first()
        if promo.activated:
            promo.activated = False
        else:
            promo.activated = True
        db.session.commit()
        return promo
    