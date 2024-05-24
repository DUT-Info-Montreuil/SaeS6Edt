from models.relations.student_absences import student_absences_cours
from database.config import db 
from services.StudentAbsencesCoursService import StudentAbsencesCoursService


dataStudentAbsencesCours = []


for student_absences_cours in dataStudentAbsencesCours:

    idStudent = student_absences_cours["id_student"]
    idCours = student_absences_cours["id_cours"]
    StudentAbsencesCoursService.add_absence_to_cours(idStudent,idCours)
