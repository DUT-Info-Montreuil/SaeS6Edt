from database.config import db
from models.User import User

class Student(User):
    __tablename__= "student"
    id_student = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    INE = db.Column(db.String(64), unique=True, nullable=False)
    # etudiantGroupe = db.relationship('EtudiantGroupe', backref='etudiant_appartient_groupe', lazy='dynamic')
    # absence = db.relationship('Absence', backref='idUser', lazy='dynamic')


    def __init__(self,INE, role="ROLE_STUDENT", **kwargs):
        super().__init__(role=role,**kwargs)
        self.INE = INE


    def to_dict(self):
        return {
            'id': self.id_student,
            'user' :super().to_dict()
        }

    