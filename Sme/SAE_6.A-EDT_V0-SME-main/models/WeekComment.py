from database.config import db
# from models.Enseignant import Enseignant

class WeekComment(db.Model):
    __tablename__ = "week_comment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_promo = db.Column(db.Integer, db.ForeignKey('promotion.id_promo'), nullable=False)
    week_number = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(255), nullable=False)

    def __init__(self, week_number, year, content, id_promo):
        self.week_number = week_number
        self.year = year
        self.content = content
        self.id_promo = id_promo

    def to_dict(self):
        return {
            'id': self.id,
            'week_number': self.week_number,
            'year': self.year,
            'content': self.content,
            'id_promo': self.id_promo
        }
        
  