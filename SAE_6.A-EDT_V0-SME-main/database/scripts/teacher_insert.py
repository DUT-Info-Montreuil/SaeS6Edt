from models.Teacher import Teacher
from database.config import db 
from services.TeacherService import TeacherService


dataTeacher = [

    {
      'name' : 'Amélie',
      'lastname' : 'Golven',
      'username' : 'agolven',
      'password' : 'agolven1234'
    }
]


for teacher in dataTeacher:
    existing_teacher = Teacher.query.filter_by(teacher=teacher['username']).first()
    if not existing_teacher:
        TeacherService.create_teacher(teacher)
    else:
        print(f"Teacher with username {teacher['username']} already exists.")
    

