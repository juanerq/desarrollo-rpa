import logging
from pymongo import MongoClient
from config.env import config

try:
  conn = MongoClient(config['MONGO_URL'])
  logging.info('✅ Successful connection to the database')

except Exception as e:
  logging.critical(f"🚨 Error connecting to database: {e}")
