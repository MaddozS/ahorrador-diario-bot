from datetime import date
from modules.model.get_user import get_user
from random import random
from modules.model.db import DB
from utils.random_saving import get_random_saving

def update_user_by_chat_id(chat_id, **kwarg):
  DB.users.update_one(
    {'chat_id': chat_id},
    {
      "$set": kwarg
    }
  )

  user = get_user(chat_id)
  return user

def submit_saving(chat_id) -> None:
  user = get_user(chat_id)

  saving = 0
  day = 0
  
  if user['save_per_day'] == 'random':
    saving = get_random_saving(user['total_days'], user['days'])
    day = saving
  else:
    saving = user['save_per_day']
    day = user['count_days'] + 1
  
  user['days'].append(day)
  
  update_user_by_chat_id( chat_id,
    total = user['total'] + saving,
    count_days = user['count_days'] + 1,
    days = user['days'],
    last_saving_date = date.today().strftime("%d/%m/%Y")
  )
  #   {'chat_id': chat_id},
  #   {
  #     "$set":{
  #       'total': user['total'] + saving,
  #       'count_days': user['count_days'] + 1,
  #       'days': user['days'],
  #       'last_saving_date': date.today().strftime("%d/%m/%Y")
  #     }
  #   }
  # )

  return day, saving