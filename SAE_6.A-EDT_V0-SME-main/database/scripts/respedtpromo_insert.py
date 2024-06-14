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
    existing_resp = ResponsableEdt.query.filter_by(username=resp['username']).first()
    if not existing_resp:
        ResponsableEdtService.create_responsable_edt(resp)
    else:
        print(f"Responsable with username {resp['username']} already exists.")