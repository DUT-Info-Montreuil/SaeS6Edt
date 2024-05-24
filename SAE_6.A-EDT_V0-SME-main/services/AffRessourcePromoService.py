from database.config import db
from models.relations.ressource_promo import affiliation_ressource_promo
from services.RessourcesService import RessourcesService
from services.PromotionService import PromotionService

class AffRessourcePromoService:

    @staticmethod
    def affiliate_ressource_to_promo(idRessource, idPromo):
        asso = affiliation_ressource_promo.insert().values(initial = idRessource, id_promo = idPromo)
        db.session.execute(asso)
        db.session.commit()

    @staticmethod
    def get_ressources_by_promo(idPromo):
        query = db.session.query(affiliation_ressource_promo).filter_by(id_promo = idPromo)
        result = query.all()
        ressources = [initial for initial, id_promo in result]
        ressources = [RessourcesService.get_resource_by_initial(initial) for initial in ressources]
        return ressources
    
    @staticmethod
    def get_promo_by_ressource(idRessource):
        query = db.session.query(affiliation_ressource_promo).filter_by(initial = idRessource)
        result = query.all()
        promo = [id_promo for initial, id_promo in result]
        promo = [PromotionService.get_promo_by_id(id_promo) for id_promo in promo]
        return promo
    
    @staticmethod
    def delete_affiliation(idRessource, idPromo):
        try:
            db.session.query(affiliation_ressource_promo).filter(
                (affiliation_ressource_promo.c.initial == idRessource) &
                (affiliation_ressource_promo.c.id_promo == idPromo)
            ).delete(synchronize_session=False)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    @staticmethod
    def change_promotion_for_all_resources_in_promo(oldPromoId, newPromoId):
        try:
            # Obtenir les ressources affiliées à l'ancienne promotion
            query = db.session.query(affiliation_ressource_promo).filter_by(id_promo=oldPromoId)
            result = query.all()

            # Mettre à jour les affiliations avec la nouvelle promotion
            for initial, id_promo in result:
                db.session.query(affiliation_ressource_promo).filter(
                    (affiliation_ressource_promo.c.initial == initial) &
                    (affiliation_ressource_promo.c.id_promo == oldPromoId)
                ).update({affiliation_ressource_promo.c.id_promo: newPromoId}, synchronize_session=False)
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e