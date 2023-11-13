import logging
import schedule
import time
import config.logging
#import presentation.server 
import presentation.server 
from script import uploadShipmentsData

if __name__ == '__main__':
  uploadShipmentsData()

  logging.info('🚀 Service running...')

  while True:
    schedule.run_pending()
    time.sleep(1)
