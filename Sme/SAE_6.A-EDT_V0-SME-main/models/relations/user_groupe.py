from database.config import db


student_course_association = db.Table(
    'user_groupe',
    db.Column('id_student', db.BigInteger, db.ForeignKey('student.id_student')),
    db.Column('id_group', db.Integer, db.ForeignKey('groupe.id'))
)