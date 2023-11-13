import logging
import os
from presentation.upload.loadData import loadShippings
from config.env import config

FILE_NAME = 'shipments-data.csv'
DATA_FILE_PATH = 'files/' + FILE_NAME

def uploadShipmentsData():
  if os.path.exists(DATA_FILE_PATH):
    loadShippings(DATA_FILE_PATH, config['TEST_MAIL'])

    nuevo_path = os.path.join(os.path.dirname(DATA_FILE_PATH), 'uploaded-data.csv')
    os.rename(DATA_FILE_PATH, nuevo_path)
  else:
    logging.warning(f"Data file not found in the path {DATA_FILE_PATH}")