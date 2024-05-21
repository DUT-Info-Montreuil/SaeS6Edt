from models.relations.ressource_promo import affiliation_ressource_promo
from database.config import db 
from services.AffRessourcePromoService import AffRessourcePromoService

data = [
    {
        "id_ressource" : "R3-01",
        "idPromo" : 1
    },
    {
        "id_ressource" : "R3-02",
        "idPromo" : 1
    },
    {
        "id_ressource" : "R3-03",
        "idPromo" : 1
    },
    {
        "id_ressource" : "R3-04",
        "idPromo" : 1
    },
    {
        "id_ressource" : "R3-05",
        "idPromo" : 1
    },
    {
        "id_ressource" : "R3-06",
        "idPromo" : 1
    },
    {
        "id_ressource" : "R3-07",
        "idPromo" : 1
    },
    {
        "id_ressource" : "R3-08",
        "idPromo" : 1
    },
    {
        "id_ressource" : "R3-09",
        "idPromo" : 1
    },
    {
        "id_ressource" : "R3-10",
        "idPromo" : 1
    }
]

for aff in data:
    initial = aff["id_ressource"]
    idPromo = aff["idPromo"]
    AffRessourcePromoService.affiliate_ressource_to_promo(initial, idPromo)