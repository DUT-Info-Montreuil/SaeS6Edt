from models.User import User
from database.config import db 
from services.StudentService import StudentService


dataUsers = [

  {
    'username' : 'jonas_obrun',
    'password' : 'jonas1234',
    'name' : 'Jonas',
    'lastname' : 'Obrun',
    'INE' : 'aeifyg848184'
  },

  {
    'username' : 'cyril_grosjean',
    'password' : 'cyril1234',
    'name' : 'Cyril',
    'lastname' : 'Grosjean',
    'INE' : 'erhgiebg555'
  },

  {
    'username' : 'nicolas_ramirez',
    'password' : 'nicolas1234',
    'name' : 'Nicolas',
    'lastname' : 'Ramirez',
    'INE' : 'kajsfafhbazf777'
  },

  {
    'username' : 'ismael_argence',
    'password' : 'ismael1234',
    'name' : 'Ismael',
    'lastname' : 'Argence',
    'INE' : 'aekvjhkajbgjhaevg88'
  },

  {
    'username' : 'onur_genc',
    'password' : 'onur1234',
    'name' : 'Onur',
    'lastname' : 'Genc',
    'INE' : 'aisgfuyazufg5698'
  },

]

for user in dataUsers:
    StudentService.create_student(user)

