from database.config import db



affiliation_resp_edt = db.Table(
    'affiliation_resp_edt',
    db.Column('id_resp', db.BigInteger, db.ForeignKey('responsable_edt.id_resp')),
    db.Column('id_promo', db.Integer, db.ForeignKey('promotion.id_promo'))
)