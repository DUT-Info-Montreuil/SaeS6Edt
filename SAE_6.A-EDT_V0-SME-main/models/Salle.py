from database.config import db

# Le modèle Salle représente une salle associée à des cours
class Salle(db.Model):
    __tablename__= "salle"

    nom = db.Column(db.String(64), primary_key=True)
    ordi = db.Column(db.Integer, nullable=True)
    tableauNumerique = db.Column(db.Integer, nullable=True)
    videoProjecteur = db.Column(db.Integer, nullable=True)
    cours = db.relationship('Cours', backref='salle_name', lazy='dynamic')

    # Constructeur de la classe Salle
    def __init__(self, name, ordi, tableauNumerique, videoProjecteur, **kwargs):
        self.nom = name
        self.ordi = ordi
        self.tableauNumerique = tableauNumerique
        self.videoProjecteur = videoProjecteur

    # Convertit l'objet Salle en un dictionnaire
    def to_dict(self):
        return {
            'nom': self.nom,
            'ordi': self.ordi,
            'tableauNumerique': self.tableauNumerique,
            'videoProjecteur': self.videoProjecteur
        }