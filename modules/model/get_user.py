from modules.model.db import DB

def is_user(chat_id):
  user = DB.users.find_one({'chat_id': chat_id})
  
  if user:
    return True
  else:
    return False

def is_completed(chat_id):
  user = DB.users.find_one({'chat_id': chat_id})
  
  return user['completed']
  
def get_user(chat_id):
  result = DB.users.find_one({'chat_id': chat_id})
  return result
  