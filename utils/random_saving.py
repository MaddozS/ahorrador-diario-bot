import random

def get_random_saving(total_days: int, days_selected) -> None:

  list_total_days = range(1, total_days+1)
  new_list = [day for day in list_total_days if day not in days_selected]

  return random.choice(new_list)