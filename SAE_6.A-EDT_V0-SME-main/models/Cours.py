from database.config import db
from models.Ressources import Ressources
from models.Groupe import Groupe
from models.Salle import Salle
from models.Teacher import Teacher
from datetime import datetime


class Cours(db.Model):

    __tablename__= "cours"
    
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    id_enseignant = db.Column(db.BigInteger, db.ForeignKey('teacher.id_teacher'), nullable=True)
    initial_ressource = db.Column(db.String(64), db.ForeignKey('ressources.initial'), nullable=False)
    id_group = db.Column(db.Integer, db.ForeignKey('groupe.id'), nullable=False)
    name_salle = db.Column(db.String(64), db.ForeignKey("salle.nom"), nullable=True)
    appelEffectue = db.Column(db.Boolean, nullable=False, default=False)
    is_published = db.Column(db.Integer, nullable=False, default=0)
    evaluation = db.Column(db.Boolean, nullable=False, default=False)

    # absences = db.relationship('Absence', backref='cours', lazy='dynamic')

    def __init__(self, start_time, end_time, initial_ressource, id_group, name_salle = None,id_enseignant= None,is_published=False, evaluation = False, **kwargs):
        if type(start_time) == str:
            self.start_time = datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S")
        else:
            self.start_time = start_time
        if type(end_time) == str:
            self.end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        else:
            self.end_time = end_time
        self.id_enseignant = id_enseignant if id_enseignant else db.null()
        self.initial_ressource = initial_ressource
        self.id_group = id_group
        self.name_salle = name_salle if name_salle else db.null()
        self.is_published = is_published
        self.evaluation = evaluation

    # def appelFait(self, appelFait):
    #     self.appelEffectue = appelFait

    def to_dict(self):
        return {
            'id': self.id,
            'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'id_enseignant': self.id_enseignant,
            'initial_ressource': self.initial_ressource,
            'id_group': self.id_group,
            'name_salle': self.name_salle,
            'appelEffectue': self.appelEffectue,
            'is_published': self.is_published,
            'evaluation': self.evaluation,
        }
    def duplicate(self):
        # Créer une nouvelle instance de la classe avec les mêmes attributs
        new_course = Cours(self.start_time, self.end_time, self.initial_ressource, self.id_group, self.name_salle, self.id_enseignant, self.is_published, self.evaluation)
        return new_course
