from models.relations.user_groupe import student_course_association
from database.config import db 
from services.UserGroupeService import UserGroupeService

dataEtudiantGroupe = []


for etudiantGroupe in dataEtudiantGroupe:
    
    idStudent = etudiantGroupe["id_student"]
    idGroup = etudiantGroupe["id_group"]

    UserGroupeService.add_user_to_group(idStudent,idGroup)

