from models.Teacher import Teacher
from database.config import db 
from services.TeacherService import TeacherService


dataTeacher = [

    {
      'name' : 'Nedra',
      'lastname' : 'Nauwynck',
      'username' : 'nnauwynck',
      'password' : 'nedra1234'
    },

    {
      'name' : 'Philippe',
      'lastname' : 'Bonnot',
      'username' : 'pbonnot',
      'password' : 'philippe1234'
    }
]


for teacher in dataTeacher:
    TeacherService.create_teacher(teacher)
    

