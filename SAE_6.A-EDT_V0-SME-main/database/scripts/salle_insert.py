from models.Salle import Salle
from database.config import db 
from services.SalleService import SalleService



dataSalles = [
    {
      "nom": "A2-01",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    },
    {
      "nom": "A2-02",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    },
    {
      "nom": "A2-03",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    },
    {
      "nom": "A2-04",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    },
    {
      "nom": "A2-05",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    },
    {
      "nom": "A2-06",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    },
    {
      "nom": "A2-07",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    },
    {
      "nom": "A2-08",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    },
    {
      "nom": "A2-09",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    },
    {
      "nom": "A2-10",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    }
]


for salles in dataSalles:
    existing_salle = Salle.query.filter_by(nom=salles['nom']).first()
    if not existing_salle:
        SalleService.create_salle(salles)
    else:
        print(f"Salle with name {salles['nom']} already exists.")


    