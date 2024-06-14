from models.Groupe import Groupe
from database.config import db 
from services.GroupeService import GroupeService

dataGroupes = [
    {
      "name": "A",
      "id": 7,
      "id_group_parent": 1
    },
    {
      "name": "B",
      "id": 8,
      "id_group_parent": 1
    },
    {
      "name": "C",
      "id": 9,
      "id_group_parent": 1
    },
    {
      "name": "D",
      "id": 10,
      "id_group_parent": 1
    }
]


for groupe in dataGroupes:
    existing_groupe = Groupe.query.filter_by(name=groupe['name']).first()
    if not existing_groupe:
        GroupeService.create_groupe(groupe)
    else:
        print(f"Groupe with name {groupe['name']} already exists.")
    