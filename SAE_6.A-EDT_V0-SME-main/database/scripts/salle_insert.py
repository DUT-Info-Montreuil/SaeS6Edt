from models.Salle import Salle
from database.config import db 
from services.SalleService import SalleService



dataSalles = [
    {
      "name": "A2-01",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    },
    {
      "name": "A2-02",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    },
    {
      "name": "A2-03",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    },
    {
      "name": "A2-04",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    },
    {
      "name": "A2-05",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    },
    {
      "name": "A2-06",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    },
    {
      "name": "A2-07",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    },
    {
      "name": "A2-08",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    },
    {
      "name": "A2-09",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    },
    {
      "name": "A2-10",
      "ordi": 20,
      "tableauNumerique": 0,
      "videoProjecteur": 1
    }
]


for salles in dataSalles:



    SalleService.create_salle(salles)

    