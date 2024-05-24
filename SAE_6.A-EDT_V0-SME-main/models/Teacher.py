from database.config import db
from models.Staff import Staff

class Teacher(Staff):
    __tablename__= "teacher"
    id_teacher = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('staff.id', ondelete='CASCADE'), nullable=False)
    nb_heures_previsionnelles = db.Column(db.Integer, nullable=True)
    nb_heure_effectue = db.Column(db.Integer, nullable=False, default=0)
    activated = db.Column(db.Boolean, nullable=False, default=False)
    #disponibilite = db.relationship('Disponibilite', backref='disponibilite_enseignant', lazy='dynamic')
    cours = db.relationship('Cours', backref='enseignant_id', lazy='dynamic')


    def __init__(self,role="ROLE_TEACHER",activated= True, **kwargs):
        super().__init__(role=role,**kwargs)
        self.activated = activated


    def to_dict(self):
        return {
            'id': self.id_teacher,
            'staff' :super().to_dict(),
            "activated": self.activated,
        }

    