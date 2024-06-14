from models.relations.affiliation_resp_edt import affiliation_resp_edt
from database.config import db 
from services.AffiliationRespEdtService import AffiliationRespEdtService


dataAffiliationRespEdt = [
    {
        "id_resp": 1,
        "id_promo": 1
    }, 
    {
        "id_resp": 2,
        "id_promo": 1
    }
]


for respEdt in dataAffiliationRespEdt:

    id_resp = respEdt["id_resp"]
    id_promo = respEdt["id_promo"]
    existing_affiliateRespEdtAffiliate = affiliation_resp_edt.query.filter_by(id_resp=respEdt['id_resp'], id_promo=respEdt['id_promo']).first()
    if not existing_affiliateRespEdtAffiliate:
        AffiliationRespEdtService.affiliate_respedt_to_promo(id_resp,id_promo)
    else:
        print(f"Affiliation between ResponsableEdt {respEdt['id_resp']} and Promotion {respEdt['id_promo']} already exists.")

