import schedule
import time
import presentation.server 

if __name__ == '__main__':
  while True:
    schedule.run_pending()
    time.sleep(1)