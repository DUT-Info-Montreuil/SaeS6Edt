from models.relations.affiliation_resp_edt import affiliation_resp_edt
from database.config import db 
from services.AffiliationRespEdtService import AffiliationRespEdtService


dataAffiliationRespEdtINFO = [
    {"id_resp": i, "id_promo": 1} for i in range(1, 7)
] + [
    {"id_resp": j, "id_promo": 2} for j in range(1, 7)
] + [
    {"id_resp": k, "id_promo": 3} for k in range(1, 7)
] + [
    {"id_resp": h, "id_promo": 4} for h in range(1, 7)
] + [
    {"id_resp": x, "id_promo": 5} for x in range(1, 7)
] + [
    {"id_resp": y, "id_promo": 6} for y in range(1, 7)
]

dataAffiliationRespEdtINFOCOM = [
    {"id_resp": i, "id_promo": 7} for i in range(7, 9)
] + [
    {"id_resp": j, "id_promo": 8} for j in range(7, 9)
] + [
    {"id_resp": k, "id_promo": 9} for k in range(7, 9)
] + [
    {"id_resp": h, "id_promo": 10} for h in range(7, 9)
] + [
    {"id_resp": x, "id_promo": 11} for x in range(7, 9)
] + [
    {"id_resp": y, "id_promo": 12} for y in range(7, 9)
]

dataAffiliationRespEdtQLIO = [
    {"id_resp": i, "id_promo": 13} for i in range(9, 12)
] + [
    {"id_resp": j, "id_promo": 14} for j in range(9, 12)
] + [
    {"id_resp": k, "id_promo": 15} for k in range(9, 12)
] + [
    {"id_resp": h, "id_promo": 16} for h in range(9, 12)
] + [
    {"id_resp": x, "id_promo": 17} for x in range(9, 12)
] + [
    {"id_resp": y, "id_promo": 18} for y in range(9, 12)
]

dataAffiliationRespEdtGACO = [
    {"id_resp": i, "id_promo": 19} for i in range(12, 19)
] + [
    {"id_resp": j, "id_promo": 20} for j in range(12, 19)
] + [
    {"id_resp": k, "id_promo": 21} for k in range(12, 19)
] + [
    {"id_resp": h, "id_promo": 22} for h in range(12, 19)
] + [
    {"id_resp": x, "id_promo": 23} for x in range(12, 19)
] + [
    {"id_resp": y, "id_promo": 24} for y in range(12, 19)
]


for respEdt in dataAffiliationRespEdtINFO:
    idResp = respEdt["id_resp"]
    id_promo = respEdt["id_promo"]
    AffiliationRespEdtService.affiliate_respedt_to_promo(idResp,id_promo)

for respEdt in dataAffiliationRespEdtINFOCOM:
    idResp = respEdt["id_resp"]
    id_promo = respEdt["id_promo"]
    AffiliationRespEdtService.affiliate_respedt_to_promo(idResp,id_promo)

for respEdt in dataAffiliationRespEdtQLIO:
    idResp = respEdt["id_resp"]
    id_promo = respEdt["id_promo"]
    AffiliationRespEdtService.affiliate_respedt_to_promo(idResp,id_promo)

for respEdt in dataAffiliationRespEdtGACO:
    idResp = respEdt["id_resp"]
    id_promo = respEdt["id_promo"]
    AffiliationRespEdtService.affiliate_respedt_to_promo(idResp,id_promo)
    

