import logging
import os

# Servicios
from presentation.upload.loadData import loadShippings

# Configuración
from config.env import config

# Conexión a la base de datos
from config.db import conn
myDB = conn.store

# Colecciones
colectionUsers = myDB.users
colectionShippings  = myDB.shippings

FILE_NAME = 'shipments-data.csv'
DATA_FILE_PATH = 'files/' + FILE_NAME


def uploadShipmentsData():
  # Se valida si el archivo de datos existe
  if os.path.exists(DATA_FILE_PATH):
    # Se eliminan los datos de la colecciones para cargar nuevos datos sin duplicarlos
    logging.info("Cleaning data collections... 🗑️")
    colectionUsers.drop()
    colectionShippings.drop()
    
    loadShippings(DATA_FILE_PATH, config['TEST_MAIL'])

    # Renombrar archivo de datos subido
    # Esto se hace para cargue el archivo solo al iniciar el servicio por primera vez
    nuevo_path = os.path.join(os.path.dirname(DATA_FILE_PATH), 'uploaded-data.csv')
    os.rename(DATA_FILE_PATH, nuevo_path)
  else:
    logging.debug(f"No file found to load in the path {DATA_FILE_PATH}")