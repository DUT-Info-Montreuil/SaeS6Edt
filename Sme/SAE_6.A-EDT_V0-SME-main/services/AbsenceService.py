from database.config import db 
from models.Absence import Absence

class AbsenceService:

    # Récupère toutes les absences pour un étudiant donné
    @staticmethod
    def get_all_absences(idEtudiant):
        return Absence.query.filter_by(idEtudiant=idEtudiant).all()
    
    # Crée une nouvelle absence pour un étudiant donné et un cours donné
    @staticmethod
    def create_absence(idEtudiant, idCours):
        absence = Absence(idEtudiant, idCours)

        db.session.add(absence)
        db.session.commit()

        return absence
    
    # Justifie une absence pour un étudiant donné et un cours donné
    @staticmethod
    def justify_absence(idEtudiant, idCours):
        absence_to_justify = Absence.query.filter_by(idEtudiant=idEtudiant, idCour=idCours).first()

        absence_to_justify.justifée = True

        db.session.commit()

    # Supprime une absence pour un étudiant donné et un cours donné.
    @staticmethod
    def delete_absence(idEtudiant, idCours):
        absence_to_delete = Absence.query.filter_by(idEtudiant=idEtudiant, idCour=idCours).first()
        db.session.delete(absence_to_delete)
        db.session.commit()

    # Modifie l'absence associée à un étudiant et un cours donnés en remplaçant le cours par un nouveau.
    @staticmethod
    def modify_absence(idEtudiant, idCours, newIdCours):
        absence_to_correct = Absence.query.filter_by(idEtudiant=idEtudiant, idCour=idCours).first()
        absence_to_correct.idCour = newIdCours
        db.session.commit()
