from sqlalchemy import update
from models.Promotion import Promotion
from models.Groupe import Groupe
from models.User import User
from models.Student import Student
from services.AffiliationRespEdtService import AffiliationRespEdtService
from services.AffRessourcePromoService import AffRessourcePromoService
from services.GroupeService import GroupeService
from database.config import db
from models.relations.user_groupe import student_course_association
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import aliased
import random

from services.PromotionService import PromotionService


class UserGroupeService:

    @staticmethod
    def add_user_to_group(user_id, group_id):
        # Create an instance of the user_groupe table
        user_group_association = student_course_association.insert().values(id_student=user_id, id_group=group_id)

        # Add the association to the database session
        db.session.execute(user_group_association)

        # Commit the changes to the database
        db.session.commit()

    # Vérifie qu'un étudiant fait partie d'un groupe
    @staticmethod
    def get_groupe_etudiant(idStudent,idGroupe):
        return student_course_association.query.filter_by(idStudent=idStudent).filter_by(idGroupe=idGroupe).first()

    # Récupère les groupes d'un étudiant
    @staticmethod
    def get_groupes_for_student(idStudent):
        query = db.session.query(student_course_association).filter_by(id_student=idStudent)

        result = query.all()
        groupes = [id_group for id_student, id_group in result]
        groupes_tree_list = []
        for groupe in groupes:
            if groupe not in groupes_tree_list:
                groupes_tree_list.append(groupe)
            #Add the groupe id to the list no duplicates
            for groupe_tree in GroupeService.get_parents_list(groupe):
                if groupe_tree not in groupes_tree_list:
                    groupes_tree_list.append(groupe_tree)

        return groupes_tree_list

    # Vérifie qu'un groupe possède bien un étudiant
    @staticmethod
    def get_etudiant_by_groupe(idGroupe, idStudent):
        return student_course_association.query.filter_by(idGroupe=idGroupe).filter_by(idStudent=idStudent).all()

    # Modifie le groupe d'un étudiant
    @staticmethod
    def update_student_group(student_id, new_group_id, old_group_id):
        try:
            db.session.execute(
                student_course_association.update().where(
                    (student_course_association.c.id_student == student_id) &
                    (student_course_association.c.id_group == old_group_id)
                ).values(id_group=new_group_id)
            )
            db.session.commit()
            return {"message": "Groupe d'étudiants mis à jour avec succès"}
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}


    # @staticmethod
    # def delete_user_groupe(idStudent):
    #   try:
    #       # Utilisez delete() directement sur la table d'association
    #       table = Student.query.join(student_course_association).join(Groupe).filter((student_course_association.c.id_student == Student.id_student) & (student_course_association.c.id_group == Groupe.id)).all()
    #       table.query.filter_by(id_student=idStudent).delete()
    #       db.session.commit()
    #   except Exception as e:
    #       db.session.rollback()
    #       raise e

    # Supprime les groupes auxquels un étudiant fait partie
    @staticmethod
    def delete_user_groupe(idStudent):
        try:
            # Use delete() directly on the association table
            db.session.query(student_course_association).filter(
                (student_course_association.c.id_student == idStudent) &
                (student_course_association.c.id_group == Groupe.id)
            ).delete(synchronize_session=False)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e




    # @staticmethod
    # def get_etudiants_for_groupe(idGroupe):
    #   query = db.session.query(Student.name, Student.lastname).join(student_course_association).filter(student_course_association.c.id_group == idGroupe)
    #   result = query.all()

    #   etudiants_list = [{"name": name, "lastname": lastname} for name, lastname in result]

    #   return etudiants_list

    # Récupère les étudiants d'un groupe
    @staticmethod
    def get_etudiants_for_groupe(idGroupe):
        query = db.session.query(
            student_course_association.c.id_group,
            Student.id_student,
            Student.name,
            Student.lastname
        ).join(Student).filter(student_course_association.c.id_group == idGroupe)

        result = query.all()

        etudiants_list = [{"id_group": id_group, "id_student": id_student, "name": name, "lastname": lastname} for id_group, id_student, name, lastname in result]

        return etudiants_list

    # @staticmethod
    # def modifier_etudiant_groupe(idStudent, idGroupe):
    #   user_groupe_to_modify = student_course_association.query.filter_by(idStudent=idStudent).first()

    #   user_groupe_to_modify.idGroupe = idGroupe
    #   db.session.commit()

    # Migre des étudiants d'une promotion à une autre

    @staticmethod
    def obtenir_mot_apres_but(chaine):
        mots = chaine.split()
        indice_but = mots.index("BUT")
        return mots[indice_but + 1]

    @staticmethod
    def update_promo_etudiants(idAncPromo, idNvPromo):
        # Get the old promotion
        old_promo = PromotionService.get_promo_by_id(idAncPromo)
        new_promo = PromotionService.get_promo_by_id(idNvPromo)

        # Récupère les ressources associés à la promo de l'année d'avant et les associes à la nouvelle promo
        promosAnneeAvant = PromotionService.get_promo_by_year(new_promo.year - 1)
        for oldPromo in promosAnneeAvant:
            if oldPromo.niveau == new_promo.niveau:
                
                oldPromoGroupName = UserGroupeService.obtenir_mot_apres_but(GroupeService.get_groupe_by_id(oldPromo.id_groupe).name)
                newPromoGroupName = UserGroupeService.obtenir_mot_apres_but(GroupeService.get_groupe_by_id(new_promo.id_groupe).name)

                if oldPromoGroupName == newPromoGroupName:
                    AffRessourcePromoService.change_promotion_for_all_resources_in_promo(oldPromo.id_promo, new_promo.id_promo)

        # Get the groups of the old promotion
        groups_id_of_old_promo = GroupeService.get_tree(idAncPromo)
        groups_of_old_promo = []
        for group in groups_id_of_old_promo:
            group_to_copy = GroupeService.get_groupe_by_id(group)
            groups_of_old_promo.append(group_to_copy)

        td = []
        tp = []

        # Différencier les groupes TD et TP
        for group in groups_of_old_promo:
            if group.id_group_parent is not None and len(GroupeService.get_children(group.id)['children'])>0:
                td.append(group)
            elif group.id_group_parent is not None and len(GroupeService.get_children(group.id)['children'])==0:
                tp.append(group)

        for group in td:
            GroupeService.create_groupe({"name":group.name, "id_group_parent":new_promo.id_groupe})
            new_td = Groupe.query.order_by(Groupe.id.desc()).first()

            students_of_td = UserGroupeService.get_etudiants_for_groupe(group.id)

            for student in students_of_td:
                UserGroupeService.update_student_group(student['id_student'], new_td.id, group.id)  

            
            for group2 in tp:
                if group2.id_group_parent == group.id:
                    new_tp=group2.duplicate()
                    new_tp.id_group_parent=new_td.id
                    db.session.add(new_tp)
                    
                students_of_tp = UserGroupeService.get_etudiants_for_groupe(group2.id)

                for student in students_of_tp:
                    UserGroupeService.update_student_group(student['id_student'], new_tp.id, group2.id)
        
                        
        db.session.commit()

        return GroupeService.get_tree(new_promo.id_groupe)  