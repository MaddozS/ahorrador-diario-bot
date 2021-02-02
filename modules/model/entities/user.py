from datetime import date
today = date.today()

class User():
  def __init__(self,
        chat_id, 
        name= "", 
        total_days = 0, 
        save_per_day = 'random', 
        last_saving_date = today.strftime("%d/%m/%Y"),
        count_days = 0,
        total = 0,
        days = [],
        completed = False) -> None:

      self.chat_id = chat_id
      self.name = name
      self.total_days = total_days
      self.save_per_day = save_per_day
      self.last_saving_date = last_saving_date
      self.count_days = count_days
      self.days = days
      self.last_saving_date = last_saving_date
      self.total = total
      self.completed = completed
  
  def get_dict(self) -> dict:
    return {
      'chat_id': self.chat_id,
      'name': self.name,
      'total_days': self.total_days,
      'save_per_day': self.save_per_day,
      'count_days': self.count_days,
      'days': self.days,
      'last_saving_date': self.last_saving_date,
      'total': self.total,
      'completed': self.completed,
    }