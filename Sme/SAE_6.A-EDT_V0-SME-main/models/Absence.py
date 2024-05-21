from database.config import db 
from models.Cours import Cours
from models.Student import Student

# Le modèle Absence représente une absence d'un étudiant à un cours spécifique

class Absence(db.Model):
    __tablename__= "absence"

    # Clé primaire composée : ID de l'étudiant et ID du cours
    idEtudiant = db.Column(db.BigInteger, db.ForeignKey('student.id_student'), primary_key=True)
    idCour = db.Column(db.Integer, db.ForeignKey('cours.id'), primary_key=True)
    
    # Champ indiquant si l'absence est justifiée (True) ou non (False)
    justifiée = db.Column(db.Boolean)

    # Constructeur de la classe Absence
    def __init__(self, idEtudiant, idCour):
        self.idEtudiant = idEtudiant
        self.idCour = idCour
        self.justifiée = False