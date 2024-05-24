from database.config import db
from models.relations.student_absences import student_absences_cours

class StudentAbsencesCoursService:

  @staticmethod
  def add_absence_to_cours(student_id, cours_id):
    # Create an instance of the user_groupe table
    student_absences_association = student_absences_cours.insert().values(id_student=student_id, id_cours=cours_id)

    # Add the association to the database session
    db.session.execute(student_absences_association)

    # Commit the changes to the database
    db.session.commit()

  # Réccupère l'absence d'un étudiant à un cours
  @staticmethod
  def get_student_absences_by_cours(idStudent,idCours):
    return student_absences_cours.query.filter_by(id_student=idStudent).filter_by(id_cours=idCours).all()
  # Récupère les cours auxquels un étudiant est absent
  @staticmethod
  def get_cours_by_student_absences(idStudent,idCours):
    return student_absences_cours.query.filter_by(id_cours=idCours).filter_by(id_student=idStudent).all()

  # Supprime l'absence d'un étudiant à un cours
  @staticmethod
  def delete_absences_cours(idStudent,idCours):
    absences_delete = student_absences_cours.filter_by(id_student=idStudent).filter_by(id_cours=idCours).first()

    db.session.delete(absences_delete)
    db.session.commit() 