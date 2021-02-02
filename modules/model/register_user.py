from datetime import date

from pymongo import results
from modules.model.entities.user import User
from modules.model.db import DB

today = date.today()

# USER SCHEMA EXAMPLE
# user_test = {
#   'name': "Axel",
#   'total_days': 365,
#   'save_per_day': 'random',
#   'count_days': 1,
#   'chat_id': 'TELEGRAM_CHAT_ID',
#   'days': [33, 66],
#   'last_save_date': today.strftime("%d/%m/%Y"),
#   'total': 0,
# }

def insert_new_user(**kwargs):

  user = User(**kwargs)

  result = DB.users.insert_one(user.get_dict())
  print('Agregado el usuario. ID:', format(result.inserted_id))
  return result

def insert_new_user_obj(user):

  result = DB.users.insert_one(user.get_dict())
  print('Agregado el usuario. ID:', format(result.inserted_id))
  return result
