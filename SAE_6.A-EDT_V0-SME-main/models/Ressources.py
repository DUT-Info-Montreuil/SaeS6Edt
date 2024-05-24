from database.config import db
from models.Groupe import Groupe

# Le modèle Ressources représente une ressource associée à une promotion ou un groupe
class Ressources(db.Model):
    __tablename__= "ressources"

    # Clé primaire : Initial de la ressource (par exemple, "R5A12", "R5A09", ...)
    initial = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    id_promo = db.Column(db.Integer, db.ForeignKey('promotion.id_promo'), nullable=True)
    cours = db.relationship('Cours', backref='ressource_initial', lazy='dynamic')
    color = db.Column(db.String(64), nullable=False)


    # Constructeur de la classe Ressources
    def __init__(self, name, initial, color,  **kwargs):
        self.name=name
        self.initial = initial
        self.color = color

    
    # Convertit l'objet Ressources en un dictionnaire
    def to_dict(self):
        return {
            'initial': self.initial,
            'name': self.name,
            'color':self.color
        }

    
