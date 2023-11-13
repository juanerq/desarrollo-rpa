import logging

formatter = '[%(asctime)s] [%(levelname)s]: %(message)s'

logging.basicConfig(
  level=logging.DEBUG, 
  format=formatter,
  datefmt='%Y-%m-%d %H:%M:%S'
)