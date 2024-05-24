from models.Ressources import Ressources
from database.config import db 
from services.RessourcesService import RessourcesService


dataRessources = [

  {
    "initial": "R3-01",
    "name": "Modélisation",
    "id_promo": 1,
    "color": "#FF8080"
  },
  {
    "initial": "R3-02",
    "name": "Dev Mobile",
    "id_promo": 1,
    "color": "#80FF80"
  },
  {
    "initial": "R3-03",
    "name": "Data Science",
    "id_promo": 1,
    "color": "#8080FF"
  },
  {
    "initial": "R3-04",
    "name": "IA",
    "id_promo": 1,
    "color": "#000000"
  },
  {
    "initial": "R3-05",
    "name": "Cybersécurité",
    "id_promo": 1,
    "color": "#FF80FF"
  },
  {
    "initial": "R3-06",
    "name": "Web Développement",
    "id_promo": 1,
    "color": "#80FFFF"
  },
  {
    "initial": "R3-07",
    "name": "Réseaux",
    "id_promo": 1,
    "color": "#C00000"
  },
  {
    "initial": "R3-08",
    "name": "Cloud Computing",
    "id_promo": 1,
    "color": "#00C000"
  },
  {
    "initial": "R3-09",
    "name": "Big Data",
    "id_promo": 1,
    "color": "#0000C0"
  },
  {
    "initial": "R3-10",
    "name": "Blockchain",
    "id_promo": 1,
    "color": "#C0C000"
  }

]


for ressource in dataRessources:
    RessourcesService.create_resource(ressource)