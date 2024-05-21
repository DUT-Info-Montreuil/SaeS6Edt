from models.ResponsableEdt import ResponsableEdt
from database.config import db 
from services.ResponsableEdtService import ResponsableEdtService


dataRespEDT = [
  {
    'name' : 'Sihem',
    'lastname' : 'Belabbes',
    'username' : 'sbelabbes',
    'password' : 'sihem1234'
  },
  {
    'name' : 'Anne',
    'lastname' : 'Ricordeau',
    'username' : 'aricordeau',
    'password' : 'anne1234'
  }
]


for resp in dataRespEDT:
    ResponsableEdtService.create_responsable_edt(resp)


    