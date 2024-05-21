from database.config import db
from models.ResponsableEdt import ResponsableEdt
from models.Staff import Staff
from models.User import User

class ResponsableEdtService():
    
    # Récupère tous les responsables d'emploi du temps de la base de données
    @staticmethod
    def get_all_responsable_edt():
      return ResponsableEdt.query.all()

    # Crée un nouveau responsable d'emploi du temps avec les données fournies
    @staticmethod
    def create_responsable_edt(data):
        responsable_edt = ResponsableEdt(**data)
        db.session.add(responsable_edt)
        db.session.commit()

        return responsable_edt
    
    # Récupère un responsable d'emploi du temps par son identifiant
    @staticmethod
    def get_by_id(id):
        return ResponsableEdt.query.filter_by(id_resp=id).first()
    
    # Récupère un responsable d'emploi du temps par l'identifiant de l'utilisateur associé
    @staticmethod
    def get_by_userId(userId):
        respedt = ResponsableEdt.query.filter_by(id_staff=userId).first()
        return respedt
    
    # Récupère les promotions associées à un responsable d'emploi du temps
    # @staticmethod
    # def get_promos(respEdt):
    #     promos = AffiliationRespEdtService.get_promos_for_respedt(respEdt.id_resp)
    #     return promos
    #     # id_groups = [promo.id_group for promo in promos]
    
    # Supprime un responsable d'emploi du temps de la base de données par son identifiant
    @staticmethod
    def delete_responsable_edt(id):
        responsable_edt = ResponsableEdt.query.filter_by(id_resp=id).first()
        db.session.delete(responsable_edt)
        db.session.commit()
        return responsable_edt
    
    # Met à jour les informations d'un responsable d'emploi du temps avec les valeurs fournies
    @staticmethod
    def update_responsableEdt(id, name: str, lastname: str, **kwargs):
        responsable_edt = ResponsableEdt.query.filter_by(id_resp=id).first()
        responsable_edt.name = name
        responsable_edt.lastname = lastname

        db.session.commit()
        return responsable_edt