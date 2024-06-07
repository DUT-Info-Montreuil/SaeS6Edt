from models.Promotion import Promotion
from database.config import db 
from services.PromotionService import PromotionService


dataPromotions = [
  {'niveau' : 1,'year' : 2024,'name' : 'BUT INFO S1'},
  {'niveau' : 2,'year' : 2024,'name' : 'BUT INFO S2'},
  {'niveau' : 3,'year' : 2024,'name' : 'BUT INFO S3'},
  {'niveau' : 4,'year' : 2024,'name' : 'BUT INFO S4'},
  {'niveau' : 5,'year' : 2024,'name' : 'BUT INFO S5'},
  {'niveau' : 6,'year' : 2024,'name' : 'BUT INFO S6'},
  {'niveau' : 1,'year' : 2024,'name' : 'BUT INFOCOM S1'},
  {'niveau' : 2,'year' : 2024,'name' : 'BUT INFOCOM S2'},
  {'niveau' : 3,'year' : 2024,'name' : 'BUT INFOCOM S3'},
  {'niveau' : 4,'year' : 2024,'name' : 'BUT INFOCOM S4'},
  {'niveau' : 5,'year' : 2024,'name' : 'BUT INFOCOM S5'},
  {'niveau' : 6,'year' : 2024,'name' : 'BUT INFOCOM S6'},
  {'niveau' : 1,'year' : 2024,'name' : 'BUT QLIO S1'},
  {'niveau' : 2,'year' : 2024,'name' : 'BUT QLIO S2'},
  {'niveau' : 3,'year' : 2024,'name' : 'BUT QLIO S3'},
  {'niveau' : 4,'year' : 2024,'name' : 'BUT QLIO S4'},
  {'niveau' : 5,'year' : 2024,'name' : 'BUT QLIO S5'},
  {'niveau' : 6,'year' : 2024,'name' : 'BUT QLIO S6'},
  {'niveau' : 1,'year' : 2024,'name' : 'BUT GACO S1'},
  {'niveau' : 2,'year' : 2024,'name' : 'BUT GACO S2'},
  {'niveau' : 3,'year' : 2024,'name' : 'BUT GACO S3'},
  {'niveau' : 4,'year' : 2024,'name' : 'BUT GACO S4'},
  {'niveau' : 5,'year' : 2024,'name' : 'BUT GACO S5'},
  {'niveau' : 6,'year' : 2024,'name' : 'BUT GACO S6'}
]

for promotion in dataPromotions:
    PromotionService.create_promo(promotion)
