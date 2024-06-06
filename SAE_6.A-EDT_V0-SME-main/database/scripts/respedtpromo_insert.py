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

# Département INFO
# p.bonnot@iut.univ-paris8.fr
# n.mellouli@iut.univ-paris8.fr
# m.simonot@iut.univ-paris8.fr
# m.homps@iut.univ-paris8.fr
# m.cataldi@iut.univ-paris8.fr
# a.bossard@iut.univ-paris8.fr

# Département GACO
# Amine ZIZI <a.zizi@iut.univ-paris8.fr>
# Vincent LEBEL <v.lebel@iut.univ-paris8.fr>
# Stéphane HURTADO <s.hurtado@iut.univ-paris8.fr>
# DHENIN Jean-François <jf.dhenin@iut.univ-paris8.fr>
# BABOULALL Marielle <m.baboulall@iut.univ-paris8.fr>
# Noiric SAINTINI <n.saintini@iut.univ-paris8.fr>
# Catherine DURAND <c.durand@iut.univ-paris8.fr>


# Département QLIO
# s.menjeli@iut.univ-paris8.fr
# c.ballaydally@iut.univ-paris8.fr
# y.hani@iut.univ-paris8.fr

# Département INFO-COM
# m.kaiser@iut.univ-paris8.fr
# vivianeclaus@icloud.com





for resp in dataRespEDT:
    ResponsableEdtService.create_responsable_edt(resp)


    