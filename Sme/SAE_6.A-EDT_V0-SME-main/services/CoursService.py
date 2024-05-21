from sqlalchemy import and_, or_
from models.Teacher import Teacher

from services.UserGroupeService import UserGroupeService

from database.config import db
from models.Cours import Cours
from datetime import datetime, timedelta

from services.GroupeService import GroupeService
from services.AffiliationRespEdtService import AffiliationRespEdtService
from services.ResponsableEdtService import ResponsableEdtService
from services.TeacherService import TeacherService

class CoursService:

    # Crée un nouveau cours avec les données fournies.
    @staticmethod
    def create_course(data):
        resp, code = CoursService.can_create_course(**data)
        if code >= 400:
            return resp, code

        course = Cours(**data)
        
        db.session.add(course)
        db.session.commit()

        result = course.to_dict()
        if code > 200:
            result.update(resp)
            return result, code

        return course, 200
    
    # Récupère un cours par son identifiant
    def get_course_by_id(id):
        return Cours.query.get(id)
    
    # Récupère tous les cours en fonction des paramètres spécifiés
    @staticmethod
    def get_all_courses(args,user):

        query = Cours.query

        if 'date_min' in args:
            date_start = datetime.strptime(args["date_min"], '%Y-%m-%d')
            query = query.filter(Cours.end_time >= date_start)

        if 'date_max' in args:
            date_end = datetime.strptime(args["date_max"], '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Cours.start_time < date_end)

        # if publish:
        #     query = query.filter(Cours.is_published == publish)

        if 'room' in args:
            query = query.filter(Cours.name_salle == args["room"])
        if 'teacher' in args:
            query = query.filter(Cours.id_enseignant == args["teacher"])
        if 'group' in args:
            id_groups = GroupeService.get_tree(args["group"])
            query = query.filter(Cours.id_group.in_(id_groups))
        if 'resource' in args:
            query = query.filter(Cours.initial_ressource == args["resource"])
        
        if user.role == "ROLE_RESP_EDT":
            # respedt = ResponsableEdtService.get_by_userId(user.id)
            # promos = AffiliationRespEdtService.get_promos_for_respedt(respedt.id_resp)
            # id_groups = [promo.id_group for promo in promos]

            # query = query.filter(Cours.id_group.in_(GroupeService.get_tree(user.id_group)))
            query = query.filter(or_(Cours.is_published == 0, Cours.is_published == 1))
        else:
            if user.role == "ROLE_TEACHER":
                if not 'method' in args or args["method"] == "default":
                    teacher = TeacherService.get_by_user_id(user.id)
                    query = query.filter(Cours.id_enseignant == teacher.id_teacher)

            else:
                 if not 'method' in args or args["method"] == "default":
                    query = query.filter(Cours.id_group.in_(UserGroupeService.get_groupes_for_student(user.id)))

            query = query.filter(or_(Cours.is_published == 2, Cours.is_published == 1))
        

        return query.all()
    
    # Supprime un cours de la base de données par son identifiant
    @staticmethod
    def delete_course(id):
        course = Cours.query.get(id)
        if course.is_published == 1:
            course.is_published = 2
        else:
            db.session.delete(course)
        db.session.commit()
        
        return course
    
    # Met à jour un cours avec les nouvelles données fournies
    @staticmethod
    def update_course(id, start_time, end_time, initial_ressource, id_group, name_salle = None,id_enseignant= None, evaluation= False, **kwargs):
        course = Cours.query.get(id)
        code = 0
        if(kwargs.get('isInDraft') == False):
            resp, code = CoursService.can_create_course(start_time=start_time, end_time=end_time, id_group=id_group, name_salle=name_salle, id_enseignant=id_enseignant, id_cours=id)
        if code >= 400:
            return resp, code
        
        course_duplicate = course.duplicate() if course.duplicate() is not None else None

        course_duplicate.start_time = start_time
        course_duplicate.end_time = end_time
        course_duplicate.id_enseignant = id_enseignant if id_enseignant else db.null()
        course_duplicate.initial_ressource = initial_ressource
        course_duplicate.id_group = id_group
        course_duplicate.name_salle = name_salle if name_salle else db.null()
        course_duplicate.is_published = 0
        course_duplicate.evaluation = evaluation

        db.session.add(course_duplicate)
        db.session.commit()

        
        CoursService.delete_course(course.id)


        result = course_duplicate.to_dict()
        if code > 200:
            result.update(resp)
            return result, code

        return course_duplicate, 200
    
    # Vérifie si un cours peut être créé avec les paramètres spécifiés
    @staticmethod
    def can_create_course(start_time, end_time, id_group, name_salle, id_enseignant, id_cours= None,   **kwargs):

        if type(start_time) != str:
            start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        if type(end_time) != str:
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

        if start_time >= end_time:
            return {"response" : "start_time doit être inférieur à end_time"}, 400

        try:
            group_depends = GroupeService.get_tree(id_group)
        except Exception as e:
            print(e)
            return {"response" : "Groupe introuvable"}, 404
            


        warning: str = ""

        for group in group_depends:

            if id_cours==None:
                query = Cours.query
            else:
                query = Cours.query.filter(Cours.id != id_cours).filter(Cours.is_published != 2)

            current_group = GroupeService.get_groupe_by_id(group)
            #Si un cours est déjà prévu entre start_time et end_time
            courses = query.filter(Cours.id_group==group).filter(and_(Cours.start_time >= start_time, Cours.start_time < end_time)).all()
 
            if len(courses) > 0: 
                return {"error" :f"Le groupe {current_group.name} à déjà cours !"}, 409
            
            courses = query.filter(Cours.id_group==group).filter(and_(Cours.end_time > start_time, Cours.end_time <= end_time)).all()

            if len(courses) > 0:
                return {"error" :f"Le groupe {current_group.name} à déjà cours !"}, 409
            
            courses = query.filter(Cours.id_group==group).filter(and_(Cours.start_time <= start_time, Cours.end_time >= end_time)).all()

            if len(courses) > 0:
                return {"error" :f"Le groupe {current_group.name} à déjà cours !"}, 409

            courses = query.filter(Cours.id_group==group).filter(and_(Cours.start_time == start_time, Cours.end_time == end_time)).all()

            if len(courses) > 0:
                return {"error" :f"Le groupe {current_group.name} à déjà cours !"}, 409

            #Si une salle est déjà prise entre start_time et end_time
            if name_salle!=None:
                courses = query.filter_by(name_salle=name_salle).filter(and_(Cours.start_time < end_time, Cours.end_time > start_time)).all()

                if len(courses) > 0: return {"error" :"Cette salle est déjà prise entre ces horaires"},409


                courses = query.filter(Cours.name_salle==name_salle).filter(and_(Cours.end_time > start_time, Cours.end_time < end_time)).all()

                if len(courses) > 0: 
                    return {"error" :"Cette salle est déjà prise"},409


            if id_enseignant!=None:
                courses = query.filter_by(id_enseignant=id_enseignant).filter(and_(Cours.start_time < end_time, Cours.end_time > start_time)).all()

                if len(courses) > 0: 
                    warning = "Attention ! Ce professeur à déjà un cours dans cette plage horaire"

                courses = query.filter(Cours.id_enseignant==id_enseignant).filter(and_(Cours.end_time > start_time, Cours.end_time < end_time)).all()

                if len(courses) > 0:
                    warning = "Attention ! Ce professeur à déjà un cours dans cette plage horaire"


        if warning != "":
            return {"warning" : warning}, 201
        
        return None, 200
    
    # Publie tous les cours non publiés et supprime les cours annulés
    @staticmethod
    def publish():
        courses = Cours.query.filter_by(is_published=0).all()
        for course in courses:
            course.is_published = 1
        db.session.commit()

        courses_delete = Cours.query.filter_by(is_published=2).all()
        for course in courses_delete:
            db.session.delete(course)
        db.session.commit()
        return courses
    
    # Annule tous les cours non publiés et republie les cours annulés
    @staticmethod
    def cancel():
        courses = Cours.query.filter_by(is_published=0).all()
        for course in courses:
            db.session.delete(course)
        db.session.commit()

        courses = Cours.query.filter_by(is_published=2).all()
        for course in courses:
            course.is_published = 1
        db.session.commit()


        return courses
    
    # Duplique les cours d'une période à une autre pour un groupe spécifié
    @staticmethod
    def paste(start_time, end_time, id_group, start_time_attempt, sat_date, sun_date, **kwargs):

        start_time = datetime.strptime(start_time, '%Y-%m-%d')
        end_time = datetime.strptime(end_time, '%Y-%m-%d') + timedelta(days=1)
        start_time_attempt = datetime.strptime(start_time_attempt, '%Y-%m-%d')
        sat_date = datetime.strptime(sat_date, '%Y-%m-%d')
        sun_date = datetime.strptime(sun_date, '%Y-%m-%d')

        days_diff = (start_time_attempt - start_time).days
        end_time_attempt = end_time + timedelta(days=days_diff)
            

        groups = GroupeService.get_tree(id_group)

        # for group in groups:
        #     overlapping_courses = Cours.query.filter_by(id_group=group).filter(and_(Cours.end_time >= start_time_attempt, Cours.start_time < end_time_attempt)).all()
        #     if len(overlapping_courses)>0:
        #         for course in overlapping_courses:
        #             course.is_published = 2
        #         db.session.commit()

        result = []
        for group in groups:
            courses = Cours.query.filter(Cours.id_group==group).filter(and_(Cours.end_time >= start_time, Cours.start_time < end_time)).all()
            for course in courses:

                new_course = course.duplicate()
                new_course.start_time = course.start_time + timedelta(days=days_diff)
                new_course.end_time = new_course.end_time + timedelta(days=days_diff)
                new_course.is_published = 0

                if not (new_course.start_time >= sat_date and new_course.end_time <= sun_date):

                    overlapping_courses = Cours.query.filter(and_(Cours.end_time >= new_course.start_time, Cours.start_time < new_course.end_time)).all()
                    
                    
                    if(len(overlapping_courses) > 0):

                        if(overlapping_courses[0].name_salle == new_course.name_salle):
                            print("new_course", new_course)
                            new_course.name_salle = None

                        if(overlapping_courses[0].id_enseignant == new_course.id_enseignant):
                            print("new_course", new_course)
                            new_course.id_enseignant = None

                        group_tree_of_new_course = GroupeService.get_tree(new_course.id_group)
                        print(group_tree_of_new_course)
                        for group_t in group_tree_of_new_course:
                            if(overlapping_courses[0].id_group == group_t):
                                group_of_new_course = GroupeService.get_groupe_by_id(new_course.id_group)
                                return {"error" :f"Le groupe {group_of_new_course.name} à déjà cours !"}, 409
                    
                    db.session.add(new_course)
                    result.append(new_course)
            db.session.commit()
        return result
    
    # Duplique un cours dans les groupes spécifiés
    @staticmethod
    def duplicate(courseId, groupsToDuplicateTo, **kwargs):

        if not courseId:
            return {"Aucun cours transmis !"},404

        if not groupsToDuplicateTo:
            return {"Aucun groupes choisis !"},404

        course = Cours.query.filter(Cours.id == courseId).first()
        
        if course:
            result = []
            for group in groupsToDuplicateTo:
                new_course = course.duplicate()

                new_course.id_group = group
                new_course.is_published = 0

                group_has_course = Cours.query.filter(Cours.id_group == group).filter(and_(Cours.end_time >= new_course.start_time, Cours.start_time <= new_course.end_time)).first()                            

                if not group_has_course:
                    db.session.add(new_course)
                    db.session.commit()
                    result.append(new_course)

            return result
        else:
            return {"Aucun cours avec cet id !"},404

    # Récupère tous les cours d'un enseignant
    @staticmethod
    def get_courses_by_teacher(id_user):
        try:
            teacher = Teacher.query.filter_by(id_user=id_user).first()
            return Cours.query.filter_by(id_enseignant=teacher.id_teacher).all()
        except Exception as e:
            return {"error": str(e)}, 403

    

