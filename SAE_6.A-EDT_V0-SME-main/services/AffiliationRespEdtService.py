from database.config import db
from models.relations.affiliation_resp_edt import affiliation_resp_edt
from models.Promotion import Promotion
from services.ResponsableEdtService import ResponsableEdtService
from services.PromotionService import PromotionService


class AffiliationRespEdtService:

  @staticmethod
  def affiliate_respedt_to_promo(resp_id, promo_id):
    # Create an instance of the user_groupe table
    resp_edt_association = affiliation_resp_edt.insert().values(id_resp=resp_id, id_promo=promo_id)

    # Add the association to the database session
    db.session.execute(resp_edt_association)

    # Commit the changes to the database
    db.session.commit()


  @staticmethod
  def get_respedt_by_promo(idPromo):

      query = db.session.query(affiliation_resp_edt).filter_by(id_promo=idPromo)

      result = query.all()
      respedts = [id_resp for id_resp, id_promo in result]
      respedts = [ResponsableEdtService.get_by_id(id_resp) for id_resp in respedts]
      return respedts
  
  @staticmethod
  def get_promos_for_respedt(idRespedt):
      query = db.session.query(affiliation_resp_edt).filter_by(id_resp=idRespedt)

      result = query.all()
      promos = [id_promo for id_resp, id_promo in result]
      promos = [PromotionService.get_promo_by_id(id_promo) for id_promo in promos]

      return promos
  
  # Delete all the affiliations of a respedt
  @staticmethod
  def delete_respEdt_promo(idResp):
        try:
            # Use delete() directly on the association table
            db.session.query(affiliation_resp_edt).filter(
                (affiliation_resp_edt.c.id_resp == idResp) &
                (affiliation_resp_edt.c.id_promo == Promotion.id)
            ).delete(synchronize_session=False)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
  # Delete a specific affiliation of a respedt
  @staticmethod
  def delete_respEdt_and_promo(idResp, idPromo):
        try:
            # Use delete() directly on the association table
            db.session.query(affiliation_resp_edt).filter(
                (affiliation_resp_edt.c.id_resp == idResp) &
                (affiliation_resp_edt.c.id_promo == idPromo)
            ).delete(synchronize_session=False)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e