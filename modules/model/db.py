from pymongo import MongoClient, database
import os

class DBInit():
  def __init__(self, username, password, db_name):
    self.username = username
    self.password = password
    self.database_name = db_name


  def start_connection(self):
    uri = os.environ['db_uri']

    uri = uri.replace('<user>', self.username)
    uri = uri.replace('<pass>', self.password)
    uri = uri.replace('<dbname>', self.database_name)
    
    self.client = MongoClient(uri)

  def get_database(self):
    return self.client[self.database_name]

database = DBInit(os.environ['username_db'], os.environ['password_db'], os.environ['name_db'])
database.start_connection()

DB = database.get_database()