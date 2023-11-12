from pymongo import MongoClient
from config.env import config

conn = MongoClient(config['MONGO_URL'])





