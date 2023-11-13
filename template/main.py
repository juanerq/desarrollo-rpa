import logging
import schedule
import time
import config.logging
import presentation.server
from script import uploadShipmentsData

if __name__ == '__main__':
  # Cargue automatico de archivo shipments-data.csv en Mongo DB
  uploadShipmentsData()

  logging.info('🟢 Online service')

  # Iniciar monitoreo de tareas programadas
  while True:
    schedule.run_pending()
    time.sleep(1)
