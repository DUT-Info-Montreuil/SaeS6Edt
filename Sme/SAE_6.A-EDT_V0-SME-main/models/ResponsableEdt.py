from database.config import db
from models.Staff import Staff


class ResponsableEdt(Staff):
  __tablename__ = "responsable_edt"
  id_resp = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
  id_staff = db.Column(db.Integer, db.ForeignKey('staff.id', ondelete='CASCADE'))
  # groupes = db.relationship('Groupe', backref='responsable_edt', lazy='dynamic')
  



  def __init__(self,role="ROLE_RESP_EDT", **kwargs):
    super().__init__(role=role,**kwargs)
    self.id = super().id

  def to_dict(self):
    return {
        'id': self.id_resp,
        'staff':super().to_dict(),
    }