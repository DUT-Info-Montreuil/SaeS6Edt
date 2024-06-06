from models.ResponsableEdt import ResponsableEdt
from database.config import db 
from services.ResponsableEdtService import ResponsableEdtService


dataRespEDT = [
  #Département INFO
  {
    'name' : 'Philippe',
    'lastname' : 'Bonnot',
    'username' : 'pbonnot',
    'password' : 'bonnot1234'
  },
  {
    'name' : 'Nedra',
    'lastname' : 'Mellouli',
    'username' : 'nmellouli',
    'password' : 'mellouli1234'
  },
  {
    'name' : 'Marianne',
    'lastname' : 'Simonot',
    'username' : 'msimonot',
    'password' : 'simonot1234'
  },
  {
    'name' : 'Marc',
    'lastname' : 'Homps',
    'username' : 'mhomps',
    'password' : 'homps1234'
  },
  {
    'name' : 'Mario',
    'lastname' : 'Cataldi',
    'username' : 'mcataldi',
    'password' : 'cataldi1234'
  },
  {
    'name' : 'Aurelien',
    'lastname' : 'Bossard',
    'username' : 'abossard',
    'password' : 'bossard1234'
  },
  #Département INFO-COM
  {
    'name' : 'Marc',
    'lastname' : 'Kaiser',
    'username' : 'mkaiser',
    'password' : 'kaiser1234'
  },
  {
    'name' : 'Viviane',
    'lastname' : 'Claus',
    'username' : 'vclaus',
    'password' : 'claus1234'
  },
  #Département QLIO
    {
    'name' : 'Sonia',
    'lastname' : 'Menjeli',
    'username' : 'smenjeli',
    'password' : 'menjeli1234'
  },
    {
    'name' : 'Charlotte',
    'lastname' : 'Ballaydally',
    'username' : 'cballaydally',
    'password' : 'ballaydally1234'
  },
    {
    'name' : 'Yasmina',
    'lastname' : 'Hani',
    'username' : 'yhani',
    'password' : 'hani1234'
  },
  #Departement GACO
  {
    'name' : 'Amine',
    'lastname' : 'Zizi',
    'username' : 'azizi',
    'password' : 'zizi1234'
  },
  {
    'name' : 'Vincent',
    'lastname' : 'Lebel',
    'username' : 'vlebel',
    'password' : 'lebel1234'
  },
  {
    'name' : 'Stéphane',
    'lastname' : 'Hurtado',
    'username' : 'shurtado',
    'password' : 'hurtado1234'
  },
  {
    'name' : 'Jean-François',
    'lastname' : 'Dhenin',
    'username' : 'jfdhenin',
    'password' : 'dhenin1234'
  },
  {
    'name' : 'Marielle',
    'lastname' : 'Baboulall',
    'username' : 'mbaboulall',
    'password' : 'baboulall1234'
  },
  {
    'name' : 'Noiric',
    'lastname' : 'Saintini',
    'username' : 'nsaintini',
    'password' : 'saintini1234'
  },
  {
    'name' : 'Catherine',
    'lastname' : 'Durand',
    'username' : 'cdurand',
    'password' : 'durand1234'
  }
]

for resp in dataRespEDT:
    ResponsableEdtService.create_responsable_edt(resp)


    