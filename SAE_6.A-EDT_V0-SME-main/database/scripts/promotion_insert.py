from models.Promotion import Promotion
from database.config import db 
from services.PromotionService import PromotionService


dataPromotions = [
  {
    'niveau' : 3,
    'year' : 2023,
    'name' : 'BUT INFO S3'
  },

  {
    'niveau' : 4,
    'year' : 2022,
    'name' : 'BUT INFO S4'
  },

  {
    'niveau' : 2,
    'year' : 2023,
    'name' : 'BUT GACO S2'
  },

  {
    'niveau' : 4,
    'year' : 2022,
    'name' : 'BUT GACO S4'
  },

  {
    'niveau' : 5,
    'year' : 2023,
    'name' : 'BUT QLIO S5'
  },

  {
    'niveau' : 4,
    'year' : 2023,
    'name' : 'BUT INFO S4'
  }
]

for promotion in dataPromotions:
    PromotionService.create_promo(promotion)
