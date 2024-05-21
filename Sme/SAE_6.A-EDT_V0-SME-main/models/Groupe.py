from database.config import db

# Le modèle Groupe représente une unité de regroupement dans le contexte d'un groupe d'étudiant venant d'une promotion
class Groupe(db.Model):
    __tablename__= "groupe"

    name = db.Column(db.String(64))

    # Clé primaire : ID du groupe
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Clé étrangère : l'ID du groupe parent
    id_group_parent = db.Column(db.Integer, db.ForeignKey('groupe.id', ondelete='CASCADE'), nullable=True)


    

    # cours = db.relationship('Cours', backref='groupe_assigne_cour', lazy='dynamic')
    
    # Constructeur de la classe Groupe
    def __init__(self, name, id_group_parent, **kwargs):
        if id_group_parent: 
            if Groupe.query.get(id_group_parent) == None:
                raise Exception("Groupe parent does not exist")
        else:
            id_group_parent = db.null()

        self.name = name
        self.id_group_parent = id_group_parent

    # Convertit l'objet Groupe en un dictionnaire
    def to_dict(self, key = None, value = None):
        return {
            'id': self.id,
            'name': self.name,
            'id_group_parent': self.id_group_parent,        
        }
    
    # Duplique l'objet Groupe
    def duplicate(self):
        new_group = Groupe(self.name, self.id_group_parent)
        return new_group
        