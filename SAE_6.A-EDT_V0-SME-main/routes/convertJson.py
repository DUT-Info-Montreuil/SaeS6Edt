from flask import Blueprint
from flask_jwt_extended import (create_access_token)
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, request, jsonify
from database.config import db
import json
import datetime
import re 
from services.TeacherService import TeacherService
import requests
#TO REMOVE 
from discord_webhook import DiscordWebhook

convert_bp = Blueprint('convertJson', __name__)

""" {
        d"appelEffectue": false,
        d"end_time": "2024-05-30 16:06:00",
        "evaluation": false,
        "id": 21,
        "id_enseignant": 1,
        "id_group": 1,
        d"initial_ressource": "R3-01",
        "is_published": 0,
        d"name_salle": "A2-01",
        d"start_time": "2024-05-30 14:04:00"
    }"""


@convert_bp.route("/convert", methods=['POST'])
def converFlopToEdt():
    j = request.json.get('j')
    dept = request.json.get('dept')
    print(j)
    print(dept)
    flop = j
    #flop = json.loads(j)
    print(flop)
    edtResult = {}
    edtResult["appelEffectue"] = False
    edtResult["name_salle"] = flop["room"]["name"]
    edtResult["initial_ressource"] = flop["course"]["module"]["name"]
    d = str(flop["course"]["year"])+"-W"+str(flop["course"]["week"])
    r = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
    r = r + datetime.timedelta(minutes=int(flop["start_time"]))
    edtResult["start_time"] = r.strftime('%Y-%m-%d %H:%M:%S')
    r = r + datetime.timedelta(minutes=int(re.sub('\D', '', flop["course"]["type"])))
    edtResult["end_time"] = r.strftime('%Y-%m-%d %H:%M:%S')
    edtResult["evaluation"] = flop["course"]["is_graded"]
    idWebhook = "https://discord.com/api/webhooks/1250811831686008945/-L8gkLMTSR4ZDGr9UbtQpsRAT2Lvz1jjJroQu_A0IbvvjHCiVi3KurhL-KRpqsySAZ7Y"
    webhook = DiscordWebhook(url=idWebhook, content="https://flopedt.iut.univ-paris8.fr/fr/api/user/tutor/?dept="+dept+"&week="+str(flop["course"]["week"])+"&year="+str(flop["course"]["year"] )
)
    response = webhook.execute()
    allWeekProf = requests.get("https://flopedt.iut.univ-paris8.fr/fr/api/user/tutor/?dept="+dept+"&week="+str(flop["course"]["week"])+"&year="+str(flop["course"]["year"] ),  verify=False)
    

    webhook = DiscordWebhook(url=idWebhook, content=allWeekProf.json())
    response = webhook.execute()
    
    allWeekProf.json()

    """
#test = requests.get("https://catfact.ninja/fact")
    
    for p in  allWeekProf :
        if (p["username"] == flop["tutor"]):
            t = TeacherService.get_by_user_name(p["first_name"], p["last_name"])
            edtResult["id_enseignant"] = t.id_teacher
            edtResult["enseignant"] = t.username
        """    
           
    return edtResult

 
    
"""
 {
        "id": 1041,
        "room": {
            "id": 186,
            "name": "Amphi2"
        },
        "start_time": 670,
        "day": "tu",
        "course": {
            "id": 1019,
            "type": "CM90",
            "room_type": "CoursInfo",
            "week": 14,
            "year": 2024,
            "groups": [
                {
                    "id": 23,
                    "train_prog": "BUT1",
                    "name": "S2Cours",
                    "is_structural": true
                }
            ],
            "supp_tutor": [],
            "module": {
                "name": "Interactions Hommes Machines",
                "abbrev": "R202",
                "display": {
                    "color_bg": "#8fba06",
                    "color_txt": "#000000"
                }
            },
            "pay_module": null,
            "is_graded": false
        },
        "tutor": "MS",
        "id_visio": null,
        "number": 1
    },





   

    {
        "appelEffectue": false,
        "end_time": "2024-05-31 15:09:00",
        "evaluation": false,
        "id": 11,
        "id_enseignant": 1,
        "id_group": 1,
        "initial_ressource": "R3-02",
        "is_published": 0,
        "name_salle": "A2-03",
        "start_time": "2024-05-31 14:08:00"
    }

}
"""


